"""Install source-checked additions as drafts; never inherit older approval."""
from copy import deepcopy

from django.db import transaction

from .approved_release import catalog_mapping, local_key, local_payload, read_approved_release
from .catalog_data import seed_catalog_details
from .models import RegulationDraft
from regulations.models import ManagedArea
from .starter import GENERAL, HOG, source
from .turkey_data import EXEMPTIONS, EXEMPTION_GUIDANCE, METHODS
from .expansion_metadata import EDITION


SAFETY = "https://myfwc.com/hunting/safety-education/"
NOTICES = "https://myfwc.com/recreation/notices/"
PYTHON_ORDER = "https://myfwc.com/media/31857/eo-23-16.pdf"


def stage_existing_review_updates():
    """Enrich only unchanged starter drafts, preserving edits and publications.

    The exact old approved payload is the comparison baseline. A teammate's
    newer working draft is never replaced, even if it has not been published.
    """
    release = read_approved_release()
    mappings = catalog_mapping(release)
    updated = preserved = 0
    for entry in release["drafts"]:
        baseline = local_payload(entry["payload"], mappings)
        # Public python keys include the mapped local land identifier.
        key = local_key(entry["key"], baseline["land_type_id"])
        draft = RegulationDraft.objects.get(key=key)
        if draft.payload.get("data_expansion_edition") == EDITION:
            continue
        if draft.payload != baseline:
            preserved += 1
            continue
        content = deepcopy(baseline)
        content["data_expansion_edition"] = EDITION
        additions = [source("FWC current area notices", NOTICES,
                            "Current closure directory checked; notices can change after this data check.")]
        content["alerts"].append("Check the linked FWC area notices for temporary closures; this local dataset does not poll live closures.")
        if key.startswith("deer-"):
            additions += [source("FWC conditional license exemptions", EXEMPTIONS,
                                 "Checked youth, resident senior and conditional exemptions; quota rules remain separate."),
                          source("FWC legal deer equipment", METHODS,
                                 "Checked broadhead, PCP, muzzleloader and prohibited ammunition requirements."),
                          source("FWC hunter safety", SAFETY,
                                 "Checked birth-date/age certification requirement and supervised deferral option."),
                          source("FWC general hunting rules", GENERAL,
                                 "Checked deer shooting hours, public-land orange and dog restrictions.")]
            content["alerts"] += [EXEMPTION_GUIDANCE,
                "Ordinary deer shooting hours are one-half hour before sunrise through one-half hour after sunset; specific area restrictions still apply.",
                "Arrows/bolts for deer require broadheads at least 7/8 inch wide. Deer PCP projectiles must meet the .30-caliber requirement; rimfire and nonexpanding full-metal-case ammunition are prohibited.",
                "Deer muzzleloaders firing one bullet must be at least .30 caliber; guns firing multiple balls must be 20 gauge or larger. Season-specific method limits still apply.",
                "Hunters age 16+ born on or after June 1, 1975 need hunter-safety certification before buying a hunting license, unless using a lawful supervised deferral."]
            if "corbett" in key:
                content["alerts"].append("Deer hunters and companions on public land need at least 500 square inches of fluorescent orange above the waist, except during archery-only season.")
            else:
                content["alerts"].append("Private-land deer dogs require FWC property registration, identification collars, remote tracking/correction and written landowner permission. Dogs cannot take deer during archery, crossbow or muzzleloading seasons.")
        elif key.startswith("hog-private"):
            additions += [source("FWC general hog exception", GENERAL,
                                 "Checked private-land day/night exception, no possession limit and landowner permission.")]
            content["alerts"].append("The private-land hog exception permits lawful day or night hunting with permission and has no possession limit. It does not apply on WMAs.")
        elif key.startswith("python-public"):
            additions += [source("FWC Executive Order 23-16", PYTHON_ORDER,
                                 "Checked year-round scope, traps/free-bolt prohibition and east/west US27 Fisheating Creek exceptions on page 2.")]
            fish = ManagedArea.objects.get(name="Fisheating Creek WMA")
            content["scopes"]["managed_area"] = [value for value in content["scopes"]["managed_area"] if value != fish.pk]
            content["alerts"].append("Fisheating Creek uses separate east/west US27 reviewed scopes because EO23-16 imposes special season and permit conditions there.")
            content["alerts"].append("EO23-16 prohibits traps and modified/free-bolt captive-bolt stunners. Firearms require authorization under the specific area rules; closed-to-public-access portions remain closed.")
        known = {row["url"] for row in content["sources"]}
        content["sources"].extend(row for row in additions if row["url"] not in known)
        draft.payload = content
        draft.full_clean()
        draft.save(update_fields=["payload", "updated_at"])
        updated += 1
    return {"existing_drafts_enriched": updated, "edited_drafts_preserved": preserved}


@transaction.atomic
def seed_data_expansion():
    from .turkey_data import seed_turkey_review_drafts
    from .wma_data import seed_wma_review_drafts
    from .extra_wma_data import seed_extra_wma_review_drafts
    from .python_area_data import seed_fisheating_python_drafts
    result = seed_catalog_details()
    result.update(stage_existing_review_updates())
    result["turkey_drafts_added"] = seed_turkey_review_drafts()
    result["wma_drafts_added"] = seed_wma_review_drafts()
    result["extra_wma_drafts_added"] = seed_extra_wma_review_drafts()
    result["python_exception_drafts_added"] = seed_fisheating_python_drafts()
    return result
