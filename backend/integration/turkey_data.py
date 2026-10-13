"""FWC-source-checked 2026–2027 turkey working data, never automatic approval.

Existing imported records and immutable owner-approved releases are preserved.
New records must pass the same administrator review boundary as other drafts.
"""
from copy import deepcopy

from django.db import transaction

from regulations.models import HuntingZone, LandType, RegulatoryArea, Species
from .models import RegulationDraft
from .expansion_metadata import EDITION
from .starter import payload, period, rule, source


CHECKED = "2026-10-12"
SEASONS = "https://myfwc.com/hunting/season-dates/"
LICENSES = "https://myfwc.com/license/recreational/hunting/"
EXEMPTIONS = "https://myfwc.com/license/recreational/do-i-need-one/"
GENERAL = "https://myfwc.com/hunting/regulations/general-information/"
METHODS = "https://myfwc.com/hunting/regulations/taking-game/"
HARVEST = "https://myfwc.com/hunting/deer/harvest-report/"
YOUTH = "https://myfwc.com/hunting/get-started/youth-turkey-hunting/"
PROFILE = "https://myfwc.com/wildlifehabitats/profiles/birds/game-birds/wild-turkeys/"
STRATEGY = "https://myfwc.com/hunting/turkey/get-started/"

# Outside the WMA system only. Endpoints after December belong to 2027.
FALL_DATES = {
    "A": {
        "ARCHERY": [("2026-08-01", "2026-08-30")],
        "CROSSBOW": [("2026-08-01", "2026-09-04")],
        "MUZZLELOADER": [("2026-09-05", "2026-09-18")],
        "FALL_TURKEY": [("2026-10-05", "2026-10-18"), ("2026-11-21", "2027-01-03")],
    },
    "B": {
        "ARCHERY": [("2026-10-17", "2026-11-15")],
        "CROSSBOW": [("2026-10-17", "2026-11-20")],
        "MUZZLELOADER": [("2026-11-21", "2026-12-04")],
        "FALL_TURKEY": [("2026-12-05", "2027-01-31")],
    },
    "C": {
        "ARCHERY": [("2026-09-19", "2026-10-18")],
        "CROSSBOW": [("2026-09-19", "2026-10-23")],
        "MUZZLELOADER": [("2026-10-24", "2026-11-06")],
        "FALL_TURKEY": [("2026-11-07", "2027-01-03")],
    },
    "D": {
        "ARCHERY": [("2026-10-24", "2026-11-25")],
        "CROSSBOW": [("2026-10-24", "2026-11-25"), ("2026-11-30", "2026-12-04")],
        "MUZZLELOADER": [("2026-12-05", "2026-12-11")],
        "FALL_TURKEY": [("2026-11-26", "2026-11-29"), ("2026-12-12", "2027-01-17")],
    },
}
SPRING_DATES = {
    "NORTH_SR70": {
        "SPRING_TURKEY": [("2027-03-20", "2027-04-25")],
        "YOUTH_TURKEY": [("2027-03-12", "2027-03-15")],
    },
    "SOUTH_SR70": {
        "SPRING_TURKEY": [("2027-03-06", "2027-04-11")],
        "YOUTH_TURKEY": [("2027-02-26", "2027-03-01")],
    },
}

NAMES = {
    "ARCHERY": "Turkey archery season", "CROSSBOW": "Turkey crossbow season",
    "MUZZLELOADER": "Turkey muzzleloading gun season", "FALL_TURKEY": "Fall turkey season",
    "SPRING_TURKEY": "Spring turkey season", "YOUTH_TURKEY": "Youth spring turkey hunt",
}
SEASON_PERMITS = {
    "ARCHERY": "Archery season permit", "CROSSBOW": "Crossbow season permit",
    "MUZZLELOADER": "Muzzleloading gun season permit",
}
GENERAL_METHODS = "Shotguns, rifles, handguns, muzzleloaders, crossbows, bows and lawful pre-charged pneumatic (PCP) air guns."
SEASON_METHODS = {
    "ARCHERY": "Bows only.",
    "CROSSBOW": "Crossbows, bows and airbows.",
    "MUZZLELOADER": "Muzzleloaders, crossbows, bows and airbows. Muzzleloading projectiles must load through the muzzle; ignition must use wheel lock, flintlock, percussion cap or centerfire primer (including 209). Powder may load at the breech.",
}
LICENSE_GUIDANCE = "Hunting license and Turkey Permit required unless individually exempt."
EXEMPTION_GUIDANCE = (
    "License/permit exemptions require the relevant proof and conditions: youth under 16; Florida residents age 65+; "
    "qualifying homestead hunting in the county of residence; Florida residents holding the qualifying disability license; "
    "qualifying resident military members home on leave for at most 30 days with orders; authorized military/disabled-veteran "
    "events; and qualifying licensed-preserve patrons. Check the official exemption page. An exemption does not change "
    "season dates, bag limits, access permission or harvest reporting."
)
EQUIPMENT_GUIDANCE = (
    "Turkey arrows/bolts need broadheads at least 7/8 inch wide. Turkey PCP equipment must meet FWC's minimum .20-caliber "
    "projectile requirement. Non-PCP air guns are prohibited for turkey. Centerfire semiautomatic rifle magazines cannot "
    "exceed five rounds; fully automatic firearms are prohibited."
)
RESTRICTIONS = (
    "Do not hunt turkeys with dogs, shoot a roosted turkey or hunt within 100 yards of a feeding station while feed is present. "
    "Live decoys, recorded game calls, artificial lights, traps and other prohibited methods are not authorized. "
    "Road rights-of-way, occupied premises, local discharge restrictions and private-property boundaries still apply."
)
REPORTING = (
    "Log every turkey before moving it. Report to FWC within 24 hours or before final processing, transfer to a processor/taxidermist "
    "or leaving Florida, whichever is first; retain the confirmation number. HuntIt's personal harvest record does not submit an FWC report."
)
TRANSPORT = (
    "Retain the head and beard, when applicable, and required hunter identification as evidence of legal harvest. "
    "After official reporting, transferred carcasses/parts require the hunter's name, address and harvest confirmation number; "
    "retain traceability and sex identification under FWC's processing/transport rules."
)

SPECIES_INFORMATION = {
    "scientific_name": "Meleagris gallopavo",
    "description": "Florida supports eastern and Osceola wild turkey subspecies. These large birds have long legs and broad tails; males commonly have a breast beard.",
    "habitat": "Open woodland, forest edges and clearings across suitable Florida habitat; Osceola turkeys occur in peninsular Florida.",
    "behavior": "Turkeys forage mainly on the ground, form flocks and roost in trees at night. They are wary and can fly rapidly over short distances.",
    "hunting_strategy": "Scout the hunting area beforehand, learn where turkeys travel and remain patient. Follow FWC's safe-hunting and calling guidance and positively identify the legal bird and a safe shooting direction.",
    "source_urls": [PROFILE, STRATEGY],
}


def turkey_sources():
    """Original concise evidence notes; no representation of human approval."""
    return [
        source("FWC 2026–2027 turkey seasons and limits", SEASONS, "Checked zone fall dates, SR70 spring dates, lawful categories, methods and combined season limits; WMA schedules excluded."),
        source("FWC hunting licenses and permits", LICENSES, "Checked hunting license, Turkey Permit and season-specific permits."),
        source("FWC license exemptions", EXEMPTIONS, "Checked age, residency and conditional exemptions; access and hunting restrictions remain separate."),
        source("FWC general hunting information", GENERAL, "Checked private-land permission, fall/spring shooting hours, carcass evidence and transfer labeling."),
        source("FWC legal and prohibited methods", METHODS, "Checked equipment thresholds, dogs/roost/feed restrictions and closed locations."),
        source("FWC deer and wild turkey harvest reporting", HARVEST, "Checked log-before-move duty, earliest reporting deadline and confirmation number."),
        source("FWC 2027 youth turkey hunts", YOUTH, "Checked all four days of each regional youth hunt, age/supervision, adult participation and youth season-limit counting."),
        source("FWC wild turkey species profile", PROFILE, "Checked Florida subspecies, appearance, habitat, flocking, feeding and tree roosts."),
        source("FWC how to hunt wild turkeys", STRATEGY, "Checked scouting and patience guidance; links provide safe calling and shooting instruction."),
    ]


def _turkey_rule(code, dates, *, spring=False):
    youth = code == "YOUTH_TURKEY"
    permits = ("No hunting license or permit required for youth 15 and under or a supervising adult who only supervises. "
               "Adults who call or otherwise participate need a hunting license and Turkey Permit; they may not shoot or shoot at turkey."
               if youth else LICENSE_GUIDANCE)
    if code in SEASON_PERMITS:
        permits += " " + SEASON_PERMITS[code] + " required unless exempt."
    season = "spring" if spring else "fall"
    item = rule(
        NAMES[code], code, "Gobblers and bearded turkeys only",
        [period(*bounds) for bounds in dates],
        f"Daily limit 2; possession and season limit 2 for all {season} seasons combined."
        + (" Youth-hunt harvest counts toward the same spring limit of 2." if youth else ""),
        permits, SEASON_METHODS.get(code, GENERAL_METHODS),
        [SEASONS, LICENSES, EXEMPTIONS, METHODS, GENERAL, HARVEST] + ([YOUTH] if youth else []),
        alerts=[
            "Shooting hours on private land: one-half hour before sunrise to "
            + ("sunset during spring (including youth) hunts." if spring else "one-half hour after sunset during fall hunts."),
            EQUIPMENT_GUIDANCE, RESTRICTIONS, REPORTING, TRANSPORT,
        ] + (["Only youth 15 and younger may harvest during this hunt, supervised by an adult age 18 or older."] if youth else []),
    )
    if youth:
        item["maximum_age"] = 15
    return item


@transaction.atomic
def seed_turkey_review_drafts():
    """Create six complete private turkey drafts; preserve user edits and reviews.

    Fall and spring coverage intentionally do not overlap. This prevents an
    irrelevant fall-zone selector being required for a spring SR70 search.
    """
    private = LandType.objects.get_or_create(name="Private Land")[0]
    species = Species.objects.filter(common_name__iexact="Wild Turkey").first()
    if species is None:
        species = Species.objects.create(common_name="Wild Turkey")
    zones = {code: HuntingZone.objects.get_or_create(code=code, defaults={"name": f"Zone {code}"})[0]
             for code in FALL_DATES}
    regions = {code: RegulatoryArea.objects.get_or_create(code=code, defaults={
        "name": ("North" if code == "NORTH_SR70" else "South") + " of State Road 70"})[0]
        for code in SPRING_DATES}
    created = 0
    schedules = [(f"fall-{code.lower()}", {"zone": zones[code].pk}, "zone", dates, False)
                 for code, dates in FALL_DATES.items()]
    schedules += [(f"spring-{code.lower()}", {"regulatory_area": regions[code].pk}, "regulatory_area", dates, True)
                  for code, dates in SPRING_DATES.items()]
    for suffix, scopes, selector, dates, spring in schedules:
        content = payload(
            species, private, [_turkey_rule(code, bounds, spring=spring) for code, bounds in dates.items()],
            turkey_sources(), scopes=scopes, required=[selector], permission=True,
            coverage=period("2027-02-01", "2027-06-30") if spring else period("2026-07-01", "2027-01-31"),
            alerts=["Private lands outside the WMA system only; obtain landowner permission. WMA dates, quotas and shooting hours require the specific area brochure.",
                    EXEMPTION_GUIDANCE, "The date bounds describe this edition's reviewed coverage; future seasons require new source review."],
        )
        content["species_information"] = deepcopy(SPECIES_INFORMATION)
        content["data_expansion_edition"] = EDITION
        obj, added = RegulationDraft.objects.get_or_create(
            key=f"turkey-private-{suffix}-2026-2027",
            defaults={"title": f"Wild turkey: private land, {suffix.replace('-', ' ')}, 2026–2027",
                      "species": species, "land_type": private, "payload": content},
        )
        if added:
            obj.full_clean()
            created += 1
    return created
