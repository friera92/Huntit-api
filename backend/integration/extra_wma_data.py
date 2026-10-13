"""Dinner Island Ranch 2026-2027 source-checked working drafts.

The interactive official FWC brochure and hunt calendar were read on 2026-10-12.
This module adds drafts only. It never edits the original imported regulations,
changes an existing draft, or grants new content an earlier release's approval.
"""
from copy import deepcopy

from django.db import transaction

from regulations.models import LandType, ManagedArea, Species
from .models import RegulationDraft
from .expansion_metadata import EDITION
from .python_area_data import ORDER as PYTHON_ORDER
from .starter import HUMANE, LICENSE, PYTHON, payload, period, rule, source


AREA_NAME = "Dinner Island Ranch WMA"
BROCHURE = "https://app.myfwc.com/hgm/hgmsearch/wmad?brochureTitle=Dinner+Island+Ranch"
CALENDAR = "https://app.myfwc.com/hsc/wmahuntcalendar/?areaName=dinner+island+ranch"
HOG = "https://myfwc.com/hunting/wild-hog/"
TAKING_GAME = "https://myfwc.com/hunting/regulations/taking-game/"
COVERAGE = period("2026-07-01", "2027-06-30")

# Every endpoint is copied as a complete year-specific date, not calculated
# from the statewide hunting zone. The Caracara Unit is a different area.
SCHEDULE = {
    "ARCHERY": [("2026-08-07", "2026-08-10"), ("2026-08-14", "2026-08-17"),
                ("2026-08-21", "2026-08-24"), ("2026-08-28", "2026-08-31")],
    "MUZZLELOADER": [("2026-09-11", "2026-09-13")],
    "FAMILY": [("2026-09-19", "2026-09-20"), ("2026-10-17", "2026-10-18")],
    "GENERAL_GUN": [("2026-09-25", "2026-09-27"), ("2026-10-02", "2026-10-04"),
                    ("2026-10-09", "2026-10-11")],
    "SMALL_GAME": [("2026-10-19", "2027-02-20")],
    "YOUTH_TURKEY": [("2027-02-26", "2027-03-01")],
    "SPRING_TURKEY": [("2027-03-06", "2027-03-08"), ("2027-03-13", "2027-03-15"),
                      ("2027-04-03", "2027-04-05")],
}

ACCESS_ALERTS = [
    "Dinner Island Ranch coverage excludes the separately regulated Caracara Unit. Enter and exit at the designated entrance; posted closed areas remain closed.",
    "The 2026-2027 Attention Hunters notice says there is no operating check station and waives all check-station duties. Deer and turkey must still be logged before moving and officially reported within 24 hours. HuntIt does not submit the FWC report.",
    "Vehicles may use named and numbered roads only, except valid Alternative Mobility Permit allowances. Vehicles are prohibited from 1.5 hours after sunset until 1.5 hours before sunrise, except camping-permit holders and guests accessing their designated campsite.",
    "Airboats, ATVs, swamp buggies, tracked vehicles and unregistered motorcycles are prohibited, except quota hunters and their guest permit holders may use ATVs and swamp buggies on named/numbered roads during their permitted archery, muzzleloading gun, family or general gun hunt. This exception does not authorize off-road travel.",
    "Camping requires an FWC permit and is limited to designated campgrounds. Horses are prohibited during archery, muzzleloading gun, family, general gun and spring turkey seasons; otherwise use designated roads.",
    "On posted dove fields, hunting during dove season is limited to Saturdays; otherwise only hunting allowed by the applicable area season is authorized. Check the brochure map and current closures before selecting a hunting site.",
]
SAFETY_ALERTS = [
    "No hunting over bait, night gun hunting, fully automatic firearms or centerfire semiautomatic rifles with magazines holding more than 5 rounds. The brochure's ammunition, equipment and closed-area restrictions apply.",
    "Ordinary shooting hours are half an hour before sunrise through half an hour after sunset. Turkey shooting ends at sunset.",
    "Dogs may not hunt deer, wild hog or furbearers; leashed dogs may trail wounded game under the brochure's conditions. No dogs may pursue non-native reptiles.",
    "License/season-permit exemptions do not waive a quota permit marked no exemptions. Check hunter-safety requirements and individual exemptions in the full brochure.",
    "Nonresident hunters taking native game need the applicable annual hunting license unless exempt. A hunting license is not required when hunting wild hog or removing python within the stated exception.",
]
DEER_ALERTS = [
    "Antlered deer only: at least 3 points, each at least 1 inch, on one antler, or a main beam of at least 10 inches. Youth under 16 have the statewide one-deer annual antler-point exception; a 5-inch antler is still required. Antlerless deer are not authorized in these area seasons.",
    "Do not take spotted fawns or swimming deer. Deer hunters and companions need 500 square inches of fluorescent orange above the waist, except bow-and-arrow hunting during archery season.",
    "Deer must be logged before moving and reported to FWC within 24 hours, or before an earlier processing, transfer or out-of-state deadline. The shared quota bag is not a separate allowance for each guest.",
    "Deer muzzleloaders firing a single bullet must be at least .30 caliber; those firing 2 or more balls must be at least 20 gauge. Deer arrows and bolts require broadheads at least 7/8 inch wide. No rimfire or non-expanding full-metal-jacket ammunition for deer.",
]
FAMILY_ALERT = (
    "Family hunt: the quota holder must be at least 18 and directly supervise up to 2 youth ages 8-15. "
    "The adult may hunt only with at least one youth present. Guest hunting permits are not allowed for this hunt."
)
QUOTA_ALERT = (
    "Quota permits are nontransferable and require positive identification except for youth. "
    "Where a guest permit is allowed, one guest and the host must enter/exit together, share a street-legal vehicle "
    "and hunt with the host present. Deer and turkey limits are shared per quota permit."
)

ARCHERY = (
    "Bows only. Crossbows, airbows and draw-lock bows are prohibited except the brochure's "
    "Persons With Disabilities Crossbow Permit exception."
)
MUZZLELOADER = "Muzzleloading guns only for deer or hog; ordinary archery equipment is prohibited during this season."
GENERAL = (
    "Lawful shotguns, rifles, muzzleloading guns, pistols, airguns, bows and crossbows, subject to the area brochure. "
    "For deer, no rimfire or non-expanding full-metal-jacket ammunition; PCP airguns must propel a bolt, arrow or bullet of at least .30 caliber. "
    "Deer muzzleloaders require a single bullet at least .30 caliber, or at least 20 gauge when firing 2 or more balls."
)
TURKEY_METHODS = (
    "Bows, crossbows, PCP airguns propelling a bolt or arrow, or shotguns using No. 2 or smaller shot. "
    "Rifles, pistols and PCP airguns propelling bullets are prohibited for turkey. No shooting a turkey on its roost; "
    "shooting hours are half an hour before sunrise through sunset."
)
NO_HOG_BAG = "No bag limit or size restriction. Do not remove wild hogs alive."
DEER_BAG = (
    "1 antlered deer per quota permit (shared with any permitted guest). Statewide daily 2, possession 4 and annual 5 deer limits also apply."
)
FAMILY_BAG = "2 antlered deer per family quota permit, but no more than 1 per person; statewide daily, possession and annual limits still apply."
TURKEY_BAG = (
    "1 gobbler or bearded turkey per youth or spring turkey quota permit, shared with any permitted guest. "
    "Statewide spring daily 2, possession 2 and season 2 limits also apply; youth-weekend harvest counts toward the spring season limit."
)


def _periods(code):
    return [period(first, last) for first, last in SCHEDULE[code]]


def _permits(kind, code):
    if kind == "hog":
        text = "No hunting license is required for wild hog. Management area permit required unless exempt. "
    elif kind == "deer":
        text = "Hunting license, management area permit and deer permit required unless exempt. "
    else:
        text = "Hunting license, management area permit and turkey permit required unless exempt. "
    if code == "ARCHERY":
        text += "Archery season permit required unless exempt. "
    elif code == "MUZZLELOADER":
        text += "Muzzleloading gun season permit required unless exempt. "
    if code == "SMALL_GAME":
        return text + "No quota permit required for the small-game season."
    return text + "A quota permit for this area and hunt is required; no quota exemptions."


def _rules(kind):
    citations = [BROCHURE, CALENDAR, LICENSE] + ([HOG] if kind == "hog" else [TAKING_GAME])
    if kind in {"deer", "hog"}:
        result = []
        for code, label in [("ARCHERY", "archery"), ("MUZZLELOADER", "muzzleloading gun"),
                            ("FAMILY", "family hunt"), ("GENERAL_GUN", "general gun")]:
            methods = ARCHERY if code == "ARCHERY" else MUZZLELOADER if code == "MUZZLELOADER" else GENERAL
            if kind == "hog" and code not in {"ARCHERY", "MUZZLELOADER"}:
                methods = "Lawful shotguns, rifles, muzzleloading guns, pistols, airguns, bows and crossbows, subject to the area brochure. No dogs for wild hog."
            content = rule(
                f"Dinner Island Ranch {label}", code, "Antlered deer only" if kind == "deer" else "Wild hog, either sex",
                _periods(code), (FAMILY_BAG if code == "FAMILY" else DEER_BAG) if kind == "deer" else NO_HOG_BAG,
                _permits(kind, code), methods, citations,
                alerts=([*DEER_ALERTS] if kind == "deer" else []) + [QUOTA_ALERT] + ([FAMILY_ALERT] if code == "FAMILY" else []),
            )
            result.append(content)
        if kind == "hog":
            result.append(rule(
                "Dinner Island Ranch small-game season hog", "SMALL_GAME", "Wild hog, either sex", _periods("SMALL_GAME"),
                NO_HOG_BAG, _permits(kind, "SMALL_GAME"),
                "Lawful area methods, including centerfire rifles expressly permitted during this small-game season. No dogs for wild hog; no nighttime gun hunting.",
                citations,
            ))
            prohibited = rule(
                "Dinner Island Ranch spring/youth turkey restriction", "SPRING_HOG_PROHIBITION", "Wild hog prohibited",
                _periods("YOUTH_TURKEY") + _periods("SPRING_TURKEY"), "No wild hog harvest during youth or spring turkey hunts.",
                "A turkey quota permit does not authorize wild hog hunting.", "Wild hog hunting is prohibited during these turkey hunts.",
                [BROCHURE, CALENDAR],
            )
            prohibited["prohibited"] = True
            result.append(prohibited)
        return result
    if kind == "turkey":
        youth = rule(
            "Dinner Island Ranch youth turkey", "YOUTH_TURKEY", "Gobbler or bearded turkey; youth only",
            _periods("YOUTH_TURKEY"), TURKEY_BAG,
            "Eligible youth under 16 do not need a hunting license or season permits. A youth turkey quota permit is required, with no quota exemptions. Supervising adults participating in the hunt need the applicable licenses/permits unless exempt, and may not harvest turkey.",
            TURKEY_METHODS, citations,
            alerts=["Only youth under 16 may harvest during this hunt, under direct physical supervision of an adult at least 18. An adult may assist in the youth's presence but may not harvest.",
                    "Turkey arrows and bolts require broadheads at least 7/8 inch wide. The area's PCP bolt/arrow-only restriction still applies; statewide PCP bullet guidance does not authorize bullets here.", QUOTA_ALERT],
        )
        youth["maximum_age"] = 15
        return [youth, rule(
            "Dinner Island Ranch spring turkey", "SPRING_TURKEY", "Gobbler or bearded turkey only",
            _periods("SPRING_TURKEY"), TURKEY_BAG, _permits("turkey", "SPRING_TURKEY"),
            TURKEY_METHODS, citations, alerts=["Turkey arrows and bolts require broadheads at least 7/8 inch wide. The area's PCP bolt/arrow-only restriction still applies; statewide PCP bullet guidance does not authorize bullets here.", QUOTA_ALERT],
        )]
    # Preserve the brochure's two qualifications rather than interpreting an
    # unresolved spring-turkey interaction as a blanket firearm authorization.
    return [rule(
        "Dinner Island Ranch non-native reptile removal", "YEAR_ROUND", "Burmese python",
        [deepcopy(COVERAGE)], "No bag limit.",
        "No hunting license or removal permit is required for public python removal within FWC's listed area scope; access and vehicle/camping permits are separate.",
        "Non-firearm methods may be used year-round. Firearms may be used only during open area hunting seasons, with methods allowed for that season and the brochure's shooting restrictions. Follow FWC humane-removal training and the required two-step method; the first step alone is insufficient.",
        [BROCHURE, PYTHON, HUMANE, PYTHON_ORDER], alerts=[
            "EO23-16 prohibits traps and modified/free-bolt captive-bolt stunners; all other area access and equipment restrictions still apply.",
            "No dogs for non-native reptile removal. Humanely kill on site; members of the public may not remove live pythons. Florida anti-cruelty requirements apply.",
            "Firearm reptile removal is limited to half an hour before sunrise through half an hour after sunset and does not override a season's weapon or access restrictions.",
            "The spring turkey section prohibits hunting other animals, while the non-native reptile section qualifies firearm take by open seasons. This lookup does not establish a spring/youth-turkey firearm exception; confirm this interaction with FWC before using a firearm for python removal during those hunts.",
        ],
    )]


@transaction.atomic
def seed_extra_wma_review_drafts():
    """Add eight exact-area drafts without approval or overwriting team edits."""
    area = ManagedArea.objects.get_or_create(name=AREA_NAME, defaults={"area_type": "WMA"})[0]
    species = {
        "deer": Species.objects.get_or_create(common_name="White Tailed Deer", defaults={"scientific_name": "Odocoileus virginianus"})[0],
        "hog": Species.objects.get_or_create(common_name="Wild Hog", defaults={"scientific_name": "Sus scrofa"})[0],
        "turkey": Species.objects.get_or_create(common_name="Wild Turkey")[0],
        "python": Species.objects.get_or_create(common_name="Burmese Python", defaults={"scientific_name": "Python bivittatus"})[0],
    }
    sources = [
        source("FWC Executive Order 23-16", PYTHON_ORDER,
               "Page 2 checked: traps and modified/free-bolt captive-bolt stunners prohibited; firearms need specific area authorization."),
        source("FWC Dinner Island Ranch 2026-2027 area brochure", BROCHURE,
               "Read complete interactive brochure: season dates, antlered-only deer, quota/shared bags, turkey restrictions, hog methods, access and check-station waiver."),
        source("FWC Dinner Island Ranch 2026-2027 hunt calendar", CALENDAR,
               "Corroborated every archery, muzzleloading, family, general gun, small-game and youth/spring turkey endpoint; Caracara Unit excluded."),
        source("FWC hunting licenses and permits", LICENSE,
               "Species/season permits and individual exemptions are separate from no-exemption area quota permits."),
        source("FWC wild hog public-land guidance", HOG,
               "A hunting license is never required for wild hog; area/season/quota permits and area methods still apply."),
        source("FWC public python removal", PYTHON,
               "Dinner Island Ranch is on the named public-removal list; no license/removal permit/bag limit does not override area firearm or access restrictions."),
        source("FWC humane python removal", HUMANE,
               "Humane onsite two-step removal and public prohibition on live transport checked; follow training and property-specific firearm rules."),
        source("FWC taking game methods", TAKING_GAME,
               "Deer muzzleloader minimum .30-caliber single bullet/20-gauge multiple balls and deer/turkey 7/8-inch broadheads checked; area-specific stricter methods retained."),
    ]
    created = 0
    for land_name in ["Wildlife Management Area (WMA)", "Commission-Managed Land"]:
        land = LandType.objects.get_or_create(name=land_name)[0]
        for kind, animal in species.items():
            source_urls = ({BROCHURE, CALENDAR, PYTHON, HUMANE, PYTHON_ORDER} if kind == "python" else
                           {BROCHURE, CALENDAR, LICENSE} | ({HOG} if kind == "hog" else {TAKING_GAME}))
            content = payload(animal, land, _rules(kind), deepcopy([row for row in sources if row["url"] in source_urls]),
                              coverage=deepcopy(COVERAGE), scopes={"managed_area": area.pk},
                              required=["managed_area"], alerts=[*ACCESS_ALERTS, *SAFETY_ALERTS] + (
                                  ["Turkey hunting is authorized only during the listed youth/spring hunts; no fall turkey season is authorized here.",
                                   "Log turkey before moving and officially report to FWC within 24 hours or before an earlier processing, transfer or out-of-state deadline."]
                                  if kind == "turkey" else []))
            content["data_expansion_edition"] = EDITION
            draft, added = RegulationDraft.objects.get_or_create(
                key=f"{kind}-dinner-island-{land.pk}-2026-2027",
                defaults={"title": f"{animal.common_name}: Dinner Island Ranch / {land.name}, 2026-2027",
                          "species": animal, "land_type": land, "payload": content},
            )
            if added:
                draft.full_clean()
                created += 1
    return created
