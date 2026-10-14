"""Install the exact teammate information approved by the project owner.

The approval records the project owner's verification confirmation.
Future imports cannot inherit it.
"""
import hashlib
import json
from collections import Counter
from copy import deepcopy
from datetime import date
from pathlib import Path
from urllib.parse import unquote_plus, urlparse, urlsplit, urlunsplit

from django.core.management.base import CommandError
from django.db import transaction
from django.utils.dateparse import parse_datetime

from regulations.models import (
    DeerManagementUnit, HuntingZone, LandType, ManagedArea, RegulatoryArea, Species,
)
from .models import ApprovedImportedPublication, ApprovedReleaseInstallation, _REVIEW_TOKEN


LEGACY_RELEASE_ID = "teammate-information-2026-10-12-v1"
LEGACY_RELEASE_PATH = Path(__file__).resolve().parent / "fixtures" / "approved_teammate_information_2026_10_12.json"
LEGACY_RELEASE_SHA256 = "4a4eb659836e6677df7b4bc47389b9a15c25f3e42f1c58b8edeb37a7150fb7f6"
# Distribution-only wording and map-link cleanup does not grant a new data approval.
# Keep the previously approved digest readable without rewriting immutable history.
PREVIOUS_LEGACY_RELEASE_SHA256 = "8d9272e23308806c2eb50b7383c3738f44e468da2cd48260c19133b386fa2f85"
PREVIOUS_CLEANED_LEGACY_RELEASE_SHA256 = "bb72d9cc5dd9690ca7596903232d4da153ef2581513aeed2f8b05dfc30eaca4a"
ACCEPTED_LEGACY_RELEASE_SHA256 = frozenset((
    LEGACY_RELEASE_SHA256, PREVIOUS_LEGACY_RELEASE_SHA256, PREVIOUS_CLEANED_LEGACY_RELEASE_SHA256,
))
EXPECTED_COUNTS = {"species": 4, "huntingzone": 4, "landtype": 3, "regulatoryarea": 2,
                   "seasontype": 10, "source": 3, "managedarea": 32, "licensepermit": 6,
                   "legalmethod": 13, "deermanagementunit": 12, "harvestcategory": 4,
                   "huntingseason": 102, "seasonperiod": 78, "baglimitrule": 14,
                   "regulationnote": 5}
SELECTOR_MODELS = {"species": (Species, "common_name"), "landtype": (LandType, "name"),
                   "huntingzone": (HuntingZone, "code"), "regulatoryarea": (RegulatoryArea, "code"),
                   "managedarea": (ManagedArea, "name"), "deermanagementunit": (DeerManagementUnit, "code")}
SELECTOR_FIELDS = {"species": "species", "land_type": "landtype", "zone": "huntingzone",
                   "regulatory_area": "regulatoryarea", "managed_area": "managedarea",
                   "dmu": "deermanagementunit"}


class LegacyCatalogMissingError(CommandError):
    """A pre-existing partial catalog lacks an approved search identity."""


def _clean_zone_map_url(value):
    """Remove attribution from the known official map, retaining other URL bytes."""
    parsed = urlsplit(value)
    if (parsed.scheme != "https" or parsed.netloc.lower() != "myfwc.com"
            or parsed.path != "/hunting/season-dates/zone-map/"):
        return value
    parts = parsed.query.split("&")
    retained = [part for part in parts if unquote_plus(part.partition("=")[0]) != "utm_source"]
    if retained == parts:
        return value
    return urlunsplit(parsed._replace(query="&".join(retained)))


def read_approved_legacy_release():
    try:
        content = LEGACY_RELEASE_PATH.read_bytes()
    except OSError as exc:
        raise CommandError("The approved teammate information file could not be read.") from exc
    if hashlib.sha256(content).hexdigest() != LEGACY_RELEASE_SHA256:
        raise CommandError("Approved teammate information SHA-256 mismatch. Changed content needs new human approval.")
    data = json.loads(content)
    if (data.get("release_id") != LEGACY_RELEASE_ID or data.get("format_version") != 1
            or data.get("approval", {}).get("type") != "project_owner_verification_confirmation"):
        raise CommandError("Approved teammate information metadata is invalid.")
    records = data.get("original_fixture")
    if not isinstance(records, list) or any(not isinstance(row, dict) for row in records):
        raise CommandError("Approved teammate information must contain the original fixture records.")
    counts = Counter(row.get("model", "").removeprefix("regulations.") for row in records)
    if dict(counts) != EXPECTED_COUNTS:
        raise CommandError("Approved teammate information record counts do not match the reviewed release.")
    indexed = {}
    for row in records:
        kind = row["model"].removeprefix("regulations.")
        if (row["model"] != "regulations." + kind or type(row.get("pk")) is not int
                or not isinstance(row.get("fields"), dict)):
            raise CommandError("Invalid record in approved teammate information.")
        key = (kind, row["pk"])
        if key in indexed:
            raise CommandError("Duplicate record identity in approved teammate information.")
        indexed[key] = row["fields"]
    relation_fields = {**SELECTOR_FIELDS, "season_type": "seasontype", "source": "source",
                       "harvest_category": "harvestcategory", "season": "huntingseason"}
    for (kind, _), fields in indexed.items():
        for field, target in relation_fields.items():
            if fields.get(field) is not None and (target, fields[field]) not in indexed:
                raise CommandError(f"Invalid frozen {field} reference in {kind}.")
        for field, target in [("permits", "licensepermit"), ("legal_methods", "legalmethod")]:
            if any((target, value) not in indexed for value in fields.get(field, [])):
                raise CommandError(f"Invalid frozen {field} reference in {kind}.")
        if kind == "seasonperiod":
            first, last = date.fromisoformat(fields["start_date"]), date.fromisoformat(fields["end_date"])
            if first > last:
                raise CommandError("A frozen season period has reversed date bounds.")
        if kind == "source":
            parsed = urlparse(fields["url"])
            if parsed.scheme != "https" or parsed.hostname not in ("myfwc.com", "app.myfwc.com"):
                raise CommandError("Approved teammate source does not use an official FWC URL.")
    return data


def mapped_legacy_snapshot(data):
    """Map public selector IDs; all other joins remain inside this frozen copy."""
    records = {kind: [] for kind in EXPECTED_COUNTS}
    for original in data["original_fixture"]:
        records[original["model"].removeprefix("regulations.")].append(
            {"id": original["pk"], **deepcopy(original["fields"])})
    mappings = {}
    for kind, (model, identity) in SELECTOR_MODELS.items():
        mapping = {}
        for row in records[kind]:
            matches = list(model.objects.filter(**{identity: row[identity]}))
            if not matches:
                raise LegacyCatalogMissingError(f"Approved teammate catalog mismatch: {kind} {row[identity]!r} is missing locally.")
            if len(matches) != 1:
                raise CommandError(f"Approved teammate catalog mismatch: {kind} {row[identity]!r} must identify exactly one local record.")
            mapping[row["id"]] = matches[0].pk
            if kind == "deermanagementunit" and matches[0].zone_id != mappings["huntingzone"][row["zone"]]:
                raise CommandError(f"Approved teammate catalog mismatch: DMU {row[identity]} belongs to a different zone.")
        mappings[kind] = mapping
    for kind, rows in records.items():
        for row in rows:
            if kind in mappings:
                row["id"] = mappings[kind][row["id"]]
            for field, target in SELECTOR_FIELDS.items():
                if row.get(field) is not None:
                    row[field] = mappings[target][row[field]]
    return {"version": 1, "release_id": LEGACY_RELEASE_ID, "sha256": LEGACY_RELEASE_SHA256,
            "approval": deepcopy(data["approval"]),
            "distribution_cleanup": deepcopy(data["distribution_cleanup"]),
            "original_fixture_sha256": data["original_fixture_sha256"], "records": records}


@transaction.atomic
def install_approved_legacy_release():
    data = read_approved_legacy_release()
    receipt = ApprovedReleaseInstallation.objects.filter(release_id=LEGACY_RELEASE_ID).first()
    if receipt:
        if receipt.sha256 not in ACCEPTED_LEGACY_RELEASE_SHA256:
            raise CommandError("Existing teammate approval receipt has a different digest; manual review is required.")
        return {"added": 0, "already_installed": True}
    existing = ApprovedImportedPublication.objects.filter(release_id=LEGACY_RELEASE_ID).first()
    if existing:
        if existing.sha256 not in ACCEPTED_LEGACY_RELEASE_SHA256:
            raise CommandError("Existing teammate publication has a different digest; manual review is required.")
        added = 0  # Includes a withdrawn snapshot: setup must not restore it.
    else:
        snapshot = mapped_legacy_snapshot(data)
        publication = ApprovedImportedPublication(
            release_id=LEGACY_RELEASE_ID, sha256=LEGACY_RELEASE_SHA256, snapshot=snapshot,
            reviewed_at=parse_datetime(data["approval"]["recorded_at"]),
            review_notes=(f"Project owner confirmed verification of all existing project information and authorized its inclusion. "
                          f"Project owner stated: {data['approval']['statement']!r}. "
                          f"Approval recorded {data['approval']['recorded_at']}; release {LEGACY_RELEASE_ID}; "
                          f"SHA-256 {LEGACY_RELEASE_SHA256}. Verification is recorded in the original approval. "
                          "Original dates and unknown fields are preserved; only nonregulatory map-link tracking was removed "
                          "at the project owner's request. Future regulatory edits require new review."),
        )
        publication.save(_review_token=_REVIEW_TOKEN)
        added = 1
    ApprovedReleaseInstallation.objects.create(release_id=LEGACY_RELEASE_ID,
        sha256=existing.sha256 if existing else LEGACY_RELEASE_SHA256,
        publications_added=added, existing_publications_preserved=1 - added)
    return {"added": added, "already_installed": False}


def current_approved_legacy_snapshot():
    """Return approved data with clean map links, never mutate frozen history."""
    publication = ApprovedImportedPublication.objects.filter(
        release_id=LEGACY_RELEASE_ID, sha256__in=ACCEPTED_LEGACY_RELEASE_SHA256, is_current=True).first()
    if not publication:
        return None
    snapshot = deepcopy(publication.snapshot)
    for row in snapshot["records"]["huntingzone"]:
        row["map_url"] = _clean_zone_map_url(row["map_url"])
    return snapshot
