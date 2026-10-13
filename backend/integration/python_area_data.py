"""Fisheating Creek's explicit east/west public-python exceptions.

Source-checked working drafts only. EO 23-16 and the 2026-2027 FWC brochure
do not permit the broad year-round/no-permit summary east of US Highway 27.
"""
from copy import deepcopy

from django.db import transaction

from regulations.models import LandType, ManagedArea, RegulatoryArea, Species
from .models import RegulationDraft
from .expansion_metadata import EDITION
from .starter import HUMANE, PYTHON, payload, period, rule, source


AREA_NAME = "Fisheating Creek WMA"
BROCHURE = "https://app.myfwc.com/hgm/hgmsearch/wmad?brochureTitle=Fisheating+Creek"
CALENDAR = "https://app.myfwc.com/hsc/wmahuntcalendar/?areaName=fisheating+creek"
ORDER = "https://myfwc.com/media/31857/eo-23-16.pdf"
COVERAGE = period("2026-07-01", "2027-06-30")
REGIONS = {
    "west": ("FISHEATING_WEST_US27", "Fisheating Creek west of U.S. Highway 27"),
    "east": ("FISHEATING_EAST_US27", "Fisheating Creek east of U.S. Highway 27: special-opportunity turkey area only"),
}
EAST_PERIODS = [period("2027-03-06", "2027-03-12"), period("2027-03-20", "2027-03-26")]
SHARED_ALERTS = [
    "Select the correct side of U.S. Highway 27 and confirm the exact hunting parcel on the official brochure map. Posted closed areas and access restrictions remain controlling.",
    "EO 23-16 prohibits traps and modified or free-bolt captive-bolt stunners on these public areas. It does not authorize entry onto private property without permission.",
    "No live python may be removed. Humanely kill on site under Florida anti-cruelty law and FWC training; the required second step must prevent recovery after immediate loss of consciousness.",
    "Dogs may not be used for non-native reptile removal. Reptile shooting hours are half an hour before sunrise through half an hour after sunset, subject to area access and firearm restrictions.",
    "Python removal does not authorize deer, hog or turkey hunting, replace a permit required for another activity, or override closures. Check current FWC notices and the full brochure.",
]


def _west_rules():
    return [rule(
        "Fisheating Creek west year-round limited-equipment removal", "YEAR_ROUND", "Burmese python west of U.S. Highway 27",
        [deepcopy(COVERAGE)], "No bag limit.",
        "No hunting license or management area permit required for year-round removal without a gun. A management area permit is required when using a gun west of U.S. Highway 27; other access and season restrictions still apply.",
        "Year-round removal uses lawful humane methods other than firearms, airguns, bows or crossbows. Firearms, airguns, bows and crossbows may be used only during open brochure hunting seasons and only as allowed by the particular season. This year-round rule does not authorize those weapons outside an open hunt.",
        [BROCHURE, ORDER, PYTHON, HUMANE], alerts=[
            "The west-side year-round exception is narrower than 'non-firearm': it also excludes airguns, bows and crossbows outside open hunting seasons.",
            "When using any seasonal hunting equipment, confirm its lawful season, method, access conditions and any required hunt permit in the official brochure; the year-round limited-equipment rule is not a weapon-season authorization.",
            "A west-side gun removal requires a management area permit under EO 23-16 even though ordinary public python removal generally does not. The east-side special-opportunity permit is a separate condition.",
        ],
    )]


def _east_rules():
    return [rule(
        "Fisheating Creek east special-opportunity reptile removal", "SPECIAL_OPPORTUNITY_SPRING_TURKEY", "Burmese python in the east-side special-opportunity spring turkey area only",
        deepcopy(EAST_PERIODS), "No python bag limit; turkey quota/bag limits do not authorize a separate turkey harvest.",
        "A valid Fisheating Creek Special-Opportunity Spring Turkey Permit for the selected hunt is required for python removal, including removal without a firearm. The EO does not require a separate hunting license for reptile take; turkey hunting has its own license and permit requirements.",
        "Only methods allowed for the special-opportunity spring turkey season: bows, crossbows, PCP airguns propelling a bolt or arrow, and shotguns using No. 2 or smaller shot, subject to brochure conditions and humane killing rules. Rifles, pistols and PCP bullets are not authorized by this season's methods.",
        [BROCHURE, CALENDAR, ORDER, PYTHON, HUMANE], alerts=[
            "East of U.S. Highway 27, reptiles may be taken only inside the designated Special-Opportunity Spring Turkey Area, during March 6-12 or March 20-26, 2027, by holders of the valid special-opportunity permit. There is no year-round east-side removal exception.",
            "The brochure expressly authorizes the east-side reptile opportunity under the special-opportunity conditions; it is not an inference from general turkey dates or another WMA's year-round rules.",
            "Turkey shooting on this area has an earlier 1 p.m. cutoff; do not apply the reptile shooting-hours provision to turkey. Area access and permit conditions can further limit the reptile opportunity.",
        ],
    )]


@transaction.atomic
def seed_fisheating_python_drafts():
    """Add four exact-location drafts; preserve all existing draft/publication data."""
    area = ManagedArea.objects.get_or_create(name=AREA_NAME, defaults={"area_type": "WMA"})[0]
    animal = Species.objects.get_or_create(common_name="Burmese Python", defaults={"scientific_name": "Python bivittatus"})[0]
    regions = {key: RegulatoryArea.objects.get_or_create(code=code, defaults={
        "name": name, "description": "Fisheating Creek public python scope under EO 23-16; confirm exact boundaries in the official area brochure.",
        "map_url": BROCHURE,
    })[0] for key, (code, name) in REGIONS.items()}
    sources = [
        source("FWC EO 23-16 public non-native reptile exceptions", ORDER,
               "Page 2 checked: west gun/management-area exception, east special-opportunity season/permit restriction, traps and captive-bolt restrictions."),
        source("FWC Fisheating Creek 2026-2027 area brochure", BROCHURE,
               "Interactive 2026-2027 reptile section checked: west year-round excludes firearms/airguns/bows/crossbows, east special-opportunity conditions, methods, hours and no dogs/live removal."),
        source("FWC Fisheating Creek 2026-2027 hunt calendar", CALENDAR,
               "Confirmed east special-opportunity spring turkey periods March 6-12 and March 20-26, 2027, distinct from the west-side spring turkey hunts."),
        source("FWC public python removal", PYTHON,
               "Listed-area opportunity and no bag limit are qualified by EO 23-16 and the specific area rules."),
        source("FWC humane python killing guidance", HUMANE,
               "Required humane onsite two-step killing; public live transport is prohibited and equipment must satisfy the area order."),
    ]
    created = 0
    for land_name in ["Wildlife Management Area (WMA)", "Commission-Managed Land"]:
        land = LandType.objects.get_or_create(name=land_name)[0]
        for side, region in regions.items():
            content = payload(animal, land, _west_rules() if side == "west" else _east_rules(), deepcopy(sources),
                              coverage=deepcopy(COVERAGE), scopes={"managed_area": area.pk, "regulatory_area": region.pk},
                              required=["managed_area", "regulatory_area"], alerts=SHARED_ALERTS)
            content["data_expansion_edition"] = EDITION
            draft, added = RegulationDraft.objects.get_or_create(
                key=f"python-fisheating-{side}-{land.pk}-2026-2027",
                defaults={"title": f"Burmese python: Fisheating Creek {side} of US27 / {land.name}, 2026-2027",
                          "species": animal, "land_type": land, "payload": content},
            )
            if added:
                draft.full_clean()
                created += 1
    return created
