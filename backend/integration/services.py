"""Read imported records without treating them as reviewed hunting permission."""
import re

from django.db.models import Q
from rest_framework.exceptions import ValidationError

from regulations.models import BagLimitRule, HuntingSeason, RegulationNote
from .serializers import is_private


REVIEW_NOTICE = (
    "Imported regulatory data has not been reviewed by the project team. "
    "Verify the information with the official sources before use."
)


def species_data(species, snapshot=None, *, publications=()):
    # The owner's approval applies to the frozen copy, never later live edits.
    approved = next((row for row in (snapshot or {}).get("records", {}).get("species", [])
                     if row["id"] == species.pk and row.get("is_active", True)), None)
    data = dict(approved or {"common_name": species.common_name, "scientific_name": species.scientific_name,
                        "image_url": species.image_url, "description": species.description,
                        "habitat": species.habitat, "behavior": species.behavior,
                        "hunting_strategy": species.hunting_strategy})
    supplemented_at = None
    supplement_sources = []
    unreviewed_background = approved is None and any(data.get(field) for field in (
        "scientific_name", "description", "habitat", "behavior", "hunting_strategy"))
    for publication in sorted(publications, key=lambda row: (row.reviewed_at, row.pk), reverse=True):
        if not publication.is_current or publication.snapshot.get("species_id") != species.pk:
            continue
        # A blank in the frozen original may be completed only by reviewed content.
        # Later live edits and unpublished drafts never inherit an earlier approval.
        profile = publication.snapshot.get("species_information", {})
        added = False
        for field in ("scientific_name", "description", "habitat", "behavior", "hunting_strategy"):
            if not data.get(field) and profile.get(field):
                data[field] = profile[field]
                added = True
        if added:
            supplemented_at = supplemented_at or publication.reviewed_at.isoformat()
            supplement_sources.extend(profile.get("source_urls", []))
    image = data["image_url"]
    if not image:
        name = data["common_name"].casefold()
        image = next((path for word, path in [
            ("hog", "/hog.png"), ("python", "/python.png"), ("deer", "/deer.png"),
        ] if word in name), "")
    return {
        "id": species.pk, "name": data["common_name"], "scientific": data["scientific_name"],
        "image": image, "about": data["description"], "habitat": data["habitat"], "behavior": data["behavior"],
        "tactics": data["hunting_strategy"],
        "species_information_reviewed": approved is not None or (supplemented_at is not None and not unreviewed_background),
        "species_information_verified_at": None if unreviewed_background else supplemented_at or (
            snapshot["approval"]["recorded_at"] if approved else None),
        "species_information_sources": list(dict.fromkeys(supplement_sources)),
    }


def year_label_matches(label, hunting_date, *, allow_blank=False):
    """A year label is a coarse record scope, not an inferred season boundary."""
    if not label:
        return allow_blank
    match = re.fullmatch(r"(\d{4})(?:-(\d{4}))?", label.strip())
    if not match:
        return False
    first, last = int(match[1]), int(match[2] or match[1])
    return first <= hunting_date.year <= last


def applicable_periods(season, hunting_date):
    return [period for period in season.periods.all() if period.start_date <= hunting_date <= period.end_date]


def season_matches_date(season, hunting_date):
    if applicable_periods(season, hunting_date):
        return True
    return (
        season.season_type.code == "YEAR_ROUND"
        and not season.periods.all()
        and year_label_matches(season.season_year, hunting_date)
    )


def scope_records(seasons, bags, selections):
    """Require scoped selections instead of silently combining different locations."""
    scopes = [
        ("zone", "Select the hunting zone required by these records."),
        ("dmu", "Select the deer management unit required by these records."),
        ("regulatory_area", "Select the regulatory area required by these records."),
        ("managed_area", "Select the managed area required by these records."),
    ]
    # Apply every supplied location before asking for additional geography.
    # Records in another managed area must not introduce unrelated requirements.
    for field, _ in scopes:
        selected = selections.get(field)
        if selected is not None:
            seasons = [row for row in seasons if getattr(row, field + "_id") in (None, selected.pk)]
            bags = [row for row in bags if getattr(row, field + "_id") in (None, selected.pk)]
    for field, prompt in scopes:
        if selections.get(field) is None and any(getattr(row, field + "_id") is not None for row in seasons + bags):
            raise ValidationError({field: [prompt]})
    return seasons, bags


def source_data(source):
    return {
        "title": source.title, "url": source.url,
        "retrieved_at": source.retrieved_at.isoformat() if source.retrieved_at else None,
        "last_verified_at": source.last_verified_at.isoformat() if source.last_verified_at else None,
    }


def search_imported_records(selections):
    """Internal diagnostic of unpublished imports; never use for public answers."""
    species, land_type, hunting_date = selections["species"], selections["land_type"], selections["date"]
    all_seasons = list(HuntingSeason.objects.filter(
        Q(managed_area__isnull=True) | Q(managed_area__is_active=True),
        species=species, land_type=land_type, is_active=True,
    ).select_related(
        "source", "season_type", "zone", "dmu", "regulatory_area", "managed_area", "harvest_category"
    ).prefetch_related("periods", "permits__source", "legal_methods").order_by("pk"))
    seasons = [row for row in all_seasons if season_matches_date(row, hunting_date)]
    season_types = {row.season_type_id for row in seasons}
    season_codes = {row.season_type.code for row in seasons}
    bags = list(BagLimitRule.objects.filter(
        Q(managed_area__isnull=True) | Q(managed_area__is_active=True),
        species=species, land_type=land_type, is_active=True,
    ).select_related("source", "season_type", "harvest_category").order_by("pk"))
    bags = [row for row in bags if year_label_matches(row.season_year, hunting_date)
            and (row.season_type_id is None or row.season_type_id in season_types)
            and (not row.season_group or any(row.season_group.upper() in code.upper() for code in season_codes))]
    seasons, bags = scope_records(seasons, bags, selections)
    # Geographic filtering can remove a season type that initially matched the date.
    season_types = {row.season_type_id for row in seasons}
    season_codes = {row.season_type.code for row in seasons}
    bags = [row for row in bags if (row.season_type_id is None or row.season_type_id in season_types)
            and (not row.season_group or any(row.season_group.upper() in code.upper() for code in season_codes))]
    notes = list(RegulationNote.objects.filter(
        Q(land_type=land_type) | Q(land_type__isnull=True), species=species, is_active=True
    ).select_related("source").order_by("pk"))
    notes = [row for row in notes if year_label_matches(row.season_year, hunting_date, allow_blank=True)]

    sources, dates, limits, licenses, methods, matched = {}, [], [], [], [], []
    alerts = [REVIEW_NOTICE]
    if not seasons:
        alerts.append("No matching season information was found. This does not establish permission to hunt.")
    if is_private(land_type) and not selections["landowner_permission"]:
        alerts.append("Landowner permission was not confirmed in this search.")
    for season in seasons:
        sources[season.source_id] = season.source
        periods = applicable_periods(season, hunting_date)
        label = season.season_type.name
        if periods:
            dates.extend(f"{label}: {p.start_date.isoformat()} to {p.end_date.isoformat()}" for p in periods)
        else:
            dates.append(f"{label}: year-round label; explicit date bounds are not recorded")
            alerts.append("A year-round label is recorded without explicit date bounds. Confirm its applicability in the source.")
        category = season.harvest_category.name if season.harvest_category else "All recorded categories"
        for field, description in [("daily_bag_limit", "Daily"), ("possession_limit", "Possession"), ("annual_limit", "Annual")]:
            value = getattr(season, field)
            if value is not None:
                limits.append(f"{label} / {category} — {description}: {value}")
        for permit in season.permits.all():
            if permit.is_active:
                licenses.append(permit.name + (f": {permit.requirements}" if permit.requirements else ""))
                if permit.source_id:
                    sources[permit.source_id] = permit.source
        methods.extend(method.name + (f": {method.description}" if method.description else "") for method in season.legal_methods.all())
        if season.notes:
            alerts.append(season.notes)
        matched.append({
            "id": season.pk, "season_type": label, "season_type_code": season.season_type.code,
            "season_year": season.season_year, "zone": season.zone_id, "dmu": season.dmu_id,
            "regulatory_area": season.regulatory_area_id, "managed_area": season.managed_area_id,
            "periods": [{"start_date": p.start_date.isoformat(), "end_date": p.end_date.isoformat()} for p in periods],
            "source_id": season.source_id,
        })
    for bag in bags:
        sources[bag.source_id] = bag.source
        category = bag.harvest_category.name if bag.harvest_category else "All recorded categories"
        value = "Unlimited (as recorded)" if bag.is_unlimited else str(bag.limit) if bag.limit is not None else "Not recorded"
        limits.append(f"{category} — {bag.limit_type}: {value}" + (f". {bag.conditions}" if bag.conditions else ""))
    for note in notes:
        sources[note.source_id] = note.source
        alerts.append((f"{note.title}: " if note.title else "") + note.text)
    if not seasons:
        # Keep relevant references available without substituting a different season.
        for season in all_seasons:
            if year_label_matches(season.season_year, hunting_date) and all(
                getattr(season, field + "_id") in (None, selections[field].pk if selections.get(field) else None)
                for field in ["zone", "dmu", "regulatory_area", "managed_area"]
            ):
                sources[season.source_id] = season.source
    query = {"species": species.pk, "land_type": land_type.pk, "date": hunting_date.isoformat(),
             "landowner_permission": selections["landowner_permission"]}
    query.update({field: selections[field].pk if selections.get(field) else None
                  for field in ["zone", "dmu", "regulatory_area", "managed_area"]})
    return {
        **species_data(species), "landType": land_type.name,
        "dates": "\n".join(dict.fromkeys(dates)) or "Not recorded for the selected date.",
        "bag": "\n".join(dict.fromkeys(limits)) or "Bag limits are not recorded for these selections. Check the official source.",
        "licenses": "\n".join(dict.fromkeys(licenses)) or "License and permit requirements are not recorded in the matched season data. Check the official source.",
        "methods": "\n".join(dict.fromkeys(methods)) or "Allowed methods are not recorded in the matched season data. Check the official source.",
        "alerts": list(dict.fromkeys(alerts)), "sources": [source_data(sources[key]) for key in sorted(sources)],
        "verified": False, "matched_seasons": matched, "query": query,
        "status": "unverified" if seasons else "no_data",
    }


def search_records(selections):
    """Compatibility entry point that always uses the reviewed public engine."""
    from .engine import ComplianceEngine
    return ComplianceEngine(selections).search()
