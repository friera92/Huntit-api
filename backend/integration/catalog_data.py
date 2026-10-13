"""Add missing working-catalog details without overwriting teammate values.

Links were checked against FWC's python-removal directory on 2026-10-12.
Catalog links are references, never evidence that an area season is open.
"""
from urllib.parse import quote_plus

from regulations.models import LicensePermit, ManagedArea, Source
from .starter import LICENSE, PYTHON, PYTHON_AREAS


# In the same order as the 32 names in the official directory / original catalog.
BROCHURE_TITLES = [
    "A-1 FEB Impoundment PSGHA", "Allapattah Flats", "Allapattah Flats PSGHA", "Big Cypress",
    "C-23/24 Reservoir PSGHA", "CREW", "Dinner Island Ranch", "DuPuis Dove Field PSGHA",
    "Everglades and Francis S. Taylor", "Fisheating Creek", "Frog Pond North PSGHA", "Holey Land",
    "J.W. Corbett", "Hungryland", "DuPuis", "Picayune Strand", "Rocky Glades PSGHA", "Rotenberger",
    "Southern Glades", "Spirit-of-the-Wild", "Stormwater Treatment Area 1 West", "Stormwater Treatment Area 2",
    None, "Stormwater Treatment Area 5/6", "Okaloacoochee Slough",
    "Kissimmee Bend Unit of the Everglades Headwaters", "Babcock / Webb", "Babcock / Webb - Yucca Pens Unit",
    "Orange Hammock", "Myakka State Forest PSGHA", "Hungryland PSGHA", None,
]
LICENSE_DETAILS = {
    "Florida Hunting License": "Required for deer/turkey unless exempt; hunting wild hog does not require a hunting license. Other area and season permits can still be required.",
    "Deer Permit": "Required with a hunting license to take or attempt deer unless exempt. It does not replace area, quota or season requirements.",
    "Management Area Permit": "Required on applicable WMAs/WEAs and some PSGHAs unless exempt; check the specific brochure. Hog hunting may require it despite the hunting-license exemption.",
    "Archery Season Permit": "Required for applicable archery-season hunts unless exempt; other species and area permits may apply. The private-land hog no-permit exception remains separate.",
    "Crossbow Season Permit": "Required for applicable crossbow-season hunts unless exempt; other species and area permits may apply. The private-land hog no-permit exception remains separate.",
    "Muzzleloading Gun Season Permit": "Required for applicable muzzleloading-season hunts unless exempt; other species and area permits may apply. The private-land hog no-permit exception remains separate.",
    "Turkey Permit": "Required with a hunting license to take or attempt turkey unless exempt; area and season permits may also apply.",
}


def _fill_blanks(obj, values):
    changed = []
    for field, value in values.items():
        if not getattr(obj, field) and value:
            setattr(obj, field, value)
            changed.append(field)
    if changed:
        obj.save(update_fields=changed)
    return bool(changed)


def seed_catalog_details():
    permit_source, _ = Source.objects.get_or_create(url=LICENSE, defaults={
        "organization": "Florida Fish and Wildlife Conservation Commission",
        "title": "FWC hunting licenses and permits — working catalog reference",
        "document_type": "Official web page",
        "notes": "Source checked 2026-10-12. New working details require human review before regulatory publication.",
    })
    permits_added = permits_enriched = areas_enriched = 0
    for name, requirements in LICENSE_DETAILS.items():
        permit, added = LicensePermit.objects.get_or_create(name=name)
        permits_added += int(added)
        permits_enriched += int(_fill_blanks(permit, {
            "requirements": requirements, "source_id": permit_source.pk,
            "description": "Working reference; confirm exemptions and the selected season/area in official FWC sources.",
        }))
    for index, name in enumerate(PYTHON_AREAS):
        area = ManagedArea.objects.filter(name=name).first()
        if area is None:
            continue
        title = BROCHURE_TITLES[index]
        if index == 31:
            link = "https://myfwc.com/recreation/cooperative/everglades-headwaters/"
        elif title is None:
            # FWC's older STA3/4 link redirects to the finder, not an area brochure.
            link = "https://myfwc.com/hunting/wma-brochures/"
        else:
            link = "https://app.myfwc.com/hgm/hgmsearch/wmad?brochureTitle=" + quote_plus(title)
        areas_enriched += int(_fill_blanks(area, {
            "brochure_url": link,
            "map_url": PYTHON,
            "description": "FWC-listed python-removal area. The official python directory links its 32-area map. Check the linked brochure/finder for area maps, current access and species-specific seasons; this catalog entry alone does not establish an open hunt.",
        }))
    return {"permits_added": permits_added, "permits_enriched": permits_enriched, "areas_enriched": areas_enriched}
