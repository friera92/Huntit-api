"""Install one previously human-approved release, never approve working imports.

Approval belongs to the exact hash-pinned bytes below. Changes to starter.py,
database drafts, import output or a different JSON file cannot inherit it.
"""
import hashlib
import json
from copy import deepcopy
from pathlib import Path

from django.core.management.base import CommandError
from django.db import transaction
from django.utils.dateparse import parse_datetime

from regulations.models import DeerManagementUnit, HuntingZone, LandType, ManagedArea, Species
from .models import (
    ApprovedReleaseInstallation, RegulationDraft, RegulatoryPublication,
    _REVIEW_TOKEN, validate_payload,
)


RELEASE_ID = "fwc-2026-10-12-v1"
RELEASE_PATH = Path(__file__).resolve().parent / "fixtures" / "approved_regulations_2026_10_12.json"
RELEASE_SHA256 = "305f768cda3fb21012ae4531cf1b5e85326287693e41f170cf73b1b409916896"
# Only descriptive approval wording changed; recognize the exact earlier release.
PREVIOUS_RELEASE_SHA256 = "ebbfdf107169475fa6b452dae65dbde437dabfe110f5709bdf1cd7e5422c9ebd"
PREVIOUS_APPROVAL_SHA256 = "28ca3e4e0d30a50be7d5521b7a22ab99d07ab63f7023a31ee7e6eb44c0cf6a91"
ACCEPTED_RELEASE_SHA256 = frozenset((RELEASE_SHA256, PREVIOUS_RELEASE_SHA256))


def read_approved_release():
    try:
        content = RELEASE_PATH.read_bytes()
    except OSError as exc:
        raise CommandError("The approved regulatory release file could not be read; no answers were installed.") from exc
    digest = hashlib.sha256(content).hexdigest()
    if digest != RELEASE_SHA256:
        raise CommandError("Approved release SHA-256 mismatch. Changed files require a new explicit human review; no answers were installed.")
    data = json.loads(content)
    if (data.get("release_id") != RELEASE_ID or data.get("format_version") != 1
            or data.get("approval", {}).get("type") != "human_source_review" or len(data.get("drafts", [])) != 18):
        raise CommandError("The approved release metadata is invalid; no answers were installed.")
    return data


def catalog_mapping(data):
    mappings = {}
    specifications = {"species": (Species, "common_name"), "land_type": (LandType, "name"),
                      "zone": (HuntingZone, "code"), "dmu": (DeerManagementUnit, "code"),
                      "managed_area": (ManagedArea, "name")}
    for kind, (model, identity) in specifications.items():
        mapping = {}
        for entry in data["catalog"][kind]:
            matches = list(model.objects.filter(**{identity: entry[identity]}))
            if len(matches) != 1:
                raise CommandError(f"Approved release catalog mismatch: {kind} {entry[identity]!r} must identify exactly one existing record. Nothing was published.")
            mapping[entry["id"]] = matches[0].pk
            if kind == "dmu" and matches[0].zone_id != mappings["zone"][entry["zone_id"]]:
                raise CommandError(f"Approved release catalog mismatch: DMU {entry[identity]} belongs to a different zone. Nothing was published.")
        mappings[kind] = mapping
    return mappings


def local_payload(frozen, mappings):
    payload = deepcopy(frozen)
    payload["species_id"] = mappings["species"][payload["species_id"]]
    payload["land_type_id"] = mappings["land_type"][payload["land_type_id"]]
    for scopes in [payload.get("scopes", {}), *(rule.get("scopes", {}) for rule in payload["rules"])]:
        for kind, value in scopes.items():
            scopes[kind] = [mappings[kind][item] for item in value] if isinstance(value, list) else mappings[kind][value]
    validate_payload(payload)
    return payload


def local_key(frozen_key, local_land_id):
    # Earlier starter keys include a local land-type PK. Keep those keys portable
    # while mapping their meaning by the frozen catalog's exact name.
    if frozen_key.startswith("python-public-"):
        return f"python-public-{local_land_id}-2026"
    if frozen_key.startswith("deer-corbett-"):
        return f"deer-corbett-{local_land_id}-2026-2027"
    return frozen_key


def matches_original_snapshot(actual, expected):
    """Compare regulatory content while allowing exact prior approval wording."""
    if actual == expected:
        return True
    metadata = actual.get("approved_release", {})
    approval = metadata.get("approval", {})
    digest = hashlib.sha256(json.dumps(
        approval, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
    ).encode("utf-8")).hexdigest()
    if (set(metadata) != {"release_id", "sha256", "approval"}
            or metadata.get("release_id") != RELEASE_ID
            or metadata.get("sha256") != PREVIOUS_RELEASE_SHA256
            or digest != PREVIOUS_APPROVAL_SHA256):
        return False
    normalized = deepcopy(actual)
    normalized["approved_release"] = deepcopy(expected["approved_release"])
    return normalized == expected


@transaction.atomic
def install_approved_release():
    data = read_approved_release()
    receipt = ApprovedReleaseInstallation.objects.filter(release_id=RELEASE_ID).first()
    if receipt:
        if receipt.sha256 not in ACCEPTED_RELEASE_SHA256:
            raise CommandError("Existing release receipt has a different digest; manual review is required.")
        return {"added": 0, "preserved": 0, "already_installed": True}
    mappings = catalog_mapping(data)
    added, preserved = 0, 0
    approval = data["approval"]
    approved_at = parse_datetime(approval["recorded_at"])
    for entry in data["drafts"]:
        payload = local_payload(entry["payload"], mappings)
        key = local_key(entry["key"], payload["land_type_id"])
        draft, created = RegulationDraft.objects.get_or_create(key=key, defaults={
            "title": entry["title"], "species_id": payload["species_id"],
            "land_type_id": payload["land_type_id"], "payload": payload,
        })
        if draft.publications.exists():
            # Includes withdrawn publications: setup must not republish them.
            preserved += 1
            continue
        if (draft.payload != payload or draft.title != entry["title"]
                or draft.species_id != payload["species_id"] or draft.land_type_id != payload["land_type_id"]):
            raise CommandError(f"Existing draft {key!r} differs from the approved release. It was preserved; nothing was published. Review it manually.")
        draft.full_clean()
        snapshot = deepcopy(payload)
        snapshot["title"] = entry["title"]
        snapshot["approved_release"] = {"release_id": RELEASE_ID, "sha256": RELEASE_SHA256,
                                         "approval": deepcopy(approval)}
        for source in snapshot["sources"]:
            source["last_verified_at"] = approved_at.isoformat()
        publication = RegulatoryPublication(
            draft=draft, revision=1, snapshot=snapshot, reviewed_by=None,
            reviewed_at=approved_at, is_current=True,
            review_notes=(f"Previously human-approved release {RELEASE_ID}; SHA-256 {RELEASE_SHA256}. "
                          f"Approval recorded {approval['recorded_at']}. Project owner stated: {approval['statement']!r}. "
                          "Official FWC sources were verified. No reviewer account or credentials are bundled. "
                          "Approval applies only to this frozen release; later imports and edits require a new administrator review."),
        )
        publication.save(_review_token=_REVIEW_TOKEN)
        added += 1
    ApprovedReleaseInstallation.objects.create(release_id=RELEASE_ID, sha256=RELEASE_SHA256,
        publications_added=added, existing_publications_preserved=preserved)
    return {"added": added, "preserved": preserved, "already_installed": False}
