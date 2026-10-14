"""Object-oriented compliance lookup over administrator-reviewed snapshots.

The engine reports the scope it knows; it never converts missing data, expired
coverage or a private-land exception into blanket permission to hunt.
"""
from dataclasses import dataclass
from datetime import date

from rest_framework.exceptions import ValidationError

from .models import RegulationDraft, RegulatoryPublication, SCOPE_MODELS
from .serializers import is_private
from .services import species_data
from .legacy_release import current_approved_legacy_snapshot
from .legacy_search import ApprovedLegacySearch
from .public_scope_guards import has_required_python_area_scope


@dataclass(frozen=True)
class HuntContext:
    selections: dict

    @property
    def hunting_date(self):
        return self.selections["date"]

    def identifier(self, field):
        obj = self.selections.get(field)
        return obj.pk if obj is not None else None

    def accepts(self, scopes):
        for field, accepted in scopes.items():
            selected = self.identifier(field)
            accepted = accepted if isinstance(accepted, list) else [accepted]
            if selected is not None and selected not in accepted:
                return False
        return True

    def require(self, fields):
        prompts = {"zone": "Select the hunting zone required by these rules.",
                   "dmu": "Select the deer management unit so antler and antlerless restrictions can be checked.",
                   "managed_area": "Select the managed area; public-land rules vary by area.",
                   "regulatory_area": "Select the regulatory area required by these rules."}
        missing = {field: [prompts[field]] for field in fields if self.identifier(field) is None}
        if missing:
            raise ValidationError(missing)

    def within(self, period):
        return (date.fromisoformat(period["start_date"]) <= self.hunting_date <= date.fromisoformat(period["end_date"])
                and ("weekdays" not in period or self.hunting_date.isoweekday() in period["weekdays"]))


@dataclass(frozen=True)
class ReviewedRule:
    publication: RegulatoryPublication
    number: int
    content: dict

    def periods(self, context):
        return [period for period in self.content["periods"] if context.within(period)]

    def result(self, context):
        return {"id": f"review-{self.publication.pk}-{self.number}",
                "publication_id": self.publication.pk, "revision": self.publication.revision,
                "season_type": self.content["name"], "season_type_code": self.content["code"],
                "category": self.content["category"], "periods": self.periods(context),
                "scopes": self.content.get("scopes", {}), "sources": self.content["source_urls"],
                "last_verified_at": self.publication.reviewed_at.isoformat()}


class ComplianceEngine:
    def __init__(self, selections):
        self.context = HuntContext(selections)

    def search(self):
        context = self.context
        species, land = context.selections["species"], context.selections["land_type"]
        legacy_snapshot = current_approved_legacy_snapshot()
        legacy = ApprovedLegacySearch(context, legacy_snapshot) if legacy_snapshot else None
        additional = legacy.records() if legacy else None
        publications = list(RegulatoryPublication.objects.filter(
            is_current=True, snapshot__species_id=species.pk, snapshot__land_type_id=land.pk,
        ).select_related("draft").order_by("pk"))
        applicable = [row for row in publications
                      if context.accepts(row.snapshot.get("scopes", {})) and context.within(row.snapshot["coverage"])
                      and has_required_python_area_scope(row.snapshot, context)]
        context.require({field for row in applicable
                         for field in [*row.snapshot.get("required_inputs", []), *row.snapshot.get("scopes", {})]})
        # Apply all supplied geography before asking for any additional selector.
        scoped_rules = [ReviewedRule(row, index, rule)
                        for row in applicable for index, rule in enumerate(row.snapshot["rules"])
                        if context.accepts(rule.get("scopes", {}))]
        context.require({field for row in scoped_rules for field in row.content.get("scopes", {})})
        active = [row for row in scoped_rules if not row.content.get("prohibited") and row.periods(context)]
        query = {"species": species.pk, "land_type": land.pk, "date": context.hunting_date.isoformat(),
                 "landowner_permission": context.selections["landowner_permission"]}
        query.update({field: context.identifier(field) for field in SCOPE_MODELS})
        result = {**species_data(species, legacy_snapshot, publications=applicable), "landType": land.name, "query": query,
                  "matched_seasons": [row.result(context) for row in active],
                  "verified": bool(applicable), "sources": [], "alerts": [],
                  "status": "reviewed" if active else "closed" if applicable else "no_data"}
        if additional:
            result["additional_records"] = additional
        if not applicable:
            # The separate approval adds turkey's recorded seasons. It must not
            # revive a withdrawn curated answer or extend bounded publications
            # using an imported year-round label with no explicit dates.
            history = RegulatoryPublication.objects.filter(
                snapshot__species_id=species.pk, snapshot__land_type_id=land.pk)
            overlaps_history = any(context.accepts(row.snapshot.get("scopes", {})) for row in history)
            explicit_legacy = bool(legacy and any(row["periods"] for row in additional["seasons"]))
            if legacy and legacy.has_coverage and explicit_legacy and not overlaps_history:
                return self.legacy_result(result, legacy)
            drafts = list(RegulationDraft.objects.filter(species=species, land_type=land))
            drafts = [row for row in drafts if context.accepts(row.payload.get("scopes", {}))
                      and context.within(row.payload["coverage"])]
            if drafts:
                result["status"] = "needs_review"
                result["alerts"].append("Matching working data is awaiting administrator source review. It is not a published hunting answer.")
            elif publications:
                result["alerts"].append("The selected date or area is outside the current reviewed coverage. No hunting permission can be established.")
            else:
                result["alerts"].append("No reviewed rule covers this selection. Missing data does not mean hunting is permitted.")
            # Offer official references without disclosing unreviewed rule claims.
            references = [source for row in drafts for source in row.payload["sources"]]
            if not references:
                references = [source for row in publications for source in row.snapshot["sources"]]
            result["sources"] = self.sources(references, reviewed=False)
            for field in ["dates", "bag", "licenses", "methods"]:
                result[field] = "No reviewed information is available for these selections. Open the official source and confirm the area rules."
            return self.with_legacy_sources(result, legacy)

        references = []
        for publication in applicable:
            result["alerts"].extend(publication.snapshot.get("alerts", []))
            references.extend(publication.snapshot["sources"])
        result["sources"] = self.sources(references, reviewed=True)
        result["alerts"].append("Source-reviewed guidance for the selected scope; check official closures and rule changes before hunting.")
        if is_private(land) and any(row.snapshot.get("permission_required") for row in applicable):
            if not context.selections["landowner_permission"]:
                result["alerts"].append("Landowner permission is required and has not been confirmed. Do not hunt without it.")
                result["eligibility"] = "permission_required"
            else:
                result["eligibility"] = "conditional"
        else:
            result["eligibility"] = "conditional"
        if not active:
            result["alerts"].append("No listed reviewed season is open on the selected date. Do not treat bag or license guidance as permission to hunt.")
            result["eligibility"] = "no_open_season"
        display = active or scoped_rules
        result["dates"] = "\n".join(dict.fromkeys(
            f"{row.content['name']} / {row.content['category']}: {self.period_label(p)}"
            for row in display for p in (row.periods(context) if active else row.content["periods"])
        )) or "No season for the selected location."
        for key in ["bag", "licenses", "methods"]:
            result[key] = "\n".join(dict.fromkeys(
                f"{row.content['name']} / {row.content['category']}: {row.content[key]}" for row in display
            )) or "Not established for this location; consult the official area source."
        for row in display:
            result["alerts"].extend(row.content.get("alerts", []))
        result["alerts"] = list(dict.fromkeys(result["alerts"]))
        result["coverage"] = [row.snapshot["coverage"] for row in applicable]
        return self.with_legacy_sources(result, legacy)

    @staticmethod
    def period_label(period):
        label = f"{period['start_date']} to {period['end_date']}"
        if "weekdays" in period:
            names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            label += " (" + ", ".join(names[value - 1] for value in period["weekdays"]) + " only)"
        return label

    def legacy_result(self, result, legacy):
        """Use verified imported seasons where no curated answer exists."""
        additional = result["additional_records"]
        active = legacy.active_seasons
        display = active or additional["seasons"]
        result.update(verified=True, status="reviewed" if active else "closed",
                      matched_seasons=active, coverage=legacy.coverage,
                      eligibility="conditional" if active else "no_open_season")
        result["dates"] = "\n".join(dict.fromkeys(
            f"{row['name']} / {row['category']}: {period['start_date']} to {period['end_date']}"
            for row in display for period in row["periods"]
            if not active or self.context.within(period)))
        for field in ("bag", "licenses", "methods"):
            result[field] = "\n".join(dict.fromkeys(f"{row['name']}: {row[field]}" for row in display))
        # The season projection already includes its applicable standalone
        # limits, complete with conditions and scoped exceptions.
        result["alerts"] = [
            "Existing project records verified by the project owner on " + additional["verified_at"][:10] +
            "; original season dates and exceptions are preserved. Check official closures and current area rules."
        ]
        if not active:
            result["alerts"].append("No recorded season is open on this date. Recorded limits and permits do not establish permission to hunt.")
        if is_private(self.context.selections["land_type"]) and not self.context.selections["landowner_permission"]:
            result["alerts"].append("Landowner permission is required and has not been confirmed. Do not hunt without it.")
            if active:
                result["eligibility"] = "permission_required"
        for row in additional["notes"]:
            result["alerts"].append((row["title"] + ": " if row["title"] else "") + row["text"])
        return self.with_legacy_sources(result, legacy)

    @staticmethod
    def with_legacy_sources(result, legacy):
        if legacy:
            known = {row["url"] for row in result["sources"]}
            result["sources"].extend(row for row in legacy.sources if row["url"] not in known)
        return result

    @staticmethod
    def sources(references, *, reviewed):
        by_url = {}
        for source in references:
            by_url[source["url"]] = {"title": source["title"], "url": source["url"],
                "retrieved_at": source.get("retrieved_at"), "source_checked_on": source["checked_on"],
                "last_verified_at": source.get("last_verified_at") if reviewed else None,
                "evidence": source["evidence"]}
        return list(by_url.values())
