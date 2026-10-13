"""Install the exact data expansion explicitly source-reviewed by the owner.

The approval belongs to a pinned frozen review pack, never mutable factories,
working drafts or later imports. Earlier publications remain immutable history.
"""
import hashlib
import json
import re
from copy import deepcopy
from pathlib import Path

from django.core.management.base import CommandError
from django.db import transaction
from django.db.models import Max
from django.utils.dateparse import parse_datetime

from regulations.models import RegulatoryArea
from .approved_release import (
    RELEASE_ID as ORIGINAL_RELEASE_ID, RELEASE_SHA256 as ORIGINAL_RELEASE_SHA256,
    catalog_mapping as original_catalog_mapping, local_key as original_local_key,
    local_payload, matches_original_snapshot, read_approved_release,
)
from .expansion_metadata import EDITION
from .models import ApprovedReleaseInstallation, RegulationDraft, RegulatoryPublication, _REVIEW_TOKEN


RELEASE_ID = "fwc-data-expansion-2026-10-12-v1-approved"
RELEASE_PATH = Path(__file__).resolve().parent / "fixtures" / "approved_data_expansion_2026_10_12.json"
RELEASE_SHA256 = "79f6028abb74d8c7a2eeccad3509ffcdd783141218ca72cf19990b8dd7c021cf"
REVIEW_SHA256 = "f54de4a3edbf240c5c20f8f6fc88fcb054dc64053dc227b544d2fc48d239374c"


def read_approved_expansion():
    try:
        raw = RELEASE_PATH.read_bytes()
    except OSError as exc:
        raise CommandError("The approved expansion could not be read; nothing was published.") from exc
    if hashlib.sha256(raw).hexdigest() != RELEASE_SHA256:
        raise CommandError("Approved expansion SHA-256 mismatch. Changed content requires a new human review; nothing was published.")
    data = json.loads(raw)
    review = data.get("review", {})
    reviewed_bytes = (json.dumps(review, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
    if (data.get("format_version") != 1 or data.get("release_id") != RELEASE_ID
            or data.get("approved_review_sha256") != REVIEW_SHA256
            or hashlib.sha256(reviewed_bytes).hexdigest() != REVIEW_SHA256
            or data.get("approval", {}).get("type") != "human_source_review"
            or data["approval"].get("statement") != "Sources checked — approve local publication"
            or review.get("edition") != EDITION or len(review.get("drafts", [])) != 58):
        raise CommandError("Approved expansion metadata is invalid; nothing was published.")
    return data


def catalog_mapping(data):
    catalog = data["review"]["catalog"]
    zones = {name: int(key) for key, name in catalog["zone"].items()}
    converted = {"catalog": {
        "species": catalog["species"], "land_type": catalog["land_types"],
        "zone": [{"id": int(key), "code": name} for key, name in catalog["zone"].items()],
        "dmu": [{"id": int(key), "code": name, "zone_id": zones[name[0]]}
                for key, name in catalog["dmu"].items()],
        "managed_area": [{"id": int(key), "name": name} for key, name in catalog["managed_area"].items()],
    }}
    mappings = original_catalog_mapping(converted)
    mappings["regulatory_area"] = {}
    for key, name in catalog["regulatory_area"].items():
        matches = list(RegulatoryArea.objects.filter(name=name))
        if len(matches) != 1:
            raise CommandError(f"Approved expansion catalog mismatch: regulatory area {name!r} must identify exactly one record. Nothing was published.")
        mappings["regulatory_area"][int(key)] = matches[0].pk
    return mappings


def local_key(frozen_key, frozen_land_id, local_land_id):
    if frozen_key.startswith(("python-public-", "deer-corbett-")):
        return original_local_key(frozen_key, local_land_id)
    match = re.fullmatch(
        r"((?:hog|deer|turkey|python)-(?:corbett|holey-land|rotenberger|dinner-island|fisheating-(?:east|west)))-(\d+)(-2026-2027(?:-expanded)?)",
        frozen_key,
    )
    if match:
        if int(match[2]) != frozen_land_id:
            raise CommandError("Frozen expansion key has an inconsistent land identity; nothing was published.")
        return f"{match[1]}-{local_land_id}{match[3]}"
    return frozen_key


def original_snapshots():
    data = read_approved_release()
    mappings = original_catalog_mapping(data)
    checked = parse_datetime(data["approval"]["recorded_at"])
    snapshots = {}
    for entry in data["drafts"]:
        content = local_payload(entry["payload"], mappings)
        content["title"] = entry["title"]
        content["approved_release"] = {"release_id": ORIGINAL_RELEASE_ID, "sha256": ORIGINAL_RELEASE_SHA256,
                                       "approval": deepcopy(data["approval"])}
        for source in content["sources"]:
            source["last_verified_at"] = checked.isoformat()
        key = original_local_key(entry["key"], content["land_type_id"])
        snapshots[key] = content
    return snapshots


@transaction.atomic
def install_approved_expansion():
    data = read_approved_expansion()
    receipt = ApprovedReleaseInstallation.objects.filter(release_id=RELEASE_ID).first()
    if receipt:
        if receipt.sha256 != RELEASE_SHA256:
            raise CommandError("Expansion receipt digest differs; manual reconciliation is required.")
        return {"added": 0, "preserved": 0, "already_installed": True}
    mappings = catalog_mapping(data)
    baseline = original_snapshots()
    planned = []
    # Preflight the complete release before changing any current answer.
    for entry in data["review"]["drafts"]:
        content = local_payload(entry["payload"], mappings)
        key = local_key(entry["key"], entry["payload"]["land_type_id"], content["land_type_id"])
        draft = RegulationDraft.objects.select_for_update().filter(key=key).first()
        histories = list(draft.publications.order_by("revision")) if draft else []
        current = next((row for row in histories if row.is_current), None)
        already_seen = any(row.snapshot.get("approved_expansion", {}).get("release_id") == RELEASE_ID for row in histories)
        preserve = already_seen or (bool(histories) and (current is None or key not in baseline))
        if current and key in baseline and not already_seen:
            if current.snapshot.get("approved_release", {}).get("release_id") == ORIGINAL_RELEASE_ID:
                if not matches_original_snapshot(current.snapshot, baseline[key]):
                    raise CommandError(f"Original publication {key!r} differs from its frozen release; nothing was published.")
            else:
                preserve = True  # A separately reviewed later answer takes precedence.
        if draft and not preserve and (draft.payload != content or draft.title != entry["title"]
                or draft.species_id != content["species_id"] or draft.land_type_id != content["land_type_id"]):
            raise CommandError(f"Existing draft {key!r} differs from the owner-approved expansion. It was preserved; nothing was published. Review the conflict manually.")
        planned.append({"key": key, "entry": entry, "content": content, "draft": draft, "preserve": preserve})

    # Keep broad Fisheating exclusions and four precise replacements together.
    fish_group = [row for row in planned if row["key"].startswith(("python-public-", "python-fisheating-"))]
    if any(row["preserve"] for row in fish_group):
        for row in fish_group:
            row["preserve"] = True
    added = preserved = 0
    approved_at = parse_datetime(data["approval"]["recorded_at"])
    for action in planned:
        if action["preserve"]:
            preserved += 1
            continue
        entry, content = action["entry"], action["content"]
        draft = action["draft"]
        if draft is None:
            draft = RegulationDraft.objects.create(key=action["key"], title=entry["title"],
                species_id=content["species_id"], land_type_id=content["land_type_id"], payload=content)
        draft.full_clean()
        revision = (draft.publications.aggregate(last=Max("revision"))["last"] or 0) + 1
        draft.publications.filter(is_current=True).update(is_current=False)
        snapshot = deepcopy(content)
        snapshot["title"] = entry["title"]
        snapshot["approved_expansion"] = {"release_id": RELEASE_ID, "sha256": RELEASE_SHA256,
            "approved_review_sha256": REVIEW_SHA256, "approval": deepcopy(data["approval"])}
        for source in snapshot["sources"]:
            source["last_verified_at"] = approved_at.isoformat()
        RegulatoryPublication(
            draft=draft, revision=revision, snapshot=snapshot, reviewed_by=None, reviewed_at=approved_at,
            review_notes=(f"Owner source-reviewed expansion {RELEASE_ID}; release SHA-256 {RELEASE_SHA256}; "
                          f"exact reviewed pack SHA-256 {REVIEW_SHA256}. Approval recorded {approved_at.isoformat()}. "
                          f"Owner stated: {data['approval']['statement']!r}. Only the frozen reviewed content is approved; "
                          "later edits require new review. No reviewer account is bundled."),
            is_current=True,
        ).save(_review_token=_REVIEW_TOKEN)
        added += 1
    ApprovedReleaseInstallation.objects.create(release_id=RELEASE_ID, sha256=RELEASE_SHA256,
        publications_added=added, existing_publications_preserved=preserved)
    return {"added": added, "preserved": preserved, "already_installed": False}
