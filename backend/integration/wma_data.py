"""Additional 2026-2027 FWC area drafts, never automatic publications.

The official interactive brochures were read on 2026-10-12. Catalog identities
are reused; imported rows and previously reviewed snapshots are not edited.
"""
from copy import deepcopy

from regulations.models import LandType, ManagedArea, Species
from .models import RegulationDraft
from .expansion_metadata import EDITION
from .starter import LICENSE, PYTHON, HUMANE, payload, period, rule, source


COVERAGE = period("2026-07-01", "2027-06-30")
PYTHON_ORDER = "https://myfwc.com/media/31857/eo-23-16.pdf"
TAKING_GAME = "https://myfwc.com/hunting/regulations/taking-game/"
BROCHURES = {
    "corbett": "https://app.myfwc.com/hgm/hgmsearch/wmad?brochureTitle=J.W.+Corbett",
    "holey-land": "https://app.myfwc.com/hgm/hgmsearch/wmad?brochureTitle=Holey+Land",
    "rotenberger": "https://app.myfwc.com/hgm/hgmsearch/wmad?brochureTitle=Rotenberger",
}
AREA_NAMES = {"corbett": "J. W. Corbett WMA", "holey-land": "Holey Land WMA",
              "rotenberger": "Rotenberger WMA"}
NO_HOG_BAG = "No bag limit or size restriction. Wild hogs may not be removed alive."
DEER_LIMIT = ("Area season limit 1 antlered deer during archery, muzzleloading gun and general gun-walk seasons. "
              "Statewide annual limit 5 deer, including no more than 2 antlerless; daily 2 and possession 4 also apply.")
ANTLER = ("Antlered deer must have at least one antler 5 inches or longer with at least 2 points, each at least 1 inch. "
          "Youth under 16 have the statewide one-deer annual antler-point exception, still requiring a 5-inch antler. "
          "Antlerless deer and spotted fawns are not authorized by these area seasons.")
ARCHERY = "Bows only; crossbows, airbows and draw-lock bows require the brochure's Persons With Disabilities Crossbow Permit exception."
MUZZLE = "Muzzleloading guns only for deer or hog; ordinary archery equipment is prohibited."
GENERAL_METHODS = "Lawful shotguns, rifles, muzzleloading guns, pistols, airguns, bows and crossbows, subject to brochure restrictions."
DEER_GENERAL_METHODS = (GENERAL_METHODS + " No rimfire or non-expanding full-metal-jacket ammunition for deer; "
                        "PCP airguns must propel a bolt, arrow or bullet of at least .30 caliber.")
EXEMPTIONS = ("Brochure license/permit exemptions include children under 16, Florida residents 65+, residents with a qualifying disabled-person certificate, "
              "and qualifying resident military personnel home on leave. They do not override quota permits marked no exemptions or required deer tags. "
              "Hunters born on/after June 1, 1975 need hunter-safety certification or the lawful supervised mentoring exception. "
              "Youth require adult supervision; mentoring license holders require a licensed supervisor aged 21+. Consult the complete brochure.")
COMMON_ALERTS = [
    "Hunting over bait, taking swimming deer or spotted fawns, and hunting in posted closed areas are prohibited.",
    "Ordinary shooting hours are half an hour before sunrise through half an hour after sunset; turkey has separate hours.",
    "Night gun hunting, fully automatic firearms and centerfire semiautomatic rifles with magazines capable of more than 5 rounds are prohibited.",
    "Deer hunters and companions need 500 square inches of fluorescent orange above the waist, except bow-and-arrow hunting during archery season.",
    EXEMPTIONS,
    "The official brochure includes PDF BROCHURE and PDF MAP ONLY controls. Follow its current maps, access restrictions and FWC closure notices.",
]
CORBETT_ALERTS = [
    "Bruce Bowman archery still-hunt area permits bows only, with the brochure's disability crossbow/airbow/draw-lock exceptions. Closed-to-hunting trails, boardwalk, parking and adjacent areas remain closed.",
    "Centerfire rifles are prohibited south and east of Stumper's Grade; all rifles are prohibited in the Pratt-Whitney buffer and within a quarter mile of the railroad and Mecca Farms.",
    "Enter/exit at designated entrances; when staffed, report at a check station on entry and departure and check harvested wildlife. No night gun hunting for these species.",
    "Motorized travel is restricted to named roads and designated access routes. From July 31, 2026 an OHV Hunting Permit is required for allowed off-road hunting vehicle use; airboats, ATVs, tracked vehicles and unregistered motorcycles remain prohibited.",
    "The area closes August 16 at midnight through August 28 at 8 a.m., with the brochure's limited road, through-hiking and boardwalk exceptions.",
]
WETLAND_ALERTS = {
    "holey-land": [
        "Entry/exit is limited to the L-5 and Miami Canal levees. Hunting on roads, ramps, parking/camping areas, levees or adjacent powerline pads, and gun hunting on/from/across levees, is prohibited.",
        "Motorized use, scouting periods, flags and access routes are restricted. During general gun-vehicle season walk-hunting is closed and only vehicles authorized by its permits may operate; consult the map and permit conditions.",
        "Dogs may hunt deer/hog only during general gun-vehicle season; deer-dog hunting needs a valid WMA deer-dog permit, and dogs pursuing deer/hog need remote tracking and correction devices.",
        "When weekend check stations are staffed, check deer at the L-5 levee station before quartering, dismembering or removing them. General gun-vehicle deer must be immediately tagged with the FWC antlered deer tag.",
    ],
    "rotenberger": [
        "Entry/exit is limited to the L-4, Powerline, Miami Canal and Manley Ditch levees. Hunting on roads, ramps, parking/camping areas, levees or adjacent powerline pads, and gun hunting on/from/across levees, is prohibited.",
        "Vehicle, scouting-period and flag requirements apply; airboats are prohibited during archery, muzzleloading and general gun-walk seasons. Do not infer a general gun-vehicle hunt from access text: the 2026-2027 brochure lists none.",
        "Dogs may not hunt deer or wild hog. Leashed dogs may trail wounded game, subject to the brochure's restrictions.",
        "When weekend check stations are staffed, check deer at the southeast Holey Land station before quartering, dismembering or removing them.",
    ],
}


def _permits(kind, code, *, vehicle=False):
    text = ("No hunting license is required for wild hog. Management area permit required unless exempt. "
            if kind == "hog" else
            "Hunting license, management area permit and deer permit required unless exempt. Nonresident game hunters require an annual hunting license. ")
    if code == "ARCHERY":
        text += "Archery season permit required unless exempt. "
    elif code == "MUZZLELOADER":
        text += "Muzzleloading gun season permit required unless exempt. "
    if vehicle:
        text += ("General gun-vehicle quota/track permit and its antlered deer tag are required by this hunt; no quota exemptions and no guest hunters. "
                 "Deer require the supplied tag; a WMA deer-dog permit is required if hunting deer with dogs.")
    else:
        text += "No quota permit required for this listed season."
    return text


def _wetland_rules(area, kind):
    url = BROCHURES[area]
    bag = NO_HOG_BAG if kind == "hog" else DEER_LIMIT
    alerts = WETLAND_ALERTS[area] + ([] if kind == "hog" else [ANTLER,
        "Arrows and bolts used for deer must have broadheads at least 7/8 inch wide. Any otherwise-authorized deer PCP airgun projectile must satisfy the statewide .30-caliber minimum; this does not authorize PCP equipment during bows-only or muzzleloader-only seasons.",
        "Muzzleloaders used for deer must be at least .30 caliber for a single bullet or at least 20 gauge when firing 2 or more balls.",
        "Log harvested deer before moving them and report to FWC within 24 hours of recovery, in addition to the area's check-station duties."])
    general_methods = DEER_GENERAL_METHODS if kind == "deer" else GENERAL_METHODS
    schedules = [
        ("Archery", "ARCHERY", "2026-08-08", "2026-08-30", ARCHERY),
        ("Muzzleloading gun", "MUZZLELOADER", "2026-09-05", "2026-09-13", MUZZLE),
        ("General gun-walk", "GENERAL_GUN_WALK", "2026-10-03", "2026-10-18", general_methods),
    ]
    if area == "holey-land":
        schedules.append(("General gun-vehicle", "GENERAL_GUN_VEHICLE", "2026-11-21", "2026-12-06", general_methods))
    rules = []
    for name, code, first, last, methods in schedules:
        vehicle = code == "GENERAL_GUN_VEHICLE"
        season_bag = ("Area general gun-vehicle limit 1 antlered deer per FWC antlered deer tag. Statewide annual 5 (maximum 2 antlerless), daily 2 and possession 4 apply."
                      if vehicle and kind == "deer" else bag)
        rules.append(rule(name, code, "Wild hog, either sex" if kind == "hog" else "Antlered deer only",
                          [period(first, last)], season_bag, _permits(kind, code, vehicle=vehicle), methods,
                          [url, LICENSE], alerts=alerts))
    return rules


def _corbett_hog_rules():
    rows = []
    schedules = [
        ("Archery", "ARCHERY", "2026-08-29", "2026-09-20", ARCHERY),
        ("Muzzleloading gun", "MUZZLELOADER", "2026-10-03", "2026-10-18", "Muzzleloading guns only, except bows in the Bruce Bowman area; muzzleloading season permit still required there."),
        ("General gun", "GENERAL_GUN", "2026-11-07", "2027-01-03", GENERAL_METHODS),
        ("Small game", "SMALL_GAME", "2027-01-04", "2027-02-21", GENERAL_METHODS),
    ]
    for name, code, first, last, methods in schedules:
        rows.append(rule(name, code, "Wild hog, either sex", [period(first, last)], NO_HOG_BAG,
                         _permits("hog", code), methods, [BROCHURES["corbett"], LICENSE],
                         alerts=CORBETT_ALERTS + ["Dogs may hunt hog only during general gun season, outside the designated still-hunt areas. Tracking and behavior-correction devices are required; small-game season does not authorize hog dogs."]))
    return rows


def _corbett_turkey_rules():
    url = BROCHURES["corbett"]
    bag = "Area daily limit 1 turkey; statewide spring season limit 2, daily 2 and possession 2 also apply. Youth harvest counts toward the spring limit."
    methods = ("Bows, crossbows, PCP airguns propelling a bolt or arrow, or centerfire/muzzleloading shotguns with No. 2 or smaller shot. "
               "Bruce Bowman remains bows only except qualifying disability permits. Rifles, pistols and PCP bullets are not authorized for this spring turkey hunt.")
    permits = "Hunting license, management area permit and turkey permit unless exempt; annual hunting license for nonresidents. No quota permit required."
    alerts = CORBETT_ALERTS + [
        "Gobbler or bearded turkey only. Hunting other animals during spring turkey season is prohibited; do not infer firearm permission for other species from the spring turkey dates.",
        "Turkey shooting hours are half an hour before sunrise until sunset. Hunting roosted turkey or over bait is prohibited.",
        "Turkey arrows and bolts require broadheads at least 7/8 inch wide. PCP airguns remain limited here to bolts or arrows and must meet the statewide .20-caliber minimum; PCP bullets remain prohibited by this area's spring methods.",
        "Log turkey before moving it and report to FWC within 24 hours of recovery, in addition to check-station requirements.",
        "Only Florida resident turkey hunters may hunt March 6-14, 2027; later spring dates also remain limited to Saturdays, Sundays and Wednesdays.",
        "No fall turkey season is listed for Corbett; do not apply private-land fall seasons to this area.",
    ]
    youth = rule("Youth turkey", "YOUTH_TURKEY", "Gobbler or bearded turkey", [period("2027-02-26", "2027-03-01")],
                 bag, permits + " Hunters under 16 are exempt; participating adults need required licenses/permits unless exempt.", methods,
                 [url, LICENSE], alerts=alerts + ["Only youth under 16 may harvest, under direct physical supervision by an adult aged 18+. Properly licensed adults may assist in the youth's presence but may not harvest."])
    youth["maximum_age"] = 15
    spring_period = period("2027-03-06", "2027-04-11")
    spring_period["weekdays"] = [3, 6, 7]
    spring = rule("Spring turkey", "SPRING_TURKEY", "Gobbler or bearded turkey", [spring_period],
                  bag, permits, methods, [url, LICENSE], alerts=alerts)
    return [youth, spring]


def _prohibited_turkey(area):
    denied = rule("Turkey take prohibited", "PROHIBITED", "Turkey take prohibited", [deepcopy(COVERAGE)],
                  "No turkey may be taken.", "No license or permit authorizes turkey take in this area.",
                  "Turkey hunting/take is prohibited by the area brochure.", [BROCHURES[area]],
                  alerts=["The area brochure expressly prohibits turkey. Private-land turkey dates and permits do not override this prohibition."])
    denied["prohibited"] = True
    return [denied]


def _python_rules(area):
    url = BROCHURES[area]
    alerts = (CORBETT_ALERTS if area == "corbett" else WETLAND_ALERTS[area]) + [
        "EO23-16 prohibits traps and modified/free-bolt captive-bolt stunners; all other area access and equipment restrictions still apply.",
        "No live python may be removed from the area. Florida anti-cruelty law and FWC humane-killing guidance apply; the required second step prevents recovery after immediate loss of consciousness.",
        "A year-round python removal opportunity does not open deer/hog/turkey seasons or authorize firearm discharge outside lawful hunting seasons. Follow each season's allowed firearm methods and property closures.",
        "Python shooting hours are half an hour before sunrise until half an hour after sunset. Report sightings/take through FWC's non-native wildlife reporting service.",
    ]
    if area == "corbett":
        alerts += ["In Bruce Bowman only hand tools and bows may take reptiles, except qualifying disability crossbow/airbow/draw-lock permits. Dogs may only search for reptiles during general gun season.",
                   "Spring turkey rules prohibit hunting other animals; confirm the interaction with the separate reptile provisions with FWC before attempting firearm reptile removal during spring turkey dates."]
    elif area == "holey-land":
        alerts += ["Centerfire rifle take is prohibited March 8-April 11, 2027; the seasonal firearm restriction still applies at all other times. Dogs may only search for reptiles during general gun-vehicle season."]
    else:
        alerts += ["Centerfire rifle take is prohibited beginning March 8, 2027 after small-game season; firearms remain limited to lawful open hunting seasons. Dogs may not take or search for reptiles."]
    return [rule("Year-round python removal", "YEAR_ROUND", "Burmese python", [deepcopy(COVERAGE)],
                 "No bag limit.", "No license or removal permit required for non-native reptiles; vehicle/access permits still apply where required.",
                 "Non-firearm removal is allowed year-round subject to access and humane-killing rules. Firearms may be used only during open brochure hunting seasons and only as allowed by that season. Follow the linked FWC humane-killing guidance.",
                 [url, PYTHON, HUMANE, PYTHON_ORDER], alerts=alerts)]


def seed_wma_review_drafts():
    """Add 22 independently reviewable area/land/species drafts without overwrites."""
    lands = [LandType.objects.get_or_create(name=name)[0] for name in
             ["Wildlife Management Area (WMA)", "Commission-Managed Land"]]
    species = {"hog": Species.objects.get_or_create(common_name="Wild Hog", defaults={"scientific_name": "Sus scrofa"})[0],
               "turkey": Species.objects.get_or_create(common_name="Wild Turkey", defaults={"scientific_name": "Meleagris gallopavo"})[0],
               "python": Species.objects.get_or_create(common_name="Burmese Python", defaults={"scientific_name": "Python bivittatus"})[0]}
    species["deer"] = Species.objects.filter(common_name__icontains="deer").first()
    if species["deer"] is None:
        species["deer"] = Species.objects.create(common_name="White Tailed Deer", scientific_name="Odocoileus virginianus")
    created = 0
    for area_key, area_name in AREA_NAMES.items():
        area = ManagedArea.objects.get_or_create(name=area_name, defaults={"area_type": "WMA"})[0]
        kinds = ["hog", "turkey", "python"] if area_key == "corbett" else ["deer", "hog", "turkey", "python"]
        for kind in kinds:
            if kind == "python":
                rules = _python_rules(area_key)
            elif kind == "turkey":
                rules = _corbett_turkey_rules() if area_key == "corbett" else _prohibited_turkey(area_key)
            elif area_key == "corbett":
                rules = _corbett_hog_rules()
            else:
                rules = _wetland_rules(area_key, kind)
            sources = [source(f"FWC {area_name} 2026-2027 regulations and map", BROCHURES[area_key],
                              "Interactive brochure checked: area dates, legal species, bag limits, methods, permits, access and exceptions; PDF map available on the same page."),
                       source("FWC hunting licenses and permits", LICENSE, "General license, management-area and season permits; brochure exemptions and area-specific quota restrictions retained.")]
            if kind == "deer" or (kind == "turkey" and area_key == "corbett"):
                sources.append(source("FWC legal resident-game equipment", TAKING_GAME,
                                      "Checked broadhead minimum width, species-specific PCP minimums and deer muzzleloader design requirements; area season-method restrictions remain controlling."))
                for entry in rules:
                    entry["source_urls"].append(TAKING_GAME)
            if kind == "python":
                sources += [source("FWC Executive Order 23-16", PYTHON_ORDER, "Page 2: traps and modified/free-bolt captive-bolt stunners prohibited; firearms need specific area authorization."),
                            source("FWC python removal", PYTHON, "Area-specific removal is subject to the brochure and current FWC orders."),
                            source("FWC humane killing methods", HUMANE, "Humane onsite killing and required second step; no public live transport.")]
            for land in lands:
                data = payload(species[kind], land, deepcopy(rules), deepcopy(sources),
                               coverage=deepcopy(COVERAGE), scopes={"managed_area": area.pk}, required=["managed_area"],
                               alerts=COMMON_ALERTS + (["The small-game legal-species list does not include wild hog; do not infer a hog season from the small-game dates."]
                                                       if area_key != "corbett" and kind == "hog" else []))
                data["data_expansion_edition"] = EDITION
                obj, added = RegulationDraft.objects.get_or_create(
                    key=f"{kind}-{area_key}-{land.pk}-2026-2027-expanded",
                    defaults={"title": f"{species[kind].common_name}: {area_name} / {land.name}, 2026-2027 expansion",
                              "species": species[kind], "land_type": land, "payload": data})
                if added:
                    obj.full_clean()
                    created += 1
    return created
