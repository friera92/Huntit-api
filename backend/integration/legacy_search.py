"""Search the frozen teammate release without consulting mutable working rows.

Recorded date periods and missing fields remain intact. An undated year-round
label is information about its recorded season year, not new explicit coverage.
The public engine decides whether that information can support its main answer.
"""
from collections import defaultdict
from copy import deepcopy
from datetime import date
import re


SCOPE_FIELDS = ("zone", "dmu", "regulatory_area", "managed_area")
SCOPE_CATALOGS = {"zone": "huntingzone", "dmu": "deermanagementunit",
                  "regulatory_area": "regulatoryarea", "managed_area": "managedarea"}
FALL_CODES = {"ARCHERY", "CROSSBOW", "MUZZLELOADING_GUN", "MUZZLELOADER", "FALL_TURKEY"}
SPRING_CODES = {"SPRING_TURKEY", "YOUTH_TURKEY"}
UNKNOWN_BAG = "Bag limits are not recorded in this season; check the official source."
UNKNOWN_LICENSES = "License and permit requirements are not recorded in this season; check the official source."
UNKNOWN_METHODS = "Allowed methods are not recorded in this season; check the official source."


def _year_matches(label, when, *, allow_blank=False):
    if not label:
        return allow_blank
    match = re.fullmatch(r"(\d{4})(?:-(\d{4}))?", label.strip())
    return bool(match and int(match[1]) <= when.year <= int(match[2] or match[1]))


class ApprovedLegacySearch:
    """Read one already approved snapshot for a validated hunt context."""

    def __init__(self, context, snapshot):
        self.context = context
        self.snapshot = deepcopy(snapshot or {})
        self.catalogs = {kind: {row["id"]: row for row in rows}
                         for kind, rows in self.snapshot.get("records", {}).items()}
        self.approval = self.snapshot.get("approval", {})
        self.verified_at = self.approval.get("recorded_at")
        self.verification_basis = self.approval.get("verification_basis", "")
        self.periods = defaultdict(list)
        for row in self._rows("seasonperiod"):
            self.periods[row["season"]].append({
                "start_date": row["start_date"], "end_date": row["end_date"],
                "notes": row.get("notes", ""),
            })
        for rows in self.periods.values():
            rows.sort(key=lambda row: (row["start_date"], row["end_date"]))
        self._result = None
        self._sources = {}

    def _rows(self, kind):
        return self.catalogs.get(kind, {}).values()

    def _get(self, kind, identifier):
        return self.catalogs.get(kind, {}).get(identifier, {})

    def _source(self, identifier):
        original = self._get("source", identifier)
        if not original:
            return None
        source = {key: original.get(key) for key in [
            "organization", "title", "url", "document_type", "effective_date", "retrieved_at", "notes",
        ]}
        source.update({"source_checked_on": None, "last_verified_at": self.verified_at,
                       "original_last_verified_at": original.get("last_verified_at"),
                       "verification_basis": self.verification_basis})
        self._sources[identifier] = source
        return source

    def _matches_selected_scopes(self, row):
        return all(self.context.identifier(field) is None or row.get(field) in
                   (None, self.context.identifier(field)) for field in SCOPE_FIELDS)

    def _scope_complete(self, row):
        return all(row.get(field) is None or self.context.identifier(field) is not None
                   for field in SCOPE_FIELDS)

    def _active_reference(self, row):
        if not row.get("is_active", True):
            return False
        area = self._get("managedarea", row.get("managed_area"))
        return not area or area.get("is_active", True)

    def _base_matches(self, row, *, nullable_land=False):
        return (row.get("species") == self.context.identifier("species")
                and (row.get("land_type") == self.context.identifier("land_type")
                     or nullable_land and row.get("land_type") is None)
                and self._active_reference(row)
                and _year_matches(row.get("season_year"), self.context.hunting_date,
                                  allow_blank=nullable_land)
                and self._matches_selected_scopes(row))

    def _season_code(self, season):
        return self._get("seasontype", season.get("season_type")).get("code", "")

    def _matches_date(self, season):
        periods = self.periods[season["id"]]
        if periods:
            return any(date.fromisoformat(row["start_date"]) <= self.context.hunting_date
                       <= date.fromisoformat(row["end_date"]) for row in periods)
        return self._season_code(season) == "YEAR_ROUND"

    def _select_seasons(self):
        candidates = [row for row in self._rows("huntingseason") if self._base_matches(row)]
        active = [row for row in candidates if self._matches_date(row)]
        if active:
            self.context.require({field for row in active for field in SCOPE_FIELDS
                                  if row.get(field) is not None})
        complete = [row for row in candidates if self._scope_complete(row)]
        if candidates and not active and not complete:
            self.context.require({field for row in candidates for field in SCOPE_FIELDS
                                  if row.get(field) is not None})
        return complete

    def _scope(self, row, *, advisory=False):
        land = self._get("landtype", row.get("land_type")).get("name")
        parts = [land] if land else []
        if advisory:
            parts.append("WMA advisory; an area-specific open season is not recorded")
        for field in SCOPE_FIELDS:
            reference = self._get(SCOPE_CATALOGS[field], row.get(field))
            if reference:
                value = reference.get("code") if field in ("zone", "dmu") else reference.get("name")
                parts.append(f"{field.replace('_', ' ').title()}: {value}")
        if row.get("season_group"):
            parts.append(f"{row['season_group']} season group")
        season_type = self._get("seasontype", row.get("season_type"))
        if season_type:
            parts.append(season_type["name"])
        return "; ".join(parts) or "All recorded land types"

    def _category(self, row):
        return self._get("harvestcategory", row.get("harvest_category")).get("name", "All recorded categories")

    def _bag_matches_season(self, bag, season):
        if bag.get("season_type") is not None and bag["season_type"] != season.get("season_type"):
            return False
        group, code = bag.get("season_group", "").upper(), self._season_code(season)
        if group == "FALL":
            return code in FALL_CODES
        if group == "SPRING":
            return code in SPRING_CODES
        return not group or group in code.upper()

    def _bag_text(self, bag):
        value = ("Unlimited (as recorded)" if bag.get("is_unlimited") else
                 str(bag["limit"]) if bag.get("limit") is not None else "Not recorded")
        text = f"{self._category(bag)} — {bag['limit_type']}: {value}"
        if bag.get("conditions"):
            text += f". {bag['conditions']}"
        if bag.get("dmu") is not None:
            text += f" [{self._scope(bag)}]"
        return text

    def _season(self, row, bags):
        season_type = self._get("seasontype", row["season_type"])
        limits = [f"{label}: {row[field]}" for field, label in [
            ("daily_bag_limit", "Daily"), ("possession_limit", "Possession"), ("annual_limit", "Annual"),
        ] if row.get(field) is not None]
        limits.extend(self._bag_text(bag) for bag in bags if self._bag_matches_season(bag, row))
        licenses, methods = [], []
        for identifier in row.get("permits", []):
            permit = self._get("licensepermit", identifier)
            if permit and permit.get("is_active", True):
                licenses.append("\n".join(permit.get(field, "") for field in
                                          ["name", "description", "requirements"] if permit.get(field)))
                self._source(permit.get("source"))
        if season_type.get("description"):
            methods.append(season_type["description"])
        for identifier in row.get("legal_methods", []):
            method = self._get("legalmethod", identifier)
            if method:
                methods.append("\n".join(method.get(field, "") for field in ["name", "description"]
                                         if method.get(field)))
        return {"id": row["id"], "name": season_type.get("name", ""),
                "code": season_type.get("code", ""), "season_year": row["season_year"],
                "scope": self._scope(row), "category": self._category(row),
                "periods": deepcopy(self.periods[row["id"]]), "matches_date": self._matches_date(row),
                "year_round": season_type.get("code") == "YEAR_ROUND",
                "bag": "\n".join(dict.fromkeys(limits)) or UNKNOWN_BAG,
                "licenses": "\n".join(dict.fromkeys(licenses)) or UNKNOWN_LICENSES,
                "methods": "\n".join(dict.fromkeys(methods)) or UNKNOWN_METHODS,
                "notes": row.get("notes", ""), "source": self._source(row.get("source"))}

    def records(self):
        if self._result is not None:
            return self._result
        seasons = self._select_seasons()
        active = [row for row in seasons if self._matches_date(row)]
        bags = [row for row in self._rows("baglimitrule") if self._base_matches(row)
                and self._scope_complete(row)]
        # Closed seasons keep their own complete rules; the general bag list is
        # limited to active season families when an active season is recorded.
        selected_bags = [bag for bag in bags if any(self._bag_matches_season(bag, row)
                                                  for row in active or seasons)]
        notes = []
        land = self._get("landtype", self.context.identifier("land_type"))
        for row in self._rows("regulationnote"):
            if not self._base_matches(row, nullable_land=True) or not self._scope_complete(row):
                continue
            advisory = row.get("land_type") is None and "wma" in row.get("title", "").casefold()
            if advisory and "private" in land.get("name", "").casefold():
                continue
            notes.append({"id": row["id"], "title": row.get("title", ""), "text": row["text"],
                          "season_year": row.get("season_year", ""), "scope": self._scope(row, advisory=advisory),
                          "source": self._source(row.get("source"))})
        self._result = {"verified_at": self.verified_at, "verification_basis": self.verification_basis,
                        "seasons": [self._season(row, bags) for row in seasons],
                        "bag_rules": [{"id": row["id"], "limit_type": row["limit_type"],
                                       "season_year": row["season_year"], "scope": self._scope(row),
                                       "category": self._category(row), "limit": row.get("limit"),
                                       "is_unlimited": row.get("is_unlimited", False),
                                       "conditions": row.get("conditions", ""),
                                       "source": self._source(row.get("source"))} for row in selected_bags],
                        "notes": notes}
        return self._result

    @property
    def has_coverage(self):
        return bool(self.records()["seasons"])

    @property
    def active_seasons(self):
        return [row for row in self.records()["seasons"] if row["matches_date"]]

    @property
    def coverage(self):
        periods = {(row["start_date"], row["end_date"]) for season in self.records()["seasons"]
                   for row in season["periods"]}
        return [{"start_date": start, "end_date": end} for start, end in sorted(periods)]

    @property
    def sources(self):
        self.records()
        return [self._sources[key] for key in sorted(self._sources)]
