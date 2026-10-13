"""Source-checked starter drafts. This module NEVER approves or publishes data.

Checked on 2026-10-12 against the linked FWC pages. Review coverage is a
maintenance boundary, not a claim that a year-round law expires on that date.
"""
from copy import deepcopy

from regulations.models import DeerManagementUnit, HuntingZone, LandType, ManagedArea, Species
from .models import RegulationDraft

CHECKED = "2026-10-12"
HOG = "https://myfwc.com/hunting/wild-hog/"
PYTHON = "https://myfwc.com/wildlifehabitats/nonnatives/python/removing/"
PYTHON_PROFILE = "https://myfwc.com/wildlifehabitats/profiles/reptiles/snakes/burmese-python/"
PYTHON_NEWS = "https://myfwc.com/news/all-news/python-challenge-0826/"
HUMANE = "https://myfwc.com/wildlifehabitats/nonnatives/python/humane-killing-methods/"
DEER = "https://myfwc.com/hunting/season-dates/"
LICENSE = "https://myfwc.com/license/recreational/hunting/"
GENERAL = "https://myfwc.com/hunting/regulations/general-information/"
HARVEST = "https://myfwc.com/hunting/deer/harvest-report/"
YOUTH = "https://myfwc.com/hunting/get-started/youth-deer-hunting/"
CORBETT = "https://app.myfwc.com/hgm/hgmsearch/wmad?brochureTitle=J.W.+Corbett"
DMU = {zone: f"https://myfwc.com/hunting/season-dates/dmu-{zone.lower()}/" for zone in "ABCD"}

PYTHON_AREAS = [
    "A I -FEB PSGHA", "Allapattah Flats WMA", "Allapattah Flats PSGHA", "Big Cypress WMA",
    "C-23/24 Reservoir PSGHA", "CREW WEA", "Dinner Island Ranch WMA", "DuPuis Dove Field PSGHA",
    "Everglades and Francis S. Taylor WMA", "Fisheating Creek WMA", "Frog Pond North PSGHA",
    "Holey Land WMA", "J. W. Corbett WMA", "John C. and Mariana Jones/Hungryland WEA",
    "John G. and Susan H. DuPuis, Jr. WEA", "Picayune Strand WMA", "Rocky Glades PSGHA",
    "Rotenberger WMA", "Southern Glades WEA", "Spirit-of-the-Wild WMA",
    "Stormwater Treatment Area 1 West PSGHA", "Stormwater Treatment Area 2 PSGHA",
    "Stormwater Treatment Area 3/4 PSGHA", "Stormwater Treatment Area 5/6 PSGHA",
    "Okaloacoochee Slough WMA", "Everglades Headwaters WMA, Kissimmee Bend Unit",
    "Fred C. Babcock / Cecil M. Webb WMA", "Fred C. Babcock/Cecil M. Webb WMA Yucca Pens Unit",
    "Orange Hammock WMA", "Myakka State Forest PSGHA",
    "Hungryland Small Game Area (within John C. and Mariana Jones/Hungryland WEA)",
    "Everglades Headwaters National Wildlife Refuge, Okeechobee Unit",
]


def source(title, url, evidence):
    return {"title": title, "url": url, "checked_on": CHECKED,
            "retrieved_at": None, "evidence": evidence}


def period(first, last):
    return {"start_date": first, "end_date": last}


def payload(species, land, rules, sources, *, scopes=None, required=None, permission=False, alerts=None,
            coverage=None):
    return {"version": 1, "species_id": species.pk, "land_type_id": land.pk,
            "coverage": coverage or period("2026-07-01", "2027-06-30"),
            "scopes": scopes or {}, "required_inputs": required or [], "permission_required": permission,
            "rules": rules, "sources": sources, "alerts": alerts or []}


def rule(name, code, category, periods, bag, licenses, methods, source_urls, *, scopes=None, alerts=None):
    return {"name": name, "code": code, "category": category, "periods": periods, "bag": bag,
            "licenses": licenses, "methods": methods, "source_urls": source_urls,
            "scopes": scopes or {}, "alerts": alerts or []}


def seed_review_drafts():
    private = LandType.objects.get_or_create(name="Private Land")[0]
    public = LandType.objects.get_or_create(name="Commission-Managed Land")[0]
    wma = LandType.objects.get_or_create(name="Wildlife Management Area (WMA)")[0]
    hog = Species.objects.get_or_create(common_name="Wild Hog", defaults={"scientific_name": "Sus scrofa"})[0]
    python = Species.objects.get_or_create(common_name="Burmese Python", defaults={"scientific_name": "Python bivittatus"})[0]
    deer = Species.objects.filter(common_name__icontains="deer").first()
    if deer is None:
        deer = Species.objects.create(common_name="White Tailed Deer", scientific_name="Odocoileus virginianus")
    zones = {code: HuntingZone.objects.get_or_create(code=code, defaults={"name": f"Zone {code}"})[0] for code in "ABCD"}
    dmus = {code: DeerManagementUnit.objects.get_or_create(code=code, defaults={"zone": zones[code[0]]})[0]
            for code in ["A1", "A2", "A3", "B1", "C1", "C2", "C3", "C4", "C5", "C6", "D1", "D2"]}
    areas = []
    for name in PYTHON_AREAS:
        area_type = next((kind for kind in ["PSGHA", "WMA", "WEA", "SGA"] if kind in name), "NWR")
        areas.append(ManagedArea.objects.get_or_create(name=name, defaults={"area_type": area_type})[0])
    corbett = next(row for row in areas if row.name == "J. W. Corbett WMA")
    created = 0

    def draft(key, title, species, land, content):
        nonlocal created
        obj, added = RegulationDraft.objects.get_or_create(
            key=key, defaults={"title": title, "species": species, "land_type": land, "payload": content})
        if added:
            obj.full_clean()
            created += 1

    hog_rule = rule("Year-round private-land hog", "YEAR_ROUND", "Either sex",
                    [period("2026-01-01", "2026-12-31")], "No size or bag limit.",
                    "No hunting license or nighttime gun-and-light permit required with landowner permission.",
                    "Lawful rifle, shotgun, bow, crossbow, pistol or air gun; lawful trapping and dogs subject to restrictions.",
                    [HOG], alerts=["With dogs, carry written landowner permission; identification collars and remote tracking/correction rules apply.",
                                  "Live transport or holding wild hogs requires the applicable FDACS authorization."])
    draft("hog-private-2026", "Wild hog: private land, 2026", hog, private,
          payload(hog, private, [hog_rule], [source("FWC Wild Hog", HOG,
                  "Private-property year-round exception, permission, license/night permit, bag and methods checked.")],
                  permission=True, coverage=period("2026-01-01", "2026-12-31")))

    python_sources = [source("FWC Removing Pythons in Florida", PYTHON,
                             "Current 32-area list, year-round removal, no license/permit and no bag limit checked."),
                      source("FWC Burmese Python regulatory status", PYTHON_PROFILE,
                             "Anti-cruelty protection and private-property permission checked."),
                      source("FWC humane killing guidance", HUMANE,
                             "Humane onsite removal and prohibition on public live transport checked."),
                      source("FWC 2026 python removal opportunities", PYTHON_NEWS,
                             "Explicit private-land no hunting-license/no-permit statement checked.")]
    python_rule = rule("Year-round python removal", "YEAR_ROUND", "Burmese python",
                       [period("2026-01-01", "2026-12-31")], "No bag limit.",
                       "No hunting license or removal permit required within the stated scope.",
                       "FWC describes captive-bolt equipment or a lawfully used firearm/PCP air gun for immediate loss of consciousness, followed by pithing as the required second step to prevent recovery. Follow FWC/AVMA training and all property-specific firearm rules.",
                       [PYTHON, PYTHON_PROFILE, HUMANE, PYTHON_NEWS], alerts=[
                           "Florida anti-cruelty law applies. Humanely kill at the capture location; members of the public may not transport live pythons.",
                           "Obtain appropriate humane-removal training before attempting to handle or euthanize a large constrictor. The linked FWC guidance explains both required steps; the first step alone is insufficient.",
                           "Follow Executive Order 23-16 and specific area access, closures and firearm rules. The annual area list does not override those rules."])
    draft("python-private-2026", "Burmese python: private land, 2026", python, private,
          payload(python, private, [python_rule], python_sources, permission=True,
                  coverage=period("2026-01-01", "2026-12-31")))
    for land in [public, wma]:
        supported_areas = areas if land == public else [row for row in areas if row.area_type == "WMA"]
        draft(f"python-public-{land.pk}-2026", f"Burmese python: {len(supported_areas)} FWC-listed areas / {land.name}, 2026", python, land,
              payload(python, land, [deepcopy(python_rule)], python_sources,
                      scopes={"managed_area": [row.pk for row in supported_areas]}, required=["managed_area"],
                      coverage=period("2026-01-01", "2026-12-31"),
                      alerts=["Coverage is restricted to FWC's current 32-area list (the WMA land-type option covers its WMA entries); other public lands are not covered."]))

    # Dates are 2026-2027 FWC seasons; cross-year endpoints are explicitly 2027.
    schedules = {
        "A": {"ARCHERY": [("2026-08-01", "2026-08-30")], "CROSSBOW": [("2026-08-01", "2026-09-04")],
              "MUZZLELOADER": [("2026-09-05", "2026-09-18")],
              "GENERAL_GUN": [("2026-09-19", "2026-10-18"), ("2026-11-21", "2027-01-03")],
              "YOUTH": [("2026-09-12", "2026-09-13")]},
        "B": {"ARCHERY": [("2026-10-17", "2026-11-15")], "CROSSBOW": [("2026-10-17", "2026-11-20")],
              "MUZZLELOADER": [("2026-11-21", "2026-12-04")], "GENERAL_GUN": [("2026-12-05", "2027-02-21")],
              "YOUTH": [("2026-11-28", "2026-11-29")]},
        "C": {"ARCHERY": [("2026-09-19", "2026-10-18")], "CROSSBOW": [("2026-09-19", "2026-10-23")],
              "MUZZLELOADER": [("2026-10-24", "2026-11-06")], "GENERAL_GUN": [("2026-11-07", "2027-01-24")],
              "YOUTH": [("2026-10-31", "2026-11-01")]},
        "D": {"ARCHERY": [("2026-10-24", "2026-11-25")],
              "CROSSBOW": [("2026-10-24", "2026-11-25"), ("2026-11-30", "2026-12-04")],
              "MUZZLELOADER": [("2026-12-05", "2026-12-11"), ("2027-02-22", "2027-02-28")],
              "GENERAL_GUN": [("2026-11-26", "2026-11-29"), ("2026-12-12", "2027-02-21")],
              "YOUTH": [("2026-12-05", "2026-12-06")]},
    }
    methods = {"ARCHERY": "Bows only.", "CROSSBOW": "Crossbows, bows and airbows.",
               "MUZZLELOADER": "Muzzleloaders, crossbows, bows and airbows; muzzleloading design restrictions apply.",
               "GENERAL_GUN": "Lawful centerfire rifles, shotguns, handguns, muzzleloaders, PCP air guns, crossbows and bows.",
               "YOUTH": "Any legal method for an eligible youth hunter; supervision restrictions apply."}
    names = {"ARCHERY": "Archery", "CROSSBOW": "Crossbow", "MUZZLELOADER": "Muzzleloading gun",
             "GENERAL_GUN": "General gun", "YOUTH": "Youth weekend"}
    permits = {"ARCHERY": "Archery season permit", "CROSSBOW": "Crossbow season permit",
               "MUZZLELOADER": "Muzzleloading gun season permit"}
    deer_sources = [source("FWC 2026-2027 seasons and bag limits", DEER,
                           "Zone A-D antlered/antlerless dates and daily, possession, annual limits checked; excludes WMAs."),
                    source("FWC recreational licenses and permits", LICENSE,
                           "Hunting/deer and season permits checked; individual statutory exemptions require confirmation."),
                    source("FWC general hunting rules", GENERAL,
                           "Shooting hours, safety, access and general restrictions checked."),
                    source("FWC deer harvest reporting", HARVEST,
                           "Log before moving and official reporting deadlines checked."),
                    source("FWC youth deer weekend", YOUTH,
                           "Eligible ages, supervision, no youth permit requirement and participating-adult restrictions checked.")]
    deer_sources += [source(f"FWC DMU {zone} antler rules", DMU[zone], "DMU-specific antler criteria and location exceptions checked.") for zone in "ABCD"]
    for code, dmu in dmus.items():
        zone = code[0]
        bag = ("Daily 2 deer; possession 4; annual 5, including no more than "
               + ("3 antlerless in DMU D2 outside WMAs." if code == "D2" else "2 antlerless."))
        antler = ("For hunters 16+: one antler at least 5 inches long with 2 points of at least 1 inch."
                  if code in ["A1", "A2", "C3", "D1"] else
                  "For hunters 16+: one antler at least 5 inches long with 3 points of at least 1 inch, or a main beam of at least 10 inches.")
        alerts = [antler, "Youth 15 and under have a one-deer annual exception to DMU antler-point criteria; a 5-inch antler is still required.",
                  "Spotted fawns may not be taken. Confirm the precise parcel, shooting hours, hunter safety and local restrictions."]
        if code == "A1":
            alerts.append("Antlerless deer may not be taken in DMU A1. Taking any deer in the Florida Keys is prohibited.")
        if code == "A2":
            alerts.append("Deer take is prohibited in the specified Collier County area bounded by I-75, SR29, US41 and Fakahatchee Strand's western boundary.")
        rules = []
        for season_code, dates in schedules[zone].items():
            youth = season_code == "YOUTH"
            youth_alerts = ["Only hunters 15 and under, supervised by an adult 18+, qualify for the youth weekend; at most one antlered or antlerless deer where DMU restrictions permit.",
                            "Participating adults 16+ need hunting, deer and muzzleloading permits unless exempt; muzzleloader/bow/crossbow and legal antlered deer only. Adults may not shoot during youth dog pursuits."]
            rules.append(rule(names[season_code], season_code, "Youth deer (DMU restrictions apply)" if youth else "Antlered deer",
                              [period(*value) for value in dates], "1 deer for the youth weekend, counted toward annual 5." if youth else bag,
                              ("No hunting license or permit for eligible youth 15 and under or an adult who only supervises. Participating adults have separate permit requirements."
                               if youth else "Hunting license and deer permit unless exempt. " + (permits.get(season_code, "") + " required unless exempt." if season_code in permits else "Check individual exemptions.")),
                              methods[season_code], [DEER, LICENSE, DMU[zone]] + ([YOUTH] if youth else []),
                              scopes={"zone": zones[zone].pk, "dmu": dmu.pk},
                              alerts=(youth_alerts if youth else []) + alerts))
        # Antlerless schedules are not inferred from antlered dates.
        antlerless = {}
        if code in ["A2", "A3"]:
            end = "2026-08-09" if code == "A2" else "2026-08-16"
            antlerless = {"ARCHERY": [("2026-08-01", end)], "CROSSBOW": [("2026-08-01", end)],
                          "GENERAL_GUN": [("2026-11-21", "2026-11-22" if code == "A2" else "2026-11-24")]}
        elif zone in "BCD":
            antlerless = {key: value for key, value in schedules[zone].items() if key != "YOUTH"}
            if zone == "B":
                antlerless["GENERAL_GUN"] = [("2026-12-26", "2027-01-03")]
            elif zone == "C":
                antlerless["GENERAL_GUN"] = [("2026-11-07", "2026-12-06")] if code == "C5" else [("2026-11-21", "2026-11-29")]
        for season_code, dates in antlerless.items():
            rules.append(rule(names[season_code], season_code, "Antlerless deer (not spotted fawns)",
                              [period(*value) for value in dates], bag,
                              "Hunting license and deer permit unless exempt. " + (permits.get(season_code, "") + " required unless exempt." if season_code in permits else "Check individual exemptions."),
                              methods[season_code], [DEER, LICENSE], scopes={"zone": zones[zone].pk, "dmu": dmu.pk}))
        draft(f"deer-private-{code.lower()}-2026-2027", f"Deer: private land, DMU {code}, 2026-2027", deer, private,
              payload(deer, private, rules, deer_sources, scopes={"zone": zones[zone].pk, "dmu": dmu.pk},
                      required=["zone", "dmu"], permission=True, alerts=[
                          "Statewide schedules apply outside the WMA system. Special deer-program permits and other statutory exceptions are outside this standard lookup.",
                          "All harvested deer must be logged before moving and officially reported within 24 hours or earlier processing/transfer/out-of-state deadline. HuntIt is not the FWC reporting system."]))

    corbett_sources = [source("FWC J.W. Corbett 2026-2027 area brochure", CORBETT,
                              "Area dates, daily 1/annual 2 deer, antler/antlerless, methods, permits and named-area exceptions checked."),
                       deer_sources[1], deer_sources[3]]
    corbett_bag = "Area daily limit 1 deer; area annual limit 2 across all seasons. Statewide annual 5 (maximum 2 antlerless) and possession 4 also apply."
    corbett_alerts = ["Antlered deer: at least 3 one-inch points on one antler or main beam at least 10 inches; confirm age exceptions in the brochure.",
                      "Bruce Bowman archery area is bows-only across seasons except the brochure's disability exemptions.",
                      "Check current closures, check-station duties, vehicle access and maps. An OHV hunting permit is required for relevant off-road hunting vehicle use from July 31, 2026."]
    common_permits = "Hunting license, management area permit and deer permit unless exempt; no quota permit required. "
    corbett_rules = [
        rule("Corbett archery", "ARCHERY", "Antlered deer", [period("2026-08-29", "2026-09-20")],
             corbett_bag, common_permits + "Archery season permit unless exempt.",
             "Bows only; crossbows, airbows and draw-lock bows prohibited except qualifying disability permits.", [CORBETT, LICENSE], alerts=corbett_alerts),
        rule("Corbett archery", "ARCHERY", "Antlerless deer", [period("2026-09-12", "2026-09-20")],
             corbett_bag, common_permits + "Archery season permit unless exempt.",
             "Bows only, subject to the brochure's disability exemptions.", [CORBETT, LICENSE], alerts=corbett_alerts),
        rule("Corbett muzzleloading gun", "MUZZLELOADER", "Antlered deer only", [period("2026-10-03", "2026-10-18")],
             corbett_bag, common_permits + "Muzzleloading gun season permit unless exempt, including Bruce Bowman archery-area hunters.",
             "Muzzleloaders only except bows in Bruce Bowman archery area; follow area-specific exceptions.", [CORBETT, LICENSE], alerts=corbett_alerts),
        rule("Corbett general gun", "GENERAL_GUN", "Antlered deer only", [period("2026-11-07", "2027-01-03")],
             corbett_bag, common_permits + "WMA deer-dog permit required if hunting deer with dogs; no exemptions for that permit.",
             "Lawful general-gun methods subject to brochure restrictions; dogs prohibited in designated still-hunt areas; Bruce Bowman remains bows-only.",
             [CORBETT, LICENSE], alerts=corbett_alerts),
    ]
    for land in [wma, public]:
        draft(f"deer-corbett-{land.pk}-2026-2027", f"Deer: J.W. Corbett / {land.name}, 2026-2027", deer, land,
              payload(deer, land, corbett_rules, corbett_sources, scopes={"managed_area": corbett.pk},
                      required=["managed_area"], alerts=[
                          "Representative WMA coverage is J.W. Corbett only. Other WMA deer regulations require a separately reviewed area brochure.",
                          "Use official FWC harvest reporting in addition to this personal log."]))
    return created
