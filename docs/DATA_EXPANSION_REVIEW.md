# HuntIt data expansion — source review pack

**Status: source-checked working data; human approval and publication remain pending.**

Edition: `fwc-data-expansion-2026-10-12-v1`. Source check: 2026-10-12. Exact JSON SHA-256: `f54de4a3edbf240c5c20f8f6fc88fcb054dc64053dc227b544d2fc48d239374c`.

This pack contains **58 draft scopes/revisions**. The two public-land selectors repeat the same area rules; they are not additional areas.

Compare the dates, methods, limits, licenses, area exceptions and profile below with the linked FWC sources. Source preparation does not constitute human approval. The two earlier approved releases remain intact.

After checking, an authorized reviewer can publish each draft in Django Admin, using the source acknowledgement and review notes. Saving alone does not publish. Repeating setup preserves edited drafts and withdrawn publications.

## Coverage index

| Draft | Species / land | Change |
|---|---|---|
| `deer-corbett-2-2026-2027` | White Tailed Deer / Wildlife Management Area (WMA) | proposed revision of existing approved draft |
| `deer-corbett-3-2026-2027` | White Tailed Deer / Commission-Managed Land | proposed revision of existing approved draft |
| `deer-dinner-island-2-2026-2027` | White Tailed Deer / Wildlife Management Area (WMA) | new draft |
| `deer-dinner-island-3-2026-2027` | White Tailed Deer / Commission-Managed Land | new draft |
| `deer-holey-land-2-2026-2027-expanded` | White Tailed Deer / Wildlife Management Area (WMA) | new draft |
| `deer-holey-land-3-2026-2027-expanded` | White Tailed Deer / Commission-Managed Land | new draft |
| `deer-private-a1-2026-2027` | White Tailed Deer / Private Land | proposed revision of existing approved draft |
| `deer-private-a2-2026-2027` | White Tailed Deer / Private Land | proposed revision of existing approved draft |
| `deer-private-a3-2026-2027` | White Tailed Deer / Private Land | proposed revision of existing approved draft |
| `deer-private-b1-2026-2027` | White Tailed Deer / Private Land | proposed revision of existing approved draft |
| `deer-private-c1-2026-2027` | White Tailed Deer / Private Land | proposed revision of existing approved draft |
| `deer-private-c2-2026-2027` | White Tailed Deer / Private Land | proposed revision of existing approved draft |
| `deer-private-c3-2026-2027` | White Tailed Deer / Private Land | proposed revision of existing approved draft |
| `deer-private-c4-2026-2027` | White Tailed Deer / Private Land | proposed revision of existing approved draft |
| `deer-private-c5-2026-2027` | White Tailed Deer / Private Land | proposed revision of existing approved draft |
| `deer-private-c6-2026-2027` | White Tailed Deer / Private Land | proposed revision of existing approved draft |
| `deer-private-d1-2026-2027` | White Tailed Deer / Private Land | proposed revision of existing approved draft |
| `deer-private-d2-2026-2027` | White Tailed Deer / Private Land | proposed revision of existing approved draft |
| `deer-rotenberger-2-2026-2027-expanded` | White Tailed Deer / Wildlife Management Area (WMA) | new draft |
| `deer-rotenberger-3-2026-2027-expanded` | White Tailed Deer / Commission-Managed Land | new draft |
| `hog-corbett-2-2026-2027-expanded` | Wild Hog / Wildlife Management Area (WMA) | new draft |
| `hog-corbett-3-2026-2027-expanded` | Wild Hog / Commission-Managed Land | new draft |
| `hog-dinner-island-2-2026-2027` | Wild Hog / Wildlife Management Area (WMA) | new draft |
| `hog-dinner-island-3-2026-2027` | Wild Hog / Commission-Managed Land | new draft |
| `hog-holey-land-2-2026-2027-expanded` | Wild Hog / Wildlife Management Area (WMA) | new draft |
| `hog-holey-land-3-2026-2027-expanded` | Wild Hog / Commission-Managed Land | new draft |
| `hog-private-2026` | Wild Hog / Private Land | proposed revision of existing approved draft |
| `hog-rotenberger-2-2026-2027-expanded` | Wild Hog / Wildlife Management Area (WMA) | new draft |
| `hog-rotenberger-3-2026-2027-expanded` | Wild Hog / Commission-Managed Land | new draft |
| `python-corbett-2-2026-2027-expanded` | Burmese Python / Wildlife Management Area (WMA) | new draft |
| `python-corbett-3-2026-2027-expanded` | Burmese Python / Commission-Managed Land | new draft |
| `python-dinner-island-2-2026-2027` | Burmese Python / Wildlife Management Area (WMA) | new draft |
| `python-dinner-island-3-2026-2027` | Burmese Python / Commission-Managed Land | new draft |
| `python-fisheating-east-2-2026-2027` | Burmese Python / Wildlife Management Area (WMA) | new draft |
| `python-fisheating-east-3-2026-2027` | Burmese Python / Commission-Managed Land | new draft |
| `python-fisheating-west-2-2026-2027` | Burmese Python / Wildlife Management Area (WMA) | new draft |
| `python-fisheating-west-3-2026-2027` | Burmese Python / Commission-Managed Land | new draft |
| `python-holey-land-2-2026-2027-expanded` | Burmese Python / Wildlife Management Area (WMA) | new draft |
| `python-holey-land-3-2026-2027-expanded` | Burmese Python / Commission-Managed Land | new draft |
| `python-private-2026` | Burmese Python / Private Land | proposed revision of existing approved draft |
| `python-public-2-2026` | Burmese Python / Wildlife Management Area (WMA) | proposed revision of existing approved draft |
| `python-public-3-2026` | Burmese Python / Commission-Managed Land | proposed revision of existing approved draft |
| `python-rotenberger-2-2026-2027-expanded` | Burmese Python / Wildlife Management Area (WMA) | new draft |
| `python-rotenberger-3-2026-2027-expanded` | Burmese Python / Commission-Managed Land | new draft |
| `turkey-corbett-2-2026-2027-expanded` | Wild Turkey / Wildlife Management Area (WMA) | new draft |
| `turkey-corbett-3-2026-2027-expanded` | Wild Turkey / Commission-Managed Land | new draft |
| `turkey-dinner-island-2-2026-2027` | Wild Turkey / Wildlife Management Area (WMA) | new draft |
| `turkey-dinner-island-3-2026-2027` | Wild Turkey / Commission-Managed Land | new draft |
| `turkey-holey-land-2-2026-2027-expanded` | Wild Turkey / Wildlife Management Area (WMA) | new draft |
| `turkey-holey-land-3-2026-2027-expanded` | Wild Turkey / Commission-Managed Land | new draft |
| `turkey-private-fall-a-2026-2027` | Wild Turkey / Private Land | new draft |
| `turkey-private-fall-b-2026-2027` | Wild Turkey / Private Land | new draft |
| `turkey-private-fall-c-2026-2027` | Wild Turkey / Private Land | new draft |
| `turkey-private-fall-d-2026-2027` | Wild Turkey / Private Land | new draft |
| `turkey-private-spring-north_sr70-2026-2027` | Wild Turkey / Private Land | new draft |
| `turkey-private-spring-south_sr70-2026-2027` | Wild Turkey / Private Land | new draft |
| `turkey-rotenberger-2-2026-2027-expanded` | Wild Turkey / Wildlife Management Area (WMA) | new draft |
| `turkey-rotenberger-3-2026-2027-expanded` | Wild Turkey / Commission-Managed Land | new draft |

## Deer: J.W. Corbett / Wildlife Management Area (WMA), 2026-2027

Key: `deer-corbett-2-2026-2027`. proposed revision of existing approved draft.

Scope: managed_area: J. W. Corbett WMA

Review coverage: 2026-07-01 through 2027-06-30.

- [FWC J.W. Corbett 2026-2027 area brochure](https://app.myfwc.com/hgm/hgmsearch/wmad?brochureTitle=J.W.+Corbett) — checked 2026-10-12. Area dates, daily 1/annual 2 deer, antler/antlerless, methods, permits and named-area exceptions checked.
- [FWC recreational licenses and permits](https://myfwc.com/license/recreational/hunting/) — checked 2026-10-12. Hunting/deer and season permits checked; individual statutory exemptions require confirmation.
- [FWC deer harvest reporting](https://myfwc.com/hunting/deer/harvest-report/) — checked 2026-10-12. Log before moving and official reporting deadlines checked.
- [FWC current area notices](https://myfwc.com/recreation/notices/) — checked 2026-10-12. Current closure directory checked; notices can change after this data check.
- [FWC conditional license exemptions](https://myfwc.com/license/recreational/do-i-need-one/) — checked 2026-10-12. Checked youth, resident senior and conditional exemptions; quota rules remain separate.
- [FWC legal deer equipment](https://myfwc.com/hunting/regulations/taking-game/) — checked 2026-10-12. Checked broadhead, PCP, muzzleloader and prohibited ammunition requirements.
- [FWC hunter safety](https://myfwc.com/hunting/safety-education/) — checked 2026-10-12. Checked birth-date/age certification requirement and supervised deferral option.
- [FWC general hunting rules](https://myfwc.com/hunting/regulations/general-information/) — checked 2026-10-12. Checked deer shooting hours, public-land orange and dog restrictions.

### Corbett archery / Antlered deer

Dates: 2026-08-29 to 2026-09-20

Bag: Area daily limit 1 deer; area annual limit 2 across all seasons. Statewide annual 5 (maximum 2 antlerless) and possession 4 also apply.

Licenses: Hunting license, management area permit and deer permit unless exempt; no quota permit required. Archery season permit unless exempt.

Methods: Bows only; crossbows, airbows and draw-lock bows prohibited except qualifying disability permits.

- Antlered deer: at least 3 one-inch points on one antler or main beam at least 10 inches; confirm age exceptions in the brochure.
- Bruce Bowman archery area is bows-only across seasons except the brochure's disability exemptions.
- Check current closures, check-station duties, vehicle access and maps. An OHV hunting permit is required for relevant off-road hunting vehicle use from July 31, 2026.

### Corbett archery / Antlerless deer

Dates: 2026-09-12 to 2026-09-20

Bag: Area daily limit 1 deer; area annual limit 2 across all seasons. Statewide annual 5 (maximum 2 antlerless) and possession 4 also apply.

Licenses: Hunting license, management area permit and deer permit unless exempt; no quota permit required. Archery season permit unless exempt.

Methods: Bows only, subject to the brochure's disability exemptions.

- Antlered deer: at least 3 one-inch points on one antler or main beam at least 10 inches; confirm age exceptions in the brochure.
- Bruce Bowman archery area is bows-only across seasons except the brochure's disability exemptions.
- Check current closures, check-station duties, vehicle access and maps. An OHV hunting permit is required for relevant off-road hunting vehicle use from July 31, 2026.

### Corbett muzzleloading gun / Antlered deer only

Dates: 2026-10-03 to 2026-10-18

Bag: Area daily limit 1 deer; area annual limit 2 across all seasons. Statewide annual 5 (maximum 2 antlerless) and possession 4 also apply.

Licenses: Hunting license, management area permit and deer permit unless exempt; no quota permit required. Muzzleloading gun season permit unless exempt, including Bruce Bowman archery-area hunters.

Methods: Muzzleloaders only except bows in Bruce Bowman archery area; follow area-specific exceptions.

- Antlered deer: at least 3 one-inch points on one antler or main beam at least 10 inches; confirm age exceptions in the brochure.
- Bruce Bowman archery area is bows-only across seasons except the brochure's disability exemptions.
- Check current closures, check-station duties, vehicle access and maps. An OHV hunting permit is required for relevant off-road hunting vehicle use from July 31, 2026.

### Corbett general gun / Antlered deer only

Dates: 2026-11-07 to 2027-01-03

Bag: Area daily limit 1 deer; area annual limit 2 across all seasons. Statewide annual 5 (maximum 2 antlerless) and possession 4 also apply.

Licenses: Hunting license, management area permit and deer permit unless exempt; no quota permit required. WMA deer-dog permit required if hunting deer with dogs; no exemptions for that permit.

Methods: Lawful general-gun methods subject to brochure restrictions; dogs prohibited in designated still-hunt areas; Bruce Bowman remains bows-only.

- Antlered deer: at least 3 one-inch points on one antler or main beam at least 10 inches; confirm age exceptions in the brochure.
- Bruce Bowman archery area is bows-only across seasons except the brochure's disability exemptions.
- Check current closures, check-station duties, vehicle access and maps. An OHV hunting permit is required for relevant off-road hunting vehicle use from July 31, 2026.

Conditions for the whole scope:

- Representative WMA coverage is J.W. Corbett only. Other WMA deer regulations require a separately reviewed area brochure.
- Use official FWC harvest reporting in addition to this personal log.
- Check the linked FWC area notices for temporary closures; this local dataset does not poll live closures.
- License/permit exemptions require the relevant proof and conditions: youth under 16; Florida residents age 65+; qualifying homestead hunting in the county of residence; Florida residents holding the qualifying disability license; qualifying resident military members home on leave for at most 30 days with orders; authorized military/disabled-veteran events; and qualifying licensed-preserve patrons. Check the official exemption page. An exemption does not change season dates, bag limits, access permission or harvest reporting.
- Ordinary deer shooting hours are one-half hour before sunrise through one-half hour after sunset; specific area restrictions still apply.
- Arrows/bolts for deer require broadheads at least 7/8 inch wide. Deer PCP projectiles must meet the .30-caliber requirement; rimfire and nonexpanding full-metal-case ammunition are prohibited.
- Deer muzzleloaders firing one bullet must be at least .30 caliber; guns firing multiple balls must be 20 gauge or larger. Season-specific method limits still apply.
- Hunters age 16+ born on or after June 1, 1975 need hunter-safety certification before buying a hunting license, unless using a lawful supervised deferral.
- Deer hunters and companions on public land need at least 500 square inches of fluorescent orange above the waist, except during archery-only season.

## Deer: J.W. Corbett / Commission-Managed Land, 2026-2027

Key: `deer-corbett-3-2026-2027`. proposed revision of existing approved draft.

Scope: managed_area: J. W. Corbett WMA

Review coverage: 2026-07-01 through 2027-06-30.

- [FWC J.W. Corbett 2026-2027 area brochure](https://app.myfwc.com/hgm/hgmsearch/wmad?brochureTitle=J.W.+Corbett) — checked 2026-10-12. Area dates, daily 1/annual 2 deer, antler/antlerless, methods, permits and named-area exceptions checked.
- [FWC recreational licenses and permits](https://myfwc.com/license/recreational/hunting/) — checked 2026-10-12. Hunting/deer and season permits checked; individual statutory exemptions require confirmation.
- [FWC deer harvest reporting](https://myfwc.com/hunting/deer/harvest-report/) — checked 2026-10-12. Log before moving and official reporting deadlines checked.
- [FWC current area notices](https://myfwc.com/recreation/notices/) — checked 2026-10-12. Current closure directory checked; notices can change after this data check.
- [FWC conditional license exemptions](https://myfwc.com/license/recreational/do-i-need-one/) — checked 2026-10-12. Checked youth, resident senior and conditional exemptions; quota rules remain separate.
- [FWC legal deer equipment](https://myfwc.com/hunting/regulations/taking-game/) — checked 2026-10-12. Checked broadhead, PCP, muzzleloader and prohibited ammunition requirements.
- [FWC hunter safety](https://myfwc.com/hunting/safety-education/) — checked 2026-10-12. Checked birth-date/age certification requirement and supervised deferral option.
- [FWC general hunting rules](https://myfwc.com/hunting/regulations/general-information/) — checked 2026-10-12. Checked deer shooting hours, public-land orange and dog restrictions.

### Corbett archery / Antlered deer

Dates: 2026-08-29 to 2026-09-20

Bag: Area daily limit 1 deer; area annual limit 2 across all seasons. Statewide annual 5 (maximum 2 antlerless) and possession 4 also apply.

Licenses: Hunting license, management area permit and deer permit unless exempt; no quota permit required. Archery season permit unless exempt.

Methods: Bows only; crossbows, airbows and draw-lock bows prohibited except qualifying disability permits.

- Antlered deer: at least 3 one-inch points on one antler or main beam at least 10 inches; confirm age exceptions in the brochure.
- Bruce Bowman archery area is bows-only across seasons except the brochure's disability exemptions.
- Check current closures, check-station duties, vehicle access and maps. An OHV hunting permit is required for relevant off-road hunting vehicle use from July 31, 2026.

### Corbett archery / Antlerless deer

Dates: 2026-09-12 to 2026-09-20

Bag: Area daily limit 1 deer; area annual limit 2 across all seasons. Statewide annual 5 (maximum 2 antlerless) and possession 4 also apply.

Licenses: Hunting license, management area permit and deer permit unless exempt; no quota permit required. Archery season permit unless exempt.

Methods: Bows only, subject to the brochure's disability exemptions.

- Antlered deer: at least 3 one-inch points on one antler or main beam at least 10 inches; confirm age exceptions in the brochure.
- Bruce Bowman archery area is bows-only across seasons except the brochure's disability exemptions.
- Check current closures, check-station duties, vehicle access and maps. An OHV hunting permit is required for relevant off-road hunting vehicle use from July 31, 2026.

### Corbett muzzleloading gun / Antlered deer only

Dates: 2026-10-03 to 2026-10-18

Bag: Area daily limit 1 deer; area annual limit 2 across all seasons. Statewide annual 5 (maximum 2 antlerless) and possession 4 also apply.

Licenses: Hunting license, management area permit and deer permit unless exempt; no quota permit required. Muzzleloading gun season permit unless exempt, including Bruce Bowman archery-area hunters.

Methods: Muzzleloaders only except bows in Bruce Bowman archery area; follow area-specific exceptions.

- Antlered deer: at least 3 one-inch points on one antler or main beam at least 10 inches; confirm age exceptions in the brochure.
- Bruce Bowman archery area is bows-only across seasons except the brochure's disability exemptions.
- Check current closures, check-station duties, vehicle access and maps. An OHV hunting permit is required for relevant off-road hunting vehicle use from July 31, 2026.

### Corbett general gun / Antlered deer only

Dates: 2026-11-07 to 2027-01-03

Bag: Area daily limit 1 deer; area annual limit 2 across all seasons. Statewide annual 5 (maximum 2 antlerless) and possession 4 also apply.

Licenses: Hunting license, management area permit and deer permit unless exempt; no quota permit required. WMA deer-dog permit required if hunting deer with dogs; no exemptions for that permit.

Methods: Lawful general-gun methods subject to brochure restrictions; dogs prohibited in designated still-hunt areas; Bruce Bowman remains bows-only.

- Antlered deer: at least 3 one-inch points on one antler or main beam at least 10 inches; confirm age exceptions in the brochure.
- Bruce Bowman archery area is bows-only across seasons except the brochure's disability exemptions.
- Check current closures, check-station duties, vehicle access and maps. An OHV hunting permit is required for relevant off-road hunting vehicle use from July 31, 2026.

Conditions for the whole scope:

- Representative WMA coverage is J.W. Corbett only. Other WMA deer regulations require a separately reviewed area brochure.
- Use official FWC harvest reporting in addition to this personal log.
- Check the linked FWC area notices for temporary closures; this local dataset does not poll live closures.
- License/permit exemptions require the relevant proof and conditions: youth under 16; Florida residents age 65+; qualifying homestead hunting in the county of residence; Florida residents holding the qualifying disability license; qualifying resident military members home on leave for at most 30 days with orders; authorized military/disabled-veteran events; and qualifying licensed-preserve patrons. Check the official exemption page. An exemption does not change season dates, bag limits, access permission or harvest reporting.
- Ordinary deer shooting hours are one-half hour before sunrise through one-half hour after sunset; specific area restrictions still apply.
- Arrows/bolts for deer require broadheads at least 7/8 inch wide. Deer PCP projectiles must meet the .30-caliber requirement; rimfire and nonexpanding full-metal-case ammunition are prohibited.
- Deer muzzleloaders firing one bullet must be at least .30 caliber; guns firing multiple balls must be 20 gauge or larger. Season-specific method limits still apply.
- Hunters age 16+ born on or after June 1, 1975 need hunter-safety certification before buying a hunting license, unless using a lawful supervised deferral.
- Deer hunters and companions on public land need at least 500 square inches of fluorescent orange above the waist, except during archery-only season.

## White Tailed Deer: Dinner Island Ranch / Wildlife Management Area (WMA), 2026-2027

Key: `deer-dinner-island-2-2026-2027`. new draft.

Scope: managed_area: Dinner Island Ranch WMA

Review coverage: 2026-07-01 through 2027-06-30.

- [FWC Dinner Island Ranch 2026-2027 area brochure](https://app.myfwc.com/hgm/hgmsearch/wmad?brochureTitle=Dinner+Island+Ranch) — checked 2026-10-12. Read complete interactive brochure: season dates, antlered-only deer, quota/shared bags, turkey restrictions, hog methods, access and check-station waiver.
- [FWC Dinner Island Ranch 2026-2027 hunt calendar](https://app.myfwc.com/hsc/wmahuntcalendar/?areaName=dinner+island+ranch) — checked 2026-10-12. Corroborated every archery, muzzleloading, family, general gun, small-game and youth/spring turkey endpoint; Caracara Unit excluded.
- [FWC hunting licenses and permits](https://myfwc.com/license/recreational/hunting/) — checked 2026-10-12. Species/season permits and individual exemptions are separate from no-exemption area quota permits.
- [FWC taking game methods](https://myfwc.com/hunting/regulations/taking-game/) — checked 2026-10-12. Deer muzzleloader minimum .30-caliber single bullet/20-gauge multiple balls and deer/turkey 7/8-inch broadheads checked; area-specific stricter methods retained.

### Dinner Island Ranch archery / Antlered deer only

Dates: 2026-08-07 to 2026-08-10; 2026-08-14 to 2026-08-17; 2026-08-21 to 2026-08-24; 2026-08-28 to 2026-08-31

Bag: 1 antlered deer per quota permit (shared with any permitted guest). Statewide daily 2, possession 4 and annual 5 deer limits also apply.

Licenses: Hunting license, management area permit and deer permit required unless exempt. Archery season permit required unless exempt. A quota permit for this area and hunt is required; no quota exemptions.

Methods: Bows only. Crossbows, airbows and draw-lock bows are prohibited except the brochure's Persons With Disabilities Crossbow Permit exception.

- Antlered deer only: at least 3 points, each at least 1 inch, on one antler, or a main beam of at least 10 inches. Youth under 16 have the statewide one-deer annual antler-point exception; a 5-inch antler is still required. Antlerless deer are not authorized in these area seasons.
- Do not take spotted fawns or swimming deer. Deer hunters and companions need 500 square inches of fluorescent orange above the waist, except bow-and-arrow hunting during archery season.
- Deer must be logged before moving and reported to FWC within 24 hours, or before an earlier processing, transfer or out-of-state deadline. The shared quota bag is not a separate allowance for each guest.
- Deer muzzleloaders firing a single bullet must be at least .30 caliber; those firing 2 or more balls must be at least 20 gauge. Deer arrows and bolts require broadheads at least 7/8 inch wide. No rimfire or non-expanding full-metal-jacket ammunition for deer.
- Quota permits are nontransferable and require positive identification except for youth. Where a guest permit is allowed, one guest and the host must enter/exit together, share a street-legal vehicle and hunt with the host present. Deer and turkey limits are shared per quota permit.

### Dinner Island Ranch muzzleloading gun / Antlered deer only

Dates: 2026-09-11 to 2026-09-13

Bag: 1 antlered deer per quota permit (shared with any permitted guest). Statewide daily 2, possession 4 and annual 5 deer limits also apply.

Licenses: Hunting license, management area permit and deer permit required unless exempt. Muzzleloading gun season permit required unless exempt. A quota permit for this area and hunt is required; no quota exemptions.

Methods: Muzzleloading guns only for deer or hog; ordinary archery equipment is prohibited during this season.

- Antlered deer only: at least 3 points, each at least 1 inch, on one antler, or a main beam of at least 10 inches. Youth under 16 have the statewide one-deer annual antler-point exception; a 5-inch antler is still required. Antlerless deer are not authorized in these area seasons.
- Do not take spotted fawns or swimming deer. Deer hunters and companions need 500 square inches of fluorescent orange above the waist, except bow-and-arrow hunting during archery season.
- Deer must be logged before moving and reported to FWC within 24 hours, or before an earlier processing, transfer or out-of-state deadline. The shared quota bag is not a separate allowance for each guest.
- Deer muzzleloaders firing a single bullet must be at least .30 caliber; those firing 2 or more balls must be at least 20 gauge. Deer arrows and bolts require broadheads at least 7/8 inch wide. No rimfire or non-expanding full-metal-jacket ammunition for deer.
- Quota permits are nontransferable and require positive identification except for youth. Where a guest permit is allowed, one guest and the host must enter/exit together, share a street-legal vehicle and hunt with the host present. Deer and turkey limits are shared per quota permit.

### Dinner Island Ranch family hunt / Antlered deer only

Dates: 2026-09-19 to 2026-09-20; 2026-10-17 to 2026-10-18

Bag: 2 antlered deer per family quota permit, but no more than 1 per person; statewide daily, possession and annual limits still apply.

Licenses: Hunting license, management area permit and deer permit required unless exempt. A quota permit for this area and hunt is required; no quota exemptions.

Methods: Lawful shotguns, rifles, muzzleloading guns, pistols, airguns, bows and crossbows, subject to the area brochure. For deer, no rimfire or non-expanding full-metal-jacket ammunition; PCP airguns must propel a bolt, arrow or bullet of at least .30 caliber. Deer muzzleloaders require a single bullet at least .30 caliber, or at least 20 gauge when firing 2 or more balls.

- Antlered deer only: at least 3 points, each at least 1 inch, on one antler, or a main beam of at least 10 inches. Youth under 16 have the statewide one-deer annual antler-point exception; a 5-inch antler is still required. Antlerless deer are not authorized in these area seasons.
- Do not take spotted fawns or swimming deer. Deer hunters and companions need 500 square inches of fluorescent orange above the waist, except bow-and-arrow hunting during archery season.
- Deer must be logged before moving and reported to FWC within 24 hours, or before an earlier processing, transfer or out-of-state deadline. The shared quota bag is not a separate allowance for each guest.
- Deer muzzleloaders firing a single bullet must be at least .30 caliber; those firing 2 or more balls must be at least 20 gauge. Deer arrows and bolts require broadheads at least 7/8 inch wide. No rimfire or non-expanding full-metal-jacket ammunition for deer.
- Quota permits are nontransferable and require positive identification except for youth. Where a guest permit is allowed, one guest and the host must enter/exit together, share a street-legal vehicle and hunt with the host present. Deer and turkey limits are shared per quota permit.
- Family hunt: the quota holder must be at least 18 and directly supervise up to 2 youth ages 8-15. The adult may hunt only with at least one youth present. Guest hunting permits are not allowed for this hunt.

### Dinner Island Ranch general gun / Antlered deer only

Dates: 2026-09-25 to 2026-09-27; 2026-10-02 to 2026-10-04; 2026-10-09 to 2026-10-11

Bag: 1 antlered deer per quota permit (shared with any permitted guest). Statewide daily 2, possession 4 and annual 5 deer limits also apply.

Licenses: Hunting license, management area permit and deer permit required unless exempt. A quota permit for this area and hunt is required; no quota exemptions.

Methods: Lawful shotguns, rifles, muzzleloading guns, pistols, airguns, bows and crossbows, subject to the area brochure. For deer, no rimfire or non-expanding full-metal-jacket ammunition; PCP airguns must propel a bolt, arrow or bullet of at least .30 caliber. Deer muzzleloaders require a single bullet at least .30 caliber, or at least 20 gauge when firing 2 or more balls.

- Antlered deer only: at least 3 points, each at least 1 inch, on one antler, or a main beam of at least 10 inches. Youth under 16 have the statewide one-deer annual antler-point exception; a 5-inch antler is still required. Antlerless deer are not authorized in these area seasons.
- Do not take spotted fawns or swimming deer. Deer hunters and companions need 500 square inches of fluorescent orange above the waist, except bow-and-arrow hunting during archery season.
- Deer must be logged before moving and reported to FWC within 24 hours, or before an earlier processing, transfer or out-of-state deadline. The shared quota bag is not a separate allowance for each guest.
- Deer muzzleloaders firing a single bullet must be at least .30 caliber; those firing 2 or more balls must be at least 20 gauge. Deer arrows and bolts require broadheads at least 7/8 inch wide. No rimfire or non-expanding full-metal-jacket ammunition for deer.
- Quota permits are nontransferable and require positive identification except for youth. Where a guest permit is allowed, one guest and the host must enter/exit together, share a street-legal vehicle and hunt with the host present. Deer and turkey limits are shared per quota permit.

Conditions for the whole scope:

- Dinner Island Ranch coverage excludes the separately regulated Caracara Unit. Enter and exit at the designated entrance; posted closed areas remain closed.
- The 2026-2027 Attention Hunters notice says there is no operating check station and waives all check-station duties. Deer and turkey must still be logged before moving and officially reported within 24 hours. HuntIt does not submit the FWC report.
- Vehicles may use named and numbered roads only, except valid Alternative Mobility Permit allowances. Vehicles are prohibited from 1.5 hours after sunset until 1.5 hours before sunrise, except camping-permit holders and guests accessing their designated campsite.
- Airboats, ATVs, swamp buggies, tracked vehicles and unregistered motorcycles are prohibited, except quota hunters and their guest permit holders may use ATVs and swamp buggies on named/numbered roads during their permitted archery, muzzleloading gun, family or general gun hunt. This exception does not authorize off-road travel.
- Camping requires an FWC permit and is limited to designated campgrounds. Horses are prohibited during archery, muzzleloading gun, family, general gun and spring turkey seasons; otherwise use designated roads.
- On posted dove fields, hunting during dove season is limited to Saturdays; otherwise only hunting allowed by the applicable area season is authorized. Check the brochure map and current closures before selecting a hunting site.
- No hunting over bait, night gun hunting, fully automatic firearms or centerfire semiautomatic rifles with magazines holding more than 5 rounds. The brochure's ammunition, equipment and closed-area restrictions apply.
- Ordinary shooting hours are half an hour before sunrise through half an hour after sunset. Turkey shooting ends at sunset.
- Dogs may not hunt deer, wild hog or furbearers; leashed dogs may trail wounded game under the brochure's conditions. No dogs may pursue non-native reptiles.
- License/season-permit exemptions do not waive a quota permit marked no exemptions. Check hunter-safety requirements and individual exemptions in the full brochure.
- Nonresident hunters taking native game need the applicable annual hunting license unless exempt. A hunting license is not required when hunting wild hog or removing python within the stated exception.

## White Tailed Deer: Dinner Island Ranch / Commission-Managed Land, 2026-2027

Key: `deer-dinner-island-3-2026-2027`. new draft.

Scope: managed_area: Dinner Island Ranch WMA

Review coverage: 2026-07-01 through 2027-06-30.

- [FWC Dinner Island Ranch 2026-2027 area brochure](https://app.myfwc.com/hgm/hgmsearch/wmad?brochureTitle=Dinner+Island+Ranch) — checked 2026-10-12. Read complete interactive brochure: season dates, antlered-only deer, quota/shared bags, turkey restrictions, hog methods, access and check-station waiver.
- [FWC Dinner Island Ranch 2026-2027 hunt calendar](https://app.myfwc.com/hsc/wmahuntcalendar/?areaName=dinner+island+ranch) — checked 2026-10-12. Corroborated every archery, muzzleloading, family, general gun, small-game and youth/spring turkey endpoint; Caracara Unit excluded.
- [FWC hunting licenses and permits](https://myfwc.com/license/recreational/hunting/) — checked 2026-10-12. Species/season permits and individual exemptions are separate from no-exemption area quota permits.
- [FWC taking game methods](https://myfwc.com/hunting/regulations/taking-game/) — checked 2026-10-12. Deer muzzleloader minimum .30-caliber single bullet/20-gauge multiple balls and deer/turkey 7/8-inch broadheads checked; area-specific stricter methods retained.

### Dinner Island Ranch archery / Antlered deer only

Dates: 2026-08-07 to 2026-08-10; 2026-08-14 to 2026-08-17; 2026-08-21 to 2026-08-24; 2026-08-28 to 2026-08-31

Bag: 1 antlered deer per quota permit (shared with any permitted guest). Statewide daily 2, possession 4 and annual 5 deer limits also apply.

Licenses: Hunting license, management area permit and deer permit required unless exempt. Archery season permit required unless exempt. A quota permit for this area and hunt is required; no quota exemptions.

Methods: Bows only. Crossbows, airbows and draw-lock bows are prohibited except the brochure's Persons With Disabilities Crossbow Permit exception.

- Antlered deer only: at least 3 points, each at least 1 inch, on one antler, or a main beam of at least 10 inches. Youth under 16 have the statewide one-deer annual antler-point exception; a 5-inch antler is still required. Antlerless deer are not authorized in these area seasons.
- Do not take spotted fawns or swimming deer. Deer hunters and companions need 500 square inches of fluorescent orange above the waist, except bow-and-arrow hunting during archery season.
- Deer must be logged before moving and reported to FWC within 24 hours, or before an earlier processing, transfer or out-of-state deadline. The shared quota bag is not a separate allowance for each guest.
- Deer muzzleloaders firing a single bullet must be at least .30 caliber; those firing 2 or more balls must be at least 20 gauge. Deer arrows and bolts require broadheads at least 7/8 inch wide. No rimfire or non-expanding full-metal-jacket ammunition for deer.
- Quota permits are nontransferable and require positive identification except for youth. Where a guest permit is allowed, one guest and the host must enter/exit together, share a street-legal vehicle and hunt with the host present. Deer and turkey limits are shared per quota permit.

### Dinner Island Ranch muzzleloading gun / Antlered deer only

Dates: 2026-09-11 to 2026-09-13

Bag: 1 antlered deer per quota permit (shared with any permitted guest). Statewide daily 2, possession 4 and annual 5 deer limits also apply.

Licenses: Hunting license, management area permit and deer permit required unless exempt. Muzzleloading gun season permit required unless exempt. A quota permit for this area and hunt is required; no quota exemptions.

Methods: Muzzleloading guns only for deer or hog; ordinary archery equipment is prohibited during this season.

- Antlered deer only: at least 3 points, each at least 1 inch, on one antler, or a main beam of at least 10 inches. Youth under 16 have the statewide one-deer annual antler-point exception; a 5-inch antler is still required. Antlerless deer are not authorized in these area seasons.
- Do not take spotted fawns or swimming deer. Deer hunters and companions need 500 square inches of fluorescent orange above the waist, except bow-and-arrow hunting during archery season.
- Deer must be logged before moving and reported to FWC within 24 hours, or before an earlier processing, transfer or out-of-state deadline. The shared quota bag is not a separate allowance for each guest.
- Deer muzzleloaders firing a single bullet must be at least .30 caliber; those firing 2 or more balls must be at least 20 gauge. Deer arrows and bolts require broadheads at least 7/8 inch wide. No rimfire or non-expanding full-metal-jacket ammunition for deer.
- Quota permits are nontransferable and require positive identification except for youth. Where a guest permit is allowed, one guest and the host must enter/exit together, share a street-legal vehicle and hunt with the host present. Deer and turkey limits are shared per quota permit.

### Dinner Island Ranch family hunt / Antlered deer only

Dates: 2026-09-19 to 2026-09-20; 2026-10-17 to 2026-10-18

Bag: 2 antlered deer per family quota permit, but no more than 1 per person; statewide daily, possession and annual limits still apply.

Licenses: Hunting license, management area permit and deer permit required unless exempt. A quota permit for this area and hunt is required; no quota exemptions.

Methods: Lawful shotguns, rifles, muzzleloading guns, pistols, airguns, bows and crossbows, subject to the area brochure. For deer, no rimfire or non-expanding full-metal-jacket ammunition; PCP airguns must propel a bolt, arrow or bullet of at least .30 caliber. Deer muzzleloaders require a single bullet at least .30 caliber, or at least 20 gauge when firing 2 or more balls.

- Antlered deer only: at least 3 points, each at least 1 inch, on one antler, or a main beam of at least 10 inches. Youth under 16 have the statewide one-deer annual antler-point exception; a 5-inch antler is still required. Antlerless deer are not authorized in these area seasons.
- Do not take spotted fawns or swimming deer. Deer hunters and companions need 500 square inches of fluorescent orange above the waist, except bow-and-arrow hunting during archery season.
- Deer must be logged before moving and reported to FWC within 24 hours, or before an earlier processing, transfer or out-of-state deadline. The shared quota bag is not a separate allowance for each guest.
- Deer muzzleloaders firing a single bullet must be at least .30 caliber; those firing 2 or more balls must be at least 20 gauge. Deer arrows and bolts require broadheads at least 7/8 inch wide. No rimfire or non-expanding full-metal-jacket ammunition for deer.
- Quota permits are nontransferable and require positive identification except for youth. Where a guest permit is allowed, one guest and the host must enter/exit together, share a street-legal vehicle and hunt with the host present. Deer and turkey limits are shared per quota permit.
- Family hunt: the quota holder must be at least 18 and directly supervise up to 2 youth ages 8-15. The adult may hunt only with at least one youth present. Guest hunting permits are not allowed for this hunt.

### Dinner Island Ranch general gun / Antlered deer only

Dates: 2026-09-25 to 2026-09-27; 2026-10-02 to 2026-10-04; 2026-10-09 to 2026-10-11

Bag: 1 antlered deer per quota permit (shared with any permitted guest). Statewide daily 2, possession 4 and annual 5 deer limits also apply.

Licenses: Hunting license, management area permit and deer permit required unless exempt. A quota permit for this area and hunt is required; no quota exemptions.

Methods: Lawful shotguns, rifles, muzzleloading guns, pistols, airguns, bows and crossbows, subject to the area brochure. For deer, no rimfire or non-expanding full-metal-jacket ammunition; PCP airguns must propel a bolt, arrow or bullet of at least .30 caliber. Deer muzzleloaders require a single bullet at least .30 caliber, or at least 20 gauge when firing 2 or more balls.

- Antlered deer only: at least 3 points, each at least 1 inch, on one antler, or a main beam of at least 10 inches. Youth under 16 have the statewide one-deer annual antler-point exception; a 5-inch antler is still required. Antlerless deer are not authorized in these area seasons.
- Do not take spotted fawns or swimming deer. Deer hunters and companions need 500 square inches of fluorescent orange above the waist, except bow-and-arrow hunting during archery season.
- Deer must be logged before moving and reported to FWC within 24 hours, or before an earlier processing, transfer or out-of-state deadline. The shared quota bag is not a separate allowance for each guest.
- Deer muzzleloaders firing a single bullet must be at least .30 caliber; those firing 2 or more balls must be at least 20 gauge. Deer arrows and bolts require broadheads at least 7/8 inch wide. No rimfire or non-expanding full-metal-jacket ammunition for deer.
- Quota permits are nontransferable and require positive identification except for youth. Where a guest permit is allowed, one guest and the host must enter/exit together, share a street-legal vehicle and hunt with the host present. Deer and turkey limits are shared per quota permit.

Conditions for the whole scope:

- Dinner Island Ranch coverage excludes the separately regulated Caracara Unit. Enter and exit at the designated entrance; posted closed areas remain closed.
- The 2026-2027 Attention Hunters notice says there is no operating check station and waives all check-station duties. Deer and turkey must still be logged before moving and officially reported within 24 hours. HuntIt does not submit the FWC report.
- Vehicles may use named and numbered roads only, except valid Alternative Mobility Permit allowances. Vehicles are prohibited from 1.5 hours after sunset until 1.5 hours before sunrise, except camping-permit holders and guests accessing their designated campsite.
- Airboats, ATVs, swamp buggies, tracked vehicles and unregistered motorcycles are prohibited, except quota hunters and their guest permit holders may use ATVs and swamp buggies on named/numbered roads during their permitted archery, muzzleloading gun, family or general gun hunt. This exception does not authorize off-road travel.
- Camping requires an FWC permit and is limited to designated campgrounds. Horses are prohibited during archery, muzzleloading gun, family, general gun and spring turkey seasons; otherwise use designated roads.
- On posted dove fields, hunting during dove season is limited to Saturdays; otherwise only hunting allowed by the applicable area season is authorized. Check the brochure map and current closures before selecting a hunting site.
- No hunting over bait, night gun hunting, fully automatic firearms or centerfire semiautomatic rifles with magazines holding more than 5 rounds. The brochure's ammunition, equipment and closed-area restrictions apply.
- Ordinary shooting hours are half an hour before sunrise through half an hour after sunset. Turkey shooting ends at sunset.
- Dogs may not hunt deer, wild hog or furbearers; leashed dogs may trail wounded game under the brochure's conditions. No dogs may pursue non-native reptiles.
- License/season-permit exemptions do not waive a quota permit marked no exemptions. Check hunter-safety requirements and individual exemptions in the full brochure.
- Nonresident hunters taking native game need the applicable annual hunting license unless exempt. A hunting license is not required when hunting wild hog or removing python within the stated exception.

## White Tailed Deer: Holey Land WMA / Wildlife Management Area (WMA), 2026-2027 expansion

Key: `deer-holey-land-2-2026-2027-expanded`. new draft.

Scope: managed_area: Holey Land WMA

Review coverage: 2026-07-01 through 2027-06-30.

- [FWC Holey Land WMA 2026-2027 regulations and map](https://app.myfwc.com/hgm/hgmsearch/wmad?brochureTitle=Holey+Land) — checked 2026-10-12. Interactive brochure checked: area dates, legal species, bag limits, methods, permits, access and exceptions; PDF map available on the same page.
- [FWC hunting licenses and permits](https://myfwc.com/license/recreational/hunting/) — checked 2026-10-12. General license, management-area and season permits; brochure exemptions and area-specific quota restrictions retained.
- [FWC legal resident-game equipment](https://myfwc.com/hunting/regulations/taking-game/) — checked 2026-10-12. Checked broadhead minimum width, species-specific PCP minimums and deer muzzleloader design requirements; area season-method restrictions remain controlling.

### Archery / Antlered deer only

Dates: 2026-08-08 to 2026-08-30

Bag: Area season limit 1 antlered deer during archery, muzzleloading gun and general gun-walk seasons. Statewide annual limit 5 deer, including no more than 2 antlerless; daily 2 and possession 4 also apply.

Licenses: Hunting license, management area permit and deer permit required unless exempt. Nonresident game hunters require an annual hunting license. Archery season permit required unless exempt. No quota permit required for this listed season.

Methods: Bows only; crossbows, airbows and draw-lock bows require the brochure's Persons With Disabilities Crossbow Permit exception.

- Entry/exit is limited to the L-5 and Miami Canal levees. Hunting on roads, ramps, parking/camping areas, levees or adjacent powerline pads, and gun hunting on/from/across levees, is prohibited.
- Motorized use, scouting periods, flags and access routes are restricted. During general gun-vehicle season walk-hunting is closed and only vehicles authorized by its permits may operate; consult the map and permit conditions.
- Dogs may hunt deer/hog only during general gun-vehicle season; deer-dog hunting needs a valid WMA deer-dog permit, and dogs pursuing deer/hog need remote tracking and correction devices.
- When weekend check stations are staffed, check deer at the L-5 levee station before quartering, dismembering or removing them. General gun-vehicle deer must be immediately tagged with the FWC antlered deer tag.
- Antlered deer must have at least one antler 5 inches or longer with at least 2 points, each at least 1 inch. Youth under 16 have the statewide one-deer annual antler-point exception, still requiring a 5-inch antler. Antlerless deer and spotted fawns are not authorized by these area seasons.
- Arrows and bolts used for deer must have broadheads at least 7/8 inch wide. Any otherwise-authorized deer PCP airgun projectile must satisfy the statewide .30-caliber minimum; this does not authorize PCP equipment during bows-only or muzzleloader-only seasons.
- Muzzleloaders used for deer must be at least .30 caliber for a single bullet or at least 20 gauge when firing 2 or more balls.
- Log harvested deer before moving them and report to FWC within 24 hours of recovery, in addition to the area's check-station duties.

### Muzzleloading gun / Antlered deer only

Dates: 2026-09-05 to 2026-09-13

Bag: Area season limit 1 antlered deer during archery, muzzleloading gun and general gun-walk seasons. Statewide annual limit 5 deer, including no more than 2 antlerless; daily 2 and possession 4 also apply.

Licenses: Hunting license, management area permit and deer permit required unless exempt. Nonresident game hunters require an annual hunting license. Muzzleloading gun season permit required unless exempt. No quota permit required for this listed season.

Methods: Muzzleloading guns only for deer or hog; ordinary archery equipment is prohibited.

- Entry/exit is limited to the L-5 and Miami Canal levees. Hunting on roads, ramps, parking/camping areas, levees or adjacent powerline pads, and gun hunting on/from/across levees, is prohibited.
- Motorized use, scouting periods, flags and access routes are restricted. During general gun-vehicle season walk-hunting is closed and only vehicles authorized by its permits may operate; consult the map and permit conditions.
- Dogs may hunt deer/hog only during general gun-vehicle season; deer-dog hunting needs a valid WMA deer-dog permit, and dogs pursuing deer/hog need remote tracking and correction devices.
- When weekend check stations are staffed, check deer at the L-5 levee station before quartering, dismembering or removing them. General gun-vehicle deer must be immediately tagged with the FWC antlered deer tag.
- Antlered deer must have at least one antler 5 inches or longer with at least 2 points, each at least 1 inch. Youth under 16 have the statewide one-deer annual antler-point exception, still requiring a 5-inch antler. Antlerless deer and spotted fawns are not authorized by these area seasons.
- Arrows and bolts used for deer must have broadheads at least 7/8 inch wide. Any otherwise-authorized deer PCP airgun projectile must satisfy the statewide .30-caliber minimum; this does not authorize PCP equipment during bows-only or muzzleloader-only seasons.
- Muzzleloaders used for deer must be at least .30 caliber for a single bullet or at least 20 gauge when firing 2 or more balls.
- Log harvested deer before moving them and report to FWC within 24 hours of recovery, in addition to the area's check-station duties.

### General gun-walk / Antlered deer only

Dates: 2026-10-03 to 2026-10-18

Bag: Area season limit 1 antlered deer during archery, muzzleloading gun and general gun-walk seasons. Statewide annual limit 5 deer, including no more than 2 antlerless; daily 2 and possession 4 also apply.

Licenses: Hunting license, management area permit and deer permit required unless exempt. Nonresident game hunters require an annual hunting license. No quota permit required for this listed season.

Methods: Lawful shotguns, rifles, muzzleloading guns, pistols, airguns, bows and crossbows, subject to brochure restrictions. No rimfire or non-expanding full-metal-jacket ammunition for deer; PCP airguns must propel a bolt, arrow or bullet of at least .30 caliber.

- Entry/exit is limited to the L-5 and Miami Canal levees. Hunting on roads, ramps, parking/camping areas, levees or adjacent powerline pads, and gun hunting on/from/across levees, is prohibited.
- Motorized use, scouting periods, flags and access routes are restricted. During general gun-vehicle season walk-hunting is closed and only vehicles authorized by its permits may operate; consult the map and permit conditions.
- Dogs may hunt deer/hog only during general gun-vehicle season; deer-dog hunting needs a valid WMA deer-dog permit, and dogs pursuing deer/hog need remote tracking and correction devices.
- When weekend check stations are staffed, check deer at the L-5 levee station before quartering, dismembering or removing them. General gun-vehicle deer must be immediately tagged with the FWC antlered deer tag.
- Antlered deer must have at least one antler 5 inches or longer with at least 2 points, each at least 1 inch. Youth under 16 have the statewide one-deer annual antler-point exception, still requiring a 5-inch antler. Antlerless deer and spotted fawns are not authorized by these area seasons.
- Arrows and bolts used for deer must have broadheads at least 7/8 inch wide. Any otherwise-authorized deer PCP airgun projectile must satisfy the statewide .30-caliber minimum; this does not authorize PCP equipment during bows-only or muzzleloader-only seasons.
- Muzzleloaders used for deer must be at least .30 caliber for a single bullet or at least 20 gauge when firing 2 or more balls.
- Log harvested deer before moving them and report to FWC within 24 hours of recovery, in addition to the area's check-station duties.

### General gun-vehicle / Antlered deer only

Dates: 2026-11-21 to 2026-12-06

Bag: Area general gun-vehicle limit 1 antlered deer per FWC antlered deer tag. Statewide annual 5 (maximum 2 antlerless), daily 2 and possession 4 apply.

Licenses: Hunting license, management area permit and deer permit required unless exempt. Nonresident game hunters require an annual hunting license. General gun-vehicle quota/track permit and its antlered deer tag are required by this hunt; no quota exemptions and no guest hunters. Deer require the supplied tag; a WMA deer-dog permit is required if hunting deer with dogs.

Methods: Lawful shotguns, rifles, muzzleloading guns, pistols, airguns, bows and crossbows, subject to brochure restrictions. No rimfire or non-expanding full-metal-jacket ammunition for deer; PCP airguns must propel a bolt, arrow or bullet of at least .30 caliber.

- Entry/exit is limited to the L-5 and Miami Canal levees. Hunting on roads, ramps, parking/camping areas, levees or adjacent powerline pads, and gun hunting on/from/across levees, is prohibited.
- Motorized use, scouting periods, flags and access routes are restricted. During general gun-vehicle season walk-hunting is closed and only vehicles authorized by its permits may operate; consult the map and permit conditions.
- Dogs may hunt deer/hog only during general gun-vehicle season; deer-dog hunting needs a valid WMA deer-dog permit, and dogs pursuing deer/hog need remote tracking and correction devices.
- When weekend check stations are staffed, check deer at the L-5 levee station before quartering, dismembering or removing them. General gun-vehicle deer must be immediately tagged with the FWC antlered deer tag.
- Antlered deer must have at least one antler 5 inches or longer with at least 2 points, each at least 1 inch. Youth under 16 have the statewide one-deer annual antler-point exception, still requiring a 5-inch antler. Antlerless deer and spotted fawns are not authorized by these area seasons.
- Arrows and bolts used for deer must have broadheads at least 7/8 inch wide. Any otherwise-authorized deer PCP airgun projectile must satisfy the statewide .30-caliber minimum; this does not authorize PCP equipment during bows-only or muzzleloader-only seasons.
- Muzzleloaders used for deer must be at least .30 caliber for a single bullet or at least 20 gauge when firing 2 or more balls.
- Log harvested deer before moving them and report to FWC within 24 hours of recovery, in addition to the area's check-station duties.

Conditions for the whole scope:

- Hunting over bait, taking swimming deer or spotted fawns, and hunting in posted closed areas are prohibited.
- Ordinary shooting hours are half an hour before sunrise through half an hour after sunset; turkey has separate hours.
- Night gun hunting, fully automatic firearms and centerfire semiautomatic rifles with magazines capable of more than 5 rounds are prohibited.
- Deer hunters and companions need 500 square inches of fluorescent orange above the waist, except bow-and-arrow hunting during archery season.
- Brochure license/permit exemptions include children under 16, Florida residents 65+, residents with a qualifying disabled-person certificate, and qualifying resident military personnel home on leave. They do not override quota permits marked no exemptions or required deer tags. Hunters born on/after June 1, 1975 need hunter-safety certification or the lawful supervised mentoring exception. Youth require adult supervision; mentoring license holders require a licensed supervisor aged 21+. Consult the complete brochure.
- The official brochure includes PDF BROCHURE and PDF MAP ONLY controls. Follow its current maps, access restrictions and FWC closure notices.

## White Tailed Deer: Holey Land WMA / Commission-Managed Land, 2026-2027 expansion

Key: `deer-holey-land-3-2026-2027-expanded`. new draft.

Scope: managed_area: Holey Land WMA

Review coverage: 2026-07-01 through 2027-06-30.

- [FWC Holey Land WMA 2026-2027 regulations and map](https://app.myfwc.com/hgm/hgmsearch/wmad?brochureTitle=Holey+Land) — checked 2026-10-12. Interactive brochure checked: area dates, legal species, bag limits, methods, permits, access and exceptions; PDF map available on the same page.
- [FWC hunting licenses and permits](https://myfwc.com/license/recreational/hunting/) — checked 2026-10-12. General license, management-area and season permits; brochure exemptions and area-specific quota restrictions retained.
- [FWC legal resident-game equipment](https://myfwc.com/hunting/regulations/taking-game/) — checked 2026-10-12. Checked broadhead minimum width, species-specific PCP minimums and deer muzzleloader design requirements; area season-method restrictions remain controlling.

### Archery / Antlered deer only

Dates: 2026-08-08 to 2026-08-30

Bag: Area season limit 1 antlered deer during archery, muzzleloading gun and general gun-walk seasons. Statewide annual limit 5 deer, including no more than 2 antlerless; daily 2 and possession 4 also apply.

Licenses: Hunting license, management area permit and deer permit required unless exempt. Nonresident game hunters require an annual hunting license. Archery season permit required unless exempt. No quota permit required for this listed season.

Methods: Bows only; crossbows, airbows and draw-lock bows require the brochure's Persons With Disabilities Crossbow Permit exception.

- Entry/exit is limited to the L-5 and Miami Canal levees. Hunting on roads, ramps, parking/camping areas, levees or adjacent powerline pads, and gun hunting on/from/across levees, is prohibited.
- Motorized use, scouting periods, flags and access routes are restricted. During general gun-vehicle season walk-hunting is closed and only vehicles authorized by its permits may operate; consult the map and permit conditions.
- Dogs may hunt deer/hog only during general gun-vehicle season; deer-dog hunting needs a valid WMA deer-dog permit, and dogs pursuing deer/hog need remote tracking and correction devices.
- When weekend check stations are staffed, check deer at the L-5 levee station before quartering, dismembering or removing them. General gun-vehicle deer must be immediately tagged with the FWC antlered deer tag.
- Antlered deer must have at least one antler 5 inches or longer with at least 2 points, each at least 1 inch. Youth under 16 have the statewide one-deer annual antler-point exception, still requiring a 5-inch antler. Antlerless deer and spotted fawns are not authorized by these area seasons.
- Arrows and bolts used for deer must have broadheads at least 7/8 inch wide. Any otherwise-authorized deer PCP airgun projectile must satisfy the statewide .30-caliber minimum; this does not authorize PCP equipment during bows-only or muzzleloader-only seasons.
- Muzzleloaders used for deer must be at least .30 caliber for a single bullet or at least 20 gauge when firing 2 or more balls.
- Log harvested deer before moving them and report to FWC within 24 hours of recovery, in addition to the area's check-station duties.

### Muzzleloading gun / Antlered deer only

Dates: 2026-09-05 to 2026-09-13

Bag: Area season limit 1 antlered deer during archery, muzzleloading gun and general gun-walk seasons. Statewide annual limit 5 deer, including no more than 2 antlerless; daily 2 and possession 4 also apply.

Licenses: Hunting license, management area permit and deer permit required unless exempt. Nonresident game hunters require an annual hunting license. Muzzleloading gun season permit required unless exempt. No quota permit required for this listed season.

Methods: Muzzleloading guns only for deer or hog; ordinary archery equipment is prohibited.

- Entry/exit is limited to the L-5 and Miami Canal levees. Hunting on roads, ramps, parking/camping areas, levees or adjacent powerline pads, and gun hunting on/from/across levees, is prohibited.
- Motorized use, scouting periods, flags and access routes are restricted. During general gun-vehicle season walk-hunting is closed and only vehicles authorized by its permits may operate; consult the map and permit conditions.
- Dogs may hunt deer/hog only during general gun-vehicle season; deer-dog hunting needs a valid WMA deer-dog permit, and dogs pursuing deer/hog need remote tracking and correction devices.
- When weekend check stations are staffed, check deer at the L-5 levee station before quartering, dismembering or removing them. General gun-vehicle deer must be immediately tagged with the FWC antlered deer tag.
- Antlered deer must have at least one antler 5 inches or longer with at least 2 points, each at least 1 inch. Youth under 16 have the statewide one-deer annual antler-point exception, still requiring a 5-inch antler. Antlerless deer and spotted fawns are not authorized by these area seasons.
- Arrows and bolts used for deer must have broadheads at least 7/8 inch wide. Any otherwise-authorized deer PCP airgun projectile must satisfy the statewide .30-caliber minimum; this does not authorize PCP equipment during bows-only or muzzleloader-only seasons.
- Muzzleloaders used for deer must be at least .30 caliber for a single bullet or at least 20 gauge when firing 2 or more balls.
- Log harvested deer before moving them and report to FWC within 24 hours of recovery, in addition to the area's check-station duties.

### General gun-walk / Antlered deer only

Dates: 2026-10-03 to 2026-10-18

Bag: Area season limit 1 antlered deer during archery, muzzleloading gun and general gun-walk seasons. Statewide annual limit 5 deer, including no more than 2 antlerless; daily 2 and possession 4 also apply.

Licenses: Hunting license, management area permit and deer permit required unless exempt. Nonresident game hunters require an annual hunting license. No quota permit required for this listed season.

Methods: Lawful shotguns, rifles, muzzleloading guns, pistols, airguns, bows and crossbows, subject to brochure restrictions. No rimfire or non-expanding full-metal-jacket ammunition for deer; PCP airguns must propel a bolt, arrow or bullet of at least .30 caliber.

- Entry/exit is limited to the L-5 and Miami Canal levees. Hunting on roads, ramps, parking/camping areas, levees or adjacent powerline pads, and gun hunting on/from/across levees, is prohibited.
- Motorized use, scouting periods, flags and access routes are restricted. During general gun-vehicle season walk-hunting is closed and only vehicles authorized by its permits may operate; consult the map and permit conditions.
- Dogs may hunt deer/hog only during general gun-vehicle season; deer-dog hunting needs a valid WMA deer-dog permit, and dogs pursuing deer/hog need remote tracking and correction devices.
- When weekend check stations are staffed, check deer at the L-5 levee station before quartering, dismembering or removing them. General gun-vehicle deer must be immediately tagged with the FWC antlered deer tag.
- Antlered deer must have at least one antler 5 inches or longer with at least 2 points, each at least 1 inch. Youth under 16 have the statewide one-deer annual antler-point exception, still requiring a 5-inch antler. Antlerless deer and spotted fawns are not authorized by these area seasons.
- Arrows and bolts used for deer must have broadheads at least 7/8 inch wide. Any otherwise-authorized deer PCP airgun projectile must satisfy the statewide .30-caliber minimum; this does not authorize PCP equipment during bows-only or muzzleloader-only seasons.
- Muzzleloaders used for deer must be at least .30 caliber for a single bullet or at least 20 gauge when firing 2 or more balls.
- Log harvested deer before moving them and report to FWC within 24 hours of recovery, in addition to the area's check-station duties.

### General gun-vehicle / Antlered deer only

Dates: 2026-11-21 to 2026-12-06

Bag: Area general gun-vehicle limit 1 antlered deer per FWC antlered deer tag. Statewide annual 5 (maximum 2 antlerless), daily 2 and possession 4 apply.

Licenses: Hunting license, management area permit and deer permit required unless exempt. Nonresident game hunters require an annual hunting license. General gun-vehicle quota/track permit and its antlered deer tag are required by this hunt; no quota exemptions and no guest hunters. Deer require the supplied tag; a WMA deer-dog permit is required if hunting deer with dogs.

Methods: Lawful shotguns, rifles, muzzleloading guns, pistols, airguns, bows and crossbows, subject to brochure restrictions. No rimfire or non-expanding full-metal-jacket ammunition for deer; PCP airguns must propel a bolt, arrow or bullet of at least .30 caliber.

- Entry/exit is limited to the L-5 and Miami Canal levees. Hunting on roads, ramps, parking/camping areas, levees or adjacent powerline pads, and gun hunting on/from/across levees, is prohibited.
- Motorized use, scouting periods, flags and access routes are restricted. During general gun-vehicle season walk-hunting is closed and only vehicles authorized by its permits may operate; consult the map and permit conditions.
- Dogs may hunt deer/hog only during general gun-vehicle season; deer-dog hunting needs a valid WMA deer-dog permit, and dogs pursuing deer/hog need remote tracking and correction devices.
- When weekend check stations are staffed, check deer at the L-5 levee station before quartering, dismembering or removing them. General gun-vehicle deer must be immediately tagged with the FWC antlered deer tag.
- Antlered deer must have at least one antler 5 inches or longer with at least 2 points, each at least 1 inch. Youth under 16 have the statewide one-deer annual antler-point exception, still requiring a 5-inch antler. Antlerless deer and spotted fawns are not authorized by these area seasons.
- Arrows and bolts used for deer must have broadheads at least 7/8 inch wide. Any otherwise-authorized deer PCP airgun projectile must satisfy the statewide .30-caliber minimum; this does not authorize PCP equipment during bows-only or muzzleloader-only seasons.
- Muzzleloaders used for deer must be at least .30 caliber for a single bullet or at least 20 gauge when firing 2 or more balls.
- Log harvested deer before moving them and report to FWC within 24 hours of recovery, in addition to the area's check-station duties.

Conditions for the whole scope:

- Hunting over bait, taking swimming deer or spotted fawns, and hunting in posted closed areas are prohibited.
- Ordinary shooting hours are half an hour before sunrise through half an hour after sunset; turkey has separate hours.
- Night gun hunting, fully automatic firearms and centerfire semiautomatic rifles with magazines capable of more than 5 rounds are prohibited.
- Deer hunters and companions need 500 square inches of fluorescent orange above the waist, except bow-and-arrow hunting during archery season.
- Brochure license/permit exemptions include children under 16, Florida residents 65+, residents with a qualifying disabled-person certificate, and qualifying resident military personnel home on leave. They do not override quota permits marked no exemptions or required deer tags. Hunters born on/after June 1, 1975 need hunter-safety certification or the lawful supervised mentoring exception. Youth require adult supervision; mentoring license holders require a licensed supervisor aged 21+. Consult the complete brochure.
- The official brochure includes PDF BROCHURE and PDF MAP ONLY controls. Follow its current maps, access restrictions and FWC closure notices.

## Deer: private land, DMU A1, 2026-2027

Key: `deer-private-a1-2026-2027`. proposed revision of existing approved draft.

Scope: zone: A; dmu: A1

Review coverage: 2026-07-01 through 2027-06-30.

- [FWC 2026-2027 seasons and bag limits](https://myfwc.com/hunting/season-dates/) — checked 2026-10-12. Zone A-D antlered/antlerless dates and daily, possession, annual limits checked; excludes WMAs.
- [FWC recreational licenses and permits](https://myfwc.com/license/recreational/hunting/) — checked 2026-10-12. Hunting/deer and season permits checked; individual statutory exemptions require confirmation.
- [FWC general hunting rules](https://myfwc.com/hunting/regulations/general-information/) — checked 2026-10-12. Shooting hours, safety, access and general restrictions checked.
- [FWC deer harvest reporting](https://myfwc.com/hunting/deer/harvest-report/) — checked 2026-10-12. Log before moving and official reporting deadlines checked.
- [FWC youth deer weekend](https://myfwc.com/hunting/get-started/youth-deer-hunting/) — checked 2026-10-12. Eligible ages, supervision, no youth permit requirement and participating-adult restrictions checked.
- [FWC DMU A antler rules](https://myfwc.com/hunting/season-dates/dmu-a/) — checked 2026-10-12. DMU-specific antler criteria and location exceptions checked.
- [FWC DMU B antler rules](https://myfwc.com/hunting/season-dates/dmu-b/) — checked 2026-10-12. DMU-specific antler criteria and location exceptions checked.
- [FWC DMU C antler rules](https://myfwc.com/hunting/season-dates/dmu-c/) — checked 2026-10-12. DMU-specific antler criteria and location exceptions checked.
- [FWC DMU D antler rules](https://myfwc.com/hunting/season-dates/dmu-d/) — checked 2026-10-12. DMU-specific antler criteria and location exceptions checked.
- [FWC current area notices](https://myfwc.com/recreation/notices/) — checked 2026-10-12. Current closure directory checked; notices can change after this data check.
- [FWC conditional license exemptions](https://myfwc.com/license/recreational/do-i-need-one/) — checked 2026-10-12. Checked youth, resident senior and conditional exemptions; quota rules remain separate.
- [FWC legal deer equipment](https://myfwc.com/hunting/regulations/taking-game/) — checked 2026-10-12. Checked broadhead, PCP, muzzleloader and prohibited ammunition requirements.
- [FWC hunter safety](https://myfwc.com/hunting/safety-education/) — checked 2026-10-12. Checked birth-date/age certification requirement and supervised deferral option.

### Archery / Antlered deer

Dates: 2026-08-01 to 2026-08-30

Bag: Daily 2 deer; possession 4; annual 5, including no more than 2 antlerless.

Licenses: Hunting license and deer permit unless exempt. Archery season permit required unless exempt.

Methods: Bows only.

- For hunters 16+: one antler at least 5 inches long with 2 points of at least 1 inch.
- Youth 15 and under have a one-deer annual exception to DMU antler-point criteria; a 5-inch antler is still required.
- Spotted fawns may not be taken. Confirm the precise parcel, shooting hours, hunter safety and local restrictions.
- Antlerless deer may not be taken in DMU A1. Taking any deer in the Florida Keys is prohibited.

### Crossbow / Antlered deer

Dates: 2026-08-01 to 2026-09-04

Bag: Daily 2 deer; possession 4; annual 5, including no more than 2 antlerless.

Licenses: Hunting license and deer permit unless exempt. Crossbow season permit required unless exempt.

Methods: Crossbows, bows and airbows.

- For hunters 16+: one antler at least 5 inches long with 2 points of at least 1 inch.
- Youth 15 and under have a one-deer annual exception to DMU antler-point criteria; a 5-inch antler is still required.
- Spotted fawns may not be taken. Confirm the precise parcel, shooting hours, hunter safety and local restrictions.
- Antlerless deer may not be taken in DMU A1. Taking any deer in the Florida Keys is prohibited.

### Muzzleloading gun / Antlered deer

Dates: 2026-09-05 to 2026-09-18

Bag: Daily 2 deer; possession 4; annual 5, including no more than 2 antlerless.

Licenses: Hunting license and deer permit unless exempt. Muzzleloading gun season permit required unless exempt.

Methods: Muzzleloaders, crossbows, bows and airbows; muzzleloading design restrictions apply.

- For hunters 16+: one antler at least 5 inches long with 2 points of at least 1 inch.
- Youth 15 and under have a one-deer annual exception to DMU antler-point criteria; a 5-inch antler is still required.
- Spotted fawns may not be taken. Confirm the precise parcel, shooting hours, hunter safety and local restrictions.
- Antlerless deer may not be taken in DMU A1. Taking any deer in the Florida Keys is prohibited.

### General gun / Antlered deer

Dates: 2026-09-19 to 2026-10-18; 2026-11-21 to 2027-01-03

Bag: Daily 2 deer; possession 4; annual 5, including no more than 2 antlerless.

Licenses: Hunting license and deer permit unless exempt. Check individual exemptions.

Methods: Lawful centerfire rifles, shotguns, handguns, muzzleloaders, PCP air guns, crossbows and bows.

- For hunters 16+: one antler at least 5 inches long with 2 points of at least 1 inch.
- Youth 15 and under have a one-deer annual exception to DMU antler-point criteria; a 5-inch antler is still required.
- Spotted fawns may not be taken. Confirm the precise parcel, shooting hours, hunter safety and local restrictions.
- Antlerless deer may not be taken in DMU A1. Taking any deer in the Florida Keys is prohibited.

### Youth weekend / Youth deer (DMU restrictions apply)

Dates: 2026-09-12 to 2026-09-13

Bag: 1 deer for the youth weekend, counted toward annual 5.

Licenses: No hunting license or permit for eligible youth 15 and under or an adult who only supervises. Participating adults have separate permit requirements.

Methods: Any legal method for an eligible youth hunter; supervision restrictions apply.

- Only hunters 15 and under, supervised by an adult 18+, qualify for the youth weekend; at most one antlered or antlerless deer where DMU restrictions permit.
- Participating adults 16+ need hunting, deer and muzzleloading permits unless exempt; muzzleloader/bow/crossbow and legal antlered deer only. Adults may not shoot during youth dog pursuits.
- For hunters 16+: one antler at least 5 inches long with 2 points of at least 1 inch.
- Youth 15 and under have a one-deer annual exception to DMU antler-point criteria; a 5-inch antler is still required.
- Spotted fawns may not be taken. Confirm the precise parcel, shooting hours, hunter safety and local restrictions.
- Antlerless deer may not be taken in DMU A1. Taking any deer in the Florida Keys is prohibited.

Conditions for the whole scope:

- Statewide schedules apply outside the WMA system. Special deer-program permits and other statutory exceptions are outside this standard lookup.
- All harvested deer must be logged before moving and officially reported within 24 hours or earlier processing/transfer/out-of-state deadline. HuntIt is not the FWC reporting system.
- Check the linked FWC area notices for temporary closures; this local dataset does not poll live closures.
- License/permit exemptions require the relevant proof and conditions: youth under 16; Florida residents age 65+; qualifying homestead hunting in the county of residence; Florida residents holding the qualifying disability license; qualifying resident military members home on leave for at most 30 days with orders; authorized military/disabled-veteran events; and qualifying licensed-preserve patrons. Check the official exemption page. An exemption does not change season dates, bag limits, access permission or harvest reporting.
- Ordinary deer shooting hours are one-half hour before sunrise through one-half hour after sunset; specific area restrictions still apply.
- Arrows/bolts for deer require broadheads at least 7/8 inch wide. Deer PCP projectiles must meet the .30-caliber requirement; rimfire and nonexpanding full-metal-case ammunition are prohibited.
- Deer muzzleloaders firing one bullet must be at least .30 caliber; guns firing multiple balls must be 20 gauge or larger. Season-specific method limits still apply.
- Hunters age 16+ born on or after June 1, 1975 need hunter-safety certification before buying a hunting license, unless using a lawful supervised deferral.
- Private-land deer dogs require FWC property registration, identification collars, remote tracking/correction and written landowner permission. Dogs cannot take deer during archery, crossbow or muzzleloading seasons.

## Deer: private land, DMU A2, 2026-2027

Key: `deer-private-a2-2026-2027`. proposed revision of existing approved draft.

Scope: zone: A; dmu: A2

Review coverage: 2026-07-01 through 2027-06-30.

- [FWC 2026-2027 seasons and bag limits](https://myfwc.com/hunting/season-dates/) — checked 2026-10-12. Zone A-D antlered/antlerless dates and daily, possession, annual limits checked; excludes WMAs.
- [FWC recreational licenses and permits](https://myfwc.com/license/recreational/hunting/) — checked 2026-10-12. Hunting/deer and season permits checked; individual statutory exemptions require confirmation.
- [FWC general hunting rules](https://myfwc.com/hunting/regulations/general-information/) — checked 2026-10-12. Shooting hours, safety, access and general restrictions checked.
- [FWC deer harvest reporting](https://myfwc.com/hunting/deer/harvest-report/) — checked 2026-10-12. Log before moving and official reporting deadlines checked.
- [FWC youth deer weekend](https://myfwc.com/hunting/get-started/youth-deer-hunting/) — checked 2026-10-12. Eligible ages, supervision, no youth permit requirement and participating-adult restrictions checked.
- [FWC DMU A antler rules](https://myfwc.com/hunting/season-dates/dmu-a/) — checked 2026-10-12. DMU-specific antler criteria and location exceptions checked.
- [FWC DMU B antler rules](https://myfwc.com/hunting/season-dates/dmu-b/) — checked 2026-10-12. DMU-specific antler criteria and location exceptions checked.
- [FWC DMU C antler rules](https://myfwc.com/hunting/season-dates/dmu-c/) — checked 2026-10-12. DMU-specific antler criteria and location exceptions checked.
- [FWC DMU D antler rules](https://myfwc.com/hunting/season-dates/dmu-d/) — checked 2026-10-12. DMU-specific antler criteria and location exceptions checked.
- [FWC current area notices](https://myfwc.com/recreation/notices/) — checked 2026-10-12. Current closure directory checked; notices can change after this data check.
- [FWC conditional license exemptions](https://myfwc.com/license/recreational/do-i-need-one/) — checked 2026-10-12. Checked youth, resident senior and conditional exemptions; quota rules remain separate.
- [FWC legal deer equipment](https://myfwc.com/hunting/regulations/taking-game/) — checked 2026-10-12. Checked broadhead, PCP, muzzleloader and prohibited ammunition requirements.
- [FWC hunter safety](https://myfwc.com/hunting/safety-education/) — checked 2026-10-12. Checked birth-date/age certification requirement and supervised deferral option.

### Archery / Antlered deer

Dates: 2026-08-01 to 2026-08-30

Bag: Daily 2 deer; possession 4; annual 5, including no more than 2 antlerless.

Licenses: Hunting license and deer permit unless exempt. Archery season permit required unless exempt.

Methods: Bows only.

- For hunters 16+: one antler at least 5 inches long with 2 points of at least 1 inch.
- Youth 15 and under have a one-deer annual exception to DMU antler-point criteria; a 5-inch antler is still required.
- Spotted fawns may not be taken. Confirm the precise parcel, shooting hours, hunter safety and local restrictions.
- Deer take is prohibited in the specified Collier County area bounded by I-75, SR29, US41 and Fakahatchee Strand's western boundary.

### Crossbow / Antlered deer

Dates: 2026-08-01 to 2026-09-04

Bag: Daily 2 deer; possession 4; annual 5, including no more than 2 antlerless.

Licenses: Hunting license and deer permit unless exempt. Crossbow season permit required unless exempt.

Methods: Crossbows, bows and airbows.

- For hunters 16+: one antler at least 5 inches long with 2 points of at least 1 inch.
- Youth 15 and under have a one-deer annual exception to DMU antler-point criteria; a 5-inch antler is still required.
- Spotted fawns may not be taken. Confirm the precise parcel, shooting hours, hunter safety and local restrictions.
- Deer take is prohibited in the specified Collier County area bounded by I-75, SR29, US41 and Fakahatchee Strand's western boundary.

### Muzzleloading gun / Antlered deer

Dates: 2026-09-05 to 2026-09-18

Bag: Daily 2 deer; possession 4; annual 5, including no more than 2 antlerless.

Licenses: Hunting license and deer permit unless exempt. Muzzleloading gun season permit required unless exempt.

Methods: Muzzleloaders, crossbows, bows and airbows; muzzleloading design restrictions apply.

- For hunters 16+: one antler at least 5 inches long with 2 points of at least 1 inch.
- Youth 15 and under have a one-deer annual exception to DMU antler-point criteria; a 5-inch antler is still required.
- Spotted fawns may not be taken. Confirm the precise parcel, shooting hours, hunter safety and local restrictions.
- Deer take is prohibited in the specified Collier County area bounded by I-75, SR29, US41 and Fakahatchee Strand's western boundary.

### General gun / Antlered deer

Dates: 2026-09-19 to 2026-10-18; 2026-11-21 to 2027-01-03

Bag: Daily 2 deer; possession 4; annual 5, including no more than 2 antlerless.

Licenses: Hunting license and deer permit unless exempt. Check individual exemptions.

Methods: Lawful centerfire rifles, shotguns, handguns, muzzleloaders, PCP air guns, crossbows and bows.

- For hunters 16+: one antler at least 5 inches long with 2 points of at least 1 inch.
- Youth 15 and under have a one-deer annual exception to DMU antler-point criteria; a 5-inch antler is still required.
- Spotted fawns may not be taken. Confirm the precise parcel, shooting hours, hunter safety and local restrictions.
- Deer take is prohibited in the specified Collier County area bounded by I-75, SR29, US41 and Fakahatchee Strand's western boundary.

### Youth weekend / Youth deer (DMU restrictions apply)

Dates: 2026-09-12 to 2026-09-13

Bag: 1 deer for the youth weekend, counted toward annual 5.

Licenses: No hunting license or permit for eligible youth 15 and under or an adult who only supervises. Participating adults have separate permit requirements.

Methods: Any legal method for an eligible youth hunter; supervision restrictions apply.

- Only hunters 15 and under, supervised by an adult 18+, qualify for the youth weekend; at most one antlered or antlerless deer where DMU restrictions permit.
- Participating adults 16+ need hunting, deer and muzzleloading permits unless exempt; muzzleloader/bow/crossbow and legal antlered deer only. Adults may not shoot during youth dog pursuits.
- For hunters 16+: one antler at least 5 inches long with 2 points of at least 1 inch.
- Youth 15 and under have a one-deer annual exception to DMU antler-point criteria; a 5-inch antler is still required.
- Spotted fawns may not be taken. Confirm the precise parcel, shooting hours, hunter safety and local restrictions.
- Deer take is prohibited in the specified Collier County area bounded by I-75, SR29, US41 and Fakahatchee Strand's western boundary.

### Archery / Antlerless deer (not spotted fawns)

Dates: 2026-08-01 to 2026-08-09

Bag: Daily 2 deer; possession 4; annual 5, including no more than 2 antlerless.

Licenses: Hunting license and deer permit unless exempt. Archery season permit required unless exempt.

Methods: Bows only.


### Crossbow / Antlerless deer (not spotted fawns)

Dates: 2026-08-01 to 2026-08-09

Bag: Daily 2 deer; possession 4; annual 5, including no more than 2 antlerless.

Licenses: Hunting license and deer permit unless exempt. Crossbow season permit required unless exempt.

Methods: Crossbows, bows and airbows.


### General gun / Antlerless deer (not spotted fawns)

Dates: 2026-11-21 to 2026-11-22

Bag: Daily 2 deer; possession 4; annual 5, including no more than 2 antlerless.

Licenses: Hunting license and deer permit unless exempt. Check individual exemptions.

Methods: Lawful centerfire rifles, shotguns, handguns, muzzleloaders, PCP air guns, crossbows and bows.


Conditions for the whole scope:

- Statewide schedules apply outside the WMA system. Special deer-program permits and other statutory exceptions are outside this standard lookup.
- All harvested deer must be logged before moving and officially reported within 24 hours or earlier processing/transfer/out-of-state deadline. HuntIt is not the FWC reporting system.
- Check the linked FWC area notices for temporary closures; this local dataset does not poll live closures.
- License/permit exemptions require the relevant proof and conditions: youth under 16; Florida residents age 65+; qualifying homestead hunting in the county of residence; Florida residents holding the qualifying disability license; qualifying resident military members home on leave for at most 30 days with orders; authorized military/disabled-veteran events; and qualifying licensed-preserve patrons. Check the official exemption page. An exemption does not change season dates, bag limits, access permission or harvest reporting.
- Ordinary deer shooting hours are one-half hour before sunrise through one-half hour after sunset; specific area restrictions still apply.
- Arrows/bolts for deer require broadheads at least 7/8 inch wide. Deer PCP projectiles must meet the .30-caliber requirement; rimfire and nonexpanding full-metal-case ammunition are prohibited.
- Deer muzzleloaders firing one bullet must be at least .30 caliber; guns firing multiple balls must be 20 gauge or larger. Season-specific method limits still apply.
- Hunters age 16+ born on or after June 1, 1975 need hunter-safety certification before buying a hunting license, unless using a lawful supervised deferral.
- Private-land deer dogs require FWC property registration, identification collars, remote tracking/correction and written landowner permission. Dogs cannot take deer during archery, crossbow or muzzleloading seasons.

## Deer: private land, DMU A3, 2026-2027

Key: `deer-private-a3-2026-2027`. proposed revision of existing approved draft.

Scope: zone: A; dmu: A3

Review coverage: 2026-07-01 through 2027-06-30.

- [FWC 2026-2027 seasons and bag limits](https://myfwc.com/hunting/season-dates/) — checked 2026-10-12. Zone A-D antlered/antlerless dates and daily, possession, annual limits checked; excludes WMAs.
- [FWC recreational licenses and permits](https://myfwc.com/license/recreational/hunting/) — checked 2026-10-12. Hunting/deer and season permits checked; individual statutory exemptions require confirmation.
- [FWC general hunting rules](https://myfwc.com/hunting/regulations/general-information/) — checked 2026-10-12. Shooting hours, safety, access and general restrictions checked.
- [FWC deer harvest reporting](https://myfwc.com/hunting/deer/harvest-report/) — checked 2026-10-12. Log before moving and official reporting deadlines checked.
- [FWC youth deer weekend](https://myfwc.com/hunting/get-started/youth-deer-hunting/) — checked 2026-10-12. Eligible ages, supervision, no youth permit requirement and participating-adult restrictions checked.
- [FWC DMU A antler rules](https://myfwc.com/hunting/season-dates/dmu-a/) — checked 2026-10-12. DMU-specific antler criteria and location exceptions checked.
- [FWC DMU B antler rules](https://myfwc.com/hunting/season-dates/dmu-b/) — checked 2026-10-12. DMU-specific antler criteria and location exceptions checked.
- [FWC DMU C antler rules](https://myfwc.com/hunting/season-dates/dmu-c/) — checked 2026-10-12. DMU-specific antler criteria and location exceptions checked.
- [FWC DMU D antler rules](https://myfwc.com/hunting/season-dates/dmu-d/) — checked 2026-10-12. DMU-specific antler criteria and location exceptions checked.
- [FWC current area notices](https://myfwc.com/recreation/notices/) — checked 2026-10-12. Current closure directory checked; notices can change after this data check.
- [FWC conditional license exemptions](https://myfwc.com/license/recreational/do-i-need-one/) — checked 2026-10-12. Checked youth, resident senior and conditional exemptions; quota rules remain separate.
- [FWC legal deer equipment](https://myfwc.com/hunting/regulations/taking-game/) — checked 2026-10-12. Checked broadhead, PCP, muzzleloader and prohibited ammunition requirements.
- [FWC hunter safety](https://myfwc.com/hunting/safety-education/) — checked 2026-10-12. Checked birth-date/age certification requirement and supervised deferral option.

### Archery / Antlered deer

Dates: 2026-08-01 to 2026-08-30

Bag: Daily 2 deer; possession 4; annual 5, including no more than 2 antlerless.

Licenses: Hunting license and deer permit unless exempt. Archery season permit required unless exempt.

Methods: Bows only.

- For hunters 16+: one antler at least 5 inches long with 3 points of at least 1 inch, or a main beam of at least 10 inches.
- Youth 15 and under have a one-deer annual exception to DMU antler-point criteria; a 5-inch antler is still required.
- Spotted fawns may not be taken. Confirm the precise parcel, shooting hours, hunter safety and local restrictions.

### Crossbow / Antlered deer

Dates: 2026-08-01 to 2026-09-04

Bag: Daily 2 deer; possession 4; annual 5, including no more than 2 antlerless.

Licenses: Hunting license and deer permit unless exempt. Crossbow season permit required unless exempt.

Methods: Crossbows, bows and airbows.

- For hunters 16+: one antler at least 5 inches long with 3 points of at least 1 inch, or a main beam of at least 10 inches.
- Youth 15 and under have a one-deer annual exception to DMU antler-point criteria; a 5-inch antler is still required.
- Spotted fawns may not be taken. Confirm the precise parcel, shooting hours, hunter safety and local restrictions.

### Muzzleloading gun / Antlered deer

Dates: 2026-09-05 to 2026-09-18

Bag: Daily 2 deer; possession 4; annual 5, including no more than 2 antlerless.

Licenses: Hunting license and deer permit unless exempt. Muzzleloading gun season permit required unless exempt.

Methods: Muzzleloaders, crossbows, bows and airbows; muzzleloading design restrictions apply.

- For hunters 16+: one antler at least 5 inches long with 3 points of at least 1 inch, or a main beam of at least 10 inches.
- Youth 15 and under have a one-deer annual exception to DMU antler-point criteria; a 5-inch antler is still required.
- Spotted fawns may not be taken. Confirm the precise parcel, shooting hours, hunter safety and local restrictions.

### General gun / Antlered deer

Dates: 2026-09-19 to 2026-10-18; 2026-11-21 to 2027-01-03

Bag: Daily 2 deer; possession 4; annual 5, including no more than 2 antlerless.

Licenses: Hunting license and deer permit unless exempt. Check individual exemptions.

Methods: Lawful centerfire rifles, shotguns, handguns, muzzleloaders, PCP air guns, crossbows and bows.

- For hunters 16+: one antler at least 5 inches long with 3 points of at least 1 inch, or a main beam of at least 10 inches.
- Youth 15 and under have a one-deer annual exception to DMU antler-point criteria; a 5-inch antler is still required.
- Spotted fawns may not be taken. Confirm the precise parcel, shooting hours, hunter safety and local restrictions.

### Youth weekend / Youth deer (DMU restrictions apply)

Dates: 2026-09-12 to 2026-09-13

Bag: 1 deer for the youth weekend, counted toward annual 5.

Licenses: No hunting license or permit for eligible youth 15 and under or an adult who only supervises. Participating adults have separate permit requirements.

Methods: Any legal method for an eligible youth hunter; supervision restrictions apply.

- Only hunters 15 and under, supervised by an adult 18+, qualify for the youth weekend; at most one antlered or antlerless deer where DMU restrictions permit.
- Participating adults 16+ need hunting, deer and muzzleloading permits unless exempt; muzzleloader/bow/crossbow and legal antlered deer only. Adults may not shoot during youth dog pursuits.
- For hunters 16+: one antler at least 5 inches long with 3 points of at least 1 inch, or a main beam of at least 10 inches.
- Youth 15 and under have a one-deer annual exception to DMU antler-point criteria; a 5-inch antler is still required.
- Spotted fawns may not be taken. Confirm the precise parcel, shooting hours, hunter safety and local restrictions.

### Archery / Antlerless deer (not spotted fawns)

Dates: 2026-08-01 to 2026-08-16

Bag: Daily 2 deer; possession 4; annual 5, including no more than 2 antlerless.

Licenses: Hunting license and deer permit unless exempt. Archery season permit required unless exempt.

Methods: Bows only.


### Crossbow / Antlerless deer (not spotted fawns)

Dates: 2026-08-01 to 2026-08-16

Bag: Daily 2 deer; possession 4; annual 5, including no more than 2 antlerless.

Licenses: Hunting license and deer permit unless exempt. Crossbow season permit required unless exempt.

Methods: Crossbows, bows and airbows.


### General gun / Antlerless deer (not spotted fawns)

Dates: 2026-11-21 to 2026-11-24

Bag: Daily 2 deer; possession 4; annual 5, including no more than 2 antlerless.

Licenses: Hunting license and deer permit unless exempt. Check individual exemptions.

Methods: Lawful centerfire rifles, shotguns, handguns, muzzleloaders, PCP air guns, crossbows and bows.


Conditions for the whole scope:

- Statewide schedules apply outside the WMA system. Special deer-program permits and other statutory exceptions are outside this standard lookup.
- All harvested deer must be logged before moving and officially reported within 24 hours or earlier processing/transfer/out-of-state deadline. HuntIt is not the FWC reporting system.
- Check the linked FWC area notices for temporary closures; this local dataset does not poll live closures.
- License/permit exemptions require the relevant proof and conditions: youth under 16; Florida residents age 65+; qualifying homestead hunting in the county of residence; Florida residents holding the qualifying disability license; qualifying resident military members home on leave for at most 30 days with orders; authorized military/disabled-veteran events; and qualifying licensed-preserve patrons. Check the official exemption page. An exemption does not change season dates, bag limits, access permission or harvest reporting.
- Ordinary deer shooting hours are one-half hour before sunrise through one-half hour after sunset; specific area restrictions still apply.
- Arrows/bolts for deer require broadheads at least 7/8 inch wide. Deer PCP projectiles must meet the .30-caliber requirement; rimfire and nonexpanding full-metal-case ammunition are prohibited.
- Deer muzzleloaders firing one bullet must be at least .30 caliber; guns firing multiple balls must be 20 gauge or larger. Season-specific method limits still apply.
- Hunters age 16+ born on or after June 1, 1975 need hunter-safety certification before buying a hunting license, unless using a lawful supervised deferral.
- Private-land deer dogs require FWC property registration, identification collars, remote tracking/correction and written landowner permission. Dogs cannot take deer during archery, crossbow or muzzleloading seasons.

## Deer: private land, DMU B1, 2026-2027

Key: `deer-private-b1-2026-2027`. proposed revision of existing approved draft.

Scope: zone: B; dmu: B1

Review coverage: 2026-07-01 through 2027-06-30.

- [FWC 2026-2027 seasons and bag limits](https://myfwc.com/hunting/season-dates/) — checked 2026-10-12. Zone A-D antlered/antlerless dates and daily, possession, annual limits checked; excludes WMAs.
- [FWC recreational licenses and permits](https://myfwc.com/license/recreational/hunting/) — checked 2026-10-12. Hunting/deer and season permits checked; individual statutory exemptions require confirmation.
- [FWC general hunting rules](https://myfwc.com/hunting/regulations/general-information/) — checked 2026-10-12. Shooting hours, safety, access and general restrictions checked.
- [FWC deer harvest reporting](https://myfwc.com/hunting/deer/harvest-report/) — checked 2026-10-12. Log before moving and official reporting deadlines checked.
- [FWC youth deer weekend](https://myfwc.com/hunting/get-started/youth-deer-hunting/) — checked 2026-10-12. Eligible ages, supervision, no youth permit requirement and participating-adult restrictions checked.
- [FWC DMU A antler rules](https://myfwc.com/hunting/season-dates/dmu-a/) — checked 2026-10-12. DMU-specific antler criteria and location exceptions checked.
- [FWC DMU B antler rules](https://myfwc.com/hunting/season-dates/dmu-b/) — checked 2026-10-12. DMU-specific antler criteria and location exceptions checked.
- [FWC DMU C antler rules](https://myfwc.com/hunting/season-dates/dmu-c/) — checked 2026-10-12. DMU-specific antler criteria and location exceptions checked.
- [FWC DMU D antler rules](https://myfwc.com/hunting/season-dates/dmu-d/) — checked 2026-10-12. DMU-specific antler criteria and location exceptions checked.
- [FWC current area notices](https://myfwc.com/recreation/notices/) — checked 2026-10-12. Current closure directory checked; notices can change after this data check.
- [FWC conditional license exemptions](https://myfwc.com/license/recreational/do-i-need-one/) — checked 2026-10-12. Checked youth, resident senior and conditional exemptions; quota rules remain separate.
- [FWC legal deer equipment](https://myfwc.com/hunting/regulations/taking-game/) — checked 2026-10-12. Checked broadhead, PCP, muzzleloader and prohibited ammunition requirements.
- [FWC hunter safety](https://myfwc.com/hunting/safety-education/) — checked 2026-10-12. Checked birth-date/age certification requirement and supervised deferral option.

### Archery / Antlered deer

Dates: 2026-10-17 to 2026-11-15

Bag: Daily 2 deer; possession 4; annual 5, including no more than 2 antlerless.

Licenses: Hunting license and deer permit unless exempt. Archery season permit required unless exempt.

Methods: Bows only.

- For hunters 16+: one antler at least 5 inches long with 3 points of at least 1 inch, or a main beam of at least 10 inches.
- Youth 15 and under have a one-deer annual exception to DMU antler-point criteria; a 5-inch antler is still required.
- Spotted fawns may not be taken. Confirm the precise parcel, shooting hours, hunter safety and local restrictions.

### Crossbow / Antlered deer

Dates: 2026-10-17 to 2026-11-20

Bag: Daily 2 deer; possession 4; annual 5, including no more than 2 antlerless.

Licenses: Hunting license and deer permit unless exempt. Crossbow season permit required unless exempt.

Methods: Crossbows, bows and airbows.

- For hunters 16+: one antler at least 5 inches long with 3 points of at least 1 inch, or a main beam of at least 10 inches.
- Youth 15 and under have a one-deer annual exception to DMU antler-point criteria; a 5-inch antler is still required.
- Spotted fawns may not be taken. Confirm the precise parcel, shooting hours, hunter safety and local restrictions.

### Muzzleloading gun / Antlered deer

Dates: 2026-11-21 to 2026-12-04

Bag: Daily 2 deer; possession 4; annual 5, including no more than 2 antlerless.

Licenses: Hunting license and deer permit unless exempt. Muzzleloading gun season permit required unless exempt.

Methods: Muzzleloaders, crossbows, bows and airbows; muzzleloading design restrictions apply.

- For hunters 16+: one antler at least 5 inches long with 3 points of at least 1 inch, or a main beam of at least 10 inches.
- Youth 15 and under have a one-deer annual exception to DMU antler-point criteria; a 5-inch antler is still required.
- Spotted fawns may not be taken. Confirm the precise parcel, shooting hours, hunter safety and local restrictions.

### General gun / Antlered deer

Dates: 2026-12-05 to 2027-02-21

Bag: Daily 2 deer; possession 4; annual 5, including no more than 2 antlerless.

Licenses: Hunting license and deer permit unless exempt. Check individual exemptions.

Methods: Lawful centerfire rifles, shotguns, handguns, muzzleloaders, PCP air guns, crossbows and bows.

- For hunters 16+: one antler at least 5 inches long with 3 points of at least 1 inch, or a main beam of at least 10 inches.
- Youth 15 and under have a one-deer annual exception to DMU antler-point criteria; a 5-inch antler is still required.
- Spotted fawns may not be taken. Confirm the precise parcel, shooting hours, hunter safety and local restrictions.

### Youth weekend / Youth deer (DMU restrictions apply)

Dates: 2026-11-28 to 2026-11-29

Bag: 1 deer for the youth weekend, counted toward annual 5.

Licenses: No hunting license or permit for eligible youth 15 and under or an adult who only supervises. Participating adults have separate permit requirements.

Methods: Any legal method for an eligible youth hunter; supervision restrictions apply.

- Only hunters 15 and under, supervised by an adult 18+, qualify for the youth weekend; at most one antlered or antlerless deer where DMU restrictions permit.
- Participating adults 16+ need hunting, deer and muzzleloading permits unless exempt; muzzleloader/bow/crossbow and legal antlered deer only. Adults may not shoot during youth dog pursuits.
- For hunters 16+: one antler at least 5 inches long with 3 points of at least 1 inch, or a main beam of at least 10 inches.
- Youth 15 and under have a one-deer annual exception to DMU antler-point criteria; a 5-inch antler is still required.
- Spotted fawns may not be taken. Confirm the precise parcel, shooting hours, hunter safety and local restrictions.

### Archery / Antlerless deer (not spotted fawns)

Dates: 2026-10-17 to 2026-11-15

Bag: Daily 2 deer; possession 4; annual 5, including no more than 2 antlerless.

Licenses: Hunting license and deer permit unless exempt. Archery season permit required unless exempt.

Methods: Bows only.


### Crossbow / Antlerless deer (not spotted fawns)

Dates: 2026-10-17 to 2026-11-20

Bag: Daily 2 deer; possession 4; annual 5, including no more than 2 antlerless.

Licenses: Hunting license and deer permit unless exempt. Crossbow season permit required unless exempt.

Methods: Crossbows, bows and airbows.


### Muzzleloading gun / Antlerless deer (not spotted fawns)

Dates: 2026-11-21 to 2026-12-04

Bag: Daily 2 deer; possession 4; annual 5, including no more than 2 antlerless.

Licenses: Hunting license and deer permit unless exempt. Muzzleloading gun season permit required unless exempt.

Methods: Muzzleloaders, crossbows, bows and airbows; muzzleloading design restrictions apply.


### General gun / Antlerless deer (not spotted fawns)

Dates: 2026-12-26 to 2027-01-03

Bag: Daily 2 deer; possession 4; annual 5, including no more than 2 antlerless.

Licenses: Hunting license and deer permit unless exempt. Check individual exemptions.

Methods: Lawful centerfire rifles, shotguns, handguns, muzzleloaders, PCP air guns, crossbows and bows.


Conditions for the whole scope:

- Statewide schedules apply outside the WMA system. Special deer-program permits and other statutory exceptions are outside this standard lookup.
- All harvested deer must be logged before moving and officially reported within 24 hours or earlier processing/transfer/out-of-state deadline. HuntIt is not the FWC reporting system.
- Check the linked FWC area notices for temporary closures; this local dataset does not poll live closures.
- License/permit exemptions require the relevant proof and conditions: youth under 16; Florida residents age 65+; qualifying homestead hunting in the county of residence; Florida residents holding the qualifying disability license; qualifying resident military members home on leave for at most 30 days with orders; authorized military/disabled-veteran events; and qualifying licensed-preserve patrons. Check the official exemption page. An exemption does not change season dates, bag limits, access permission or harvest reporting.
- Ordinary deer shooting hours are one-half hour before sunrise through one-half hour after sunset; specific area restrictions still apply.
- Arrows/bolts for deer require broadheads at least 7/8 inch wide. Deer PCP projectiles must meet the .30-caliber requirement; rimfire and nonexpanding full-metal-case ammunition are prohibited.
- Deer muzzleloaders firing one bullet must be at least .30 caliber; guns firing multiple balls must be 20 gauge or larger. Season-specific method limits still apply.
- Hunters age 16+ born on or after June 1, 1975 need hunter-safety certification before buying a hunting license, unless using a lawful supervised deferral.
- Private-land deer dogs require FWC property registration, identification collars, remote tracking/correction and written landowner permission. Dogs cannot take deer during archery, crossbow or muzzleloading seasons.

## Deer: private land, DMU C1, 2026-2027

Key: `deer-private-c1-2026-2027`. proposed revision of existing approved draft.

Scope: zone: C; dmu: C1

Review coverage: 2026-07-01 through 2027-06-30.

- [FWC 2026-2027 seasons and bag limits](https://myfwc.com/hunting/season-dates/) — checked 2026-10-12. Zone A-D antlered/antlerless dates and daily, possession, annual limits checked; excludes WMAs.
- [FWC recreational licenses and permits](https://myfwc.com/license/recreational/hunting/) — checked 2026-10-12. Hunting/deer and season permits checked; individual statutory exemptions require confirmation.
- [FWC general hunting rules](https://myfwc.com/hunting/regulations/general-information/) — checked 2026-10-12. Shooting hours, safety, access and general restrictions checked.
- [FWC deer harvest reporting](https://myfwc.com/hunting/deer/harvest-report/) — checked 2026-10-12. Log before moving and official reporting deadlines checked.
- [FWC youth deer weekend](https://myfwc.com/hunting/get-started/youth-deer-hunting/) — checked 2026-10-12. Eligible ages, supervision, no youth permit requirement and participating-adult restrictions checked.
- [FWC DMU A antler rules](https://myfwc.com/hunting/season-dates/dmu-a/) — checked 2026-10-12. DMU-specific antler criteria and location exceptions checked.
- [FWC DMU B antler rules](https://myfwc.com/hunting/season-dates/dmu-b/) — checked 2026-10-12. DMU-specific antler criteria and location exceptions checked.
- [FWC DMU C antler rules](https://myfwc.com/hunting/season-dates/dmu-c/) — checked 2026-10-12. DMU-specific antler criteria and location exceptions checked.
- [FWC DMU D antler rules](https://myfwc.com/hunting/season-dates/dmu-d/) — checked 2026-10-12. DMU-specific antler criteria and location exceptions checked.
- [FWC current area notices](https://myfwc.com/recreation/notices/) — checked 2026-10-12. Current closure directory checked; notices can change after this data check.
- [FWC conditional license exemptions](https://myfwc.com/license/recreational/do-i-need-one/) — checked 2026-10-12. Checked youth, resident senior and conditional exemptions; quota rules remain separate.
- [FWC legal deer equipment](https://myfwc.com/hunting/regulations/taking-game/) — checked 2026-10-12. Checked broadhead, PCP, muzzleloader and prohibited ammunition requirements.
- [FWC hunter safety](https://myfwc.com/hunting/safety-education/) — checked 2026-10-12. Checked birth-date/age certification requirement and supervised deferral option.

### Archery / Antlered deer

Dates: 2026-09-19 to 2026-10-18

Bag: Daily 2 deer; possession 4; annual 5, including no more than 2 antlerless.

Licenses: Hunting license and deer permit unless exempt. Archery season permit required unless exempt.

Methods: Bows only.

- For hunters 16+: one antler at least 5 inches long with 3 points of at least 1 inch, or a main beam of at least 10 inches.
- Youth 15 and under have a one-deer annual exception to DMU antler-point criteria; a 5-inch antler is still required.
- Spotted fawns may not be taken. Confirm the precise parcel, shooting hours, hunter safety and local restrictions.

### Crossbow / Antlered deer

Dates: 2026-09-19 to 2026-10-23

Bag: Daily 2 deer; possession 4; annual 5, including no more than 2 antlerless.

Licenses: Hunting license and deer permit unless exempt. Crossbow season permit required unless exempt.

Methods: Crossbows, bows and airbows.

- For hunters 16+: one antler at least 5 inches long with 3 points of at least 1 inch, or a main beam of at least 10 inches.
- Youth 15 and under have a one-deer annual exception to DMU antler-point criteria; a 5-inch antler is still required.
- Spotted fawns may not be taken. Confirm the precise parcel, shooting hours, hunter safety and local restrictions.

### Muzzleloading gun / Antlered deer

Dates: 2026-10-24 to 2026-11-06

Bag: Daily 2 deer; possession 4; annual 5, including no more than 2 antlerless.

Licenses: Hunting license and deer permit unless exempt. Muzzleloading gun season permit required unless exempt.

Methods: Muzzleloaders, crossbows, bows and airbows; muzzleloading design restrictions apply.

- For hunters 16+: one antler at least 5 inches long with 3 points of at least 1 inch, or a main beam of at least 10 inches.
- Youth 15 and under have a one-deer annual exception to DMU antler-point criteria; a 5-inch antler is still required.
- Spotted fawns may not be taken. Confirm the precise parcel, shooting hours, hunter safety and local restrictions.

### General gun / Antlered deer

Dates: 2026-11-07 to 2027-01-24

Bag: Daily 2 deer; possession 4; annual 5, including no more than 2 antlerless.

Licenses: Hunting license and deer permit unless exempt. Check individual exemptions.

Methods: Lawful centerfire rifles, shotguns, handguns, muzzleloaders, PCP air guns, crossbows and bows.

- For hunters 16+: one antler at least 5 inches long with 3 points of at least 1 inch, or a main beam of at least 10 inches.
- Youth 15 and under have a one-deer annual exception to DMU antler-point criteria; a 5-inch antler is still required.
- Spotted fawns may not be taken. Confirm the precise parcel, shooting hours, hunter safety and local restrictions.

### Youth weekend / Youth deer (DMU restrictions apply)

Dates: 2026-10-31 to 2026-11-01

Bag: 1 deer for the youth weekend, counted toward annual 5.

Licenses: No hunting license or permit for eligible youth 15 and under or an adult who only supervises. Participating adults have separate permit requirements.

Methods: Any legal method for an eligible youth hunter; supervision restrictions apply.

- Only hunters 15 and under, supervised by an adult 18+, qualify for the youth weekend; at most one antlered or antlerless deer where DMU restrictions permit.
- Participating adults 16+ need hunting, deer and muzzleloading permits unless exempt; muzzleloader/bow/crossbow and legal antlered deer only. Adults may not shoot during youth dog pursuits.
- For hunters 16+: one antler at least 5 inches long with 3 points of at least 1 inch, or a main beam of at least 10 inches.
- Youth 15 and under have a one-deer annual exception to DMU antler-point criteria; a 5-inch antler is still required.
- Spotted fawns may not be taken. Confirm the precise parcel, shooting hours, hunter safety and local restrictions.

### Archery / Antlerless deer (not spotted fawns)

Dates: 2026-09-19 to 2026-10-18

Bag: Daily 2 deer; possession 4; annual 5, including no more than 2 antlerless.

Licenses: Hunting license and deer permit unless exempt. Archery season permit required unless exempt.

Methods: Bows only.


### Crossbow / Antlerless deer (not spotted fawns)

Dates: 2026-09-19 to 2026-10-23

Bag: Daily 2 deer; possession 4; annual 5, including no more than 2 antlerless.

Licenses: Hunting license and deer permit unless exempt. Crossbow season permit required unless exempt.

Methods: Crossbows, bows and airbows.


### Muzzleloading gun / Antlerless deer (not spotted fawns)

Dates: 2026-10-24 to 2026-11-06

Bag: Daily 2 deer; possession 4; annual 5, including no more than 2 antlerless.

Licenses: Hunting license and deer permit unless exempt. Muzzleloading gun season permit required unless exempt.

Methods: Muzzleloaders, crossbows, bows and airbows; muzzleloading design restrictions apply.


### General gun / Antlerless deer (not spotted fawns)

Dates: 2026-11-21 to 2026-11-29

Bag: Daily 2 deer; possession 4; annual 5, including no more than 2 antlerless.

Licenses: Hunting license and deer permit unless exempt. Check individual exemptions.

Methods: Lawful centerfire rifles, shotguns, handguns, muzzleloaders, PCP air guns, crossbows and bows.


Conditions for the whole scope:

- Statewide schedules apply outside the WMA system. Special deer-program permits and other statutory exceptions are outside this standard lookup.
- All harvested deer must be logged before moving and officially reported within 24 hours or earlier processing/transfer/out-of-state deadline. HuntIt is not the FWC reporting system.
- Check the linked FWC area notices for temporary closures; this local dataset does not poll live closures.
- License/permit exemptions require the relevant proof and conditions: youth under 16; Florida residents age 65+; qualifying homestead hunting in the county of residence; Florida residents holding the qualifying disability license; qualifying resident military members home on leave for at most 30 days with orders; authorized military/disabled-veteran events; and qualifying licensed-preserve patrons. Check the official exemption page. An exemption does not change season dates, bag limits, access permission or harvest reporting.
- Ordinary deer shooting hours are one-half hour before sunrise through one-half hour after sunset; specific area restrictions still apply.
- Arrows/bolts for deer require broadheads at least 7/8 inch wide. Deer PCP projectiles must meet the .30-caliber requirement; rimfire and nonexpanding full-metal-case ammunition are prohibited.
- Deer muzzleloaders firing one bullet must be at least .30 caliber; guns firing multiple balls must be 20 gauge or larger. Season-specific method limits still apply.
- Hunters age 16+ born on or after June 1, 1975 need hunter-safety certification before buying a hunting license, unless using a lawful supervised deferral.
- Private-land deer dogs require FWC property registration, identification collars, remote tracking/correction and written landowner permission. Dogs cannot take deer during archery, crossbow or muzzleloading seasons.

## Deer: private land, DMU C2, 2026-2027

Key: `deer-private-c2-2026-2027`. proposed revision of existing approved draft.

Scope: zone: C; dmu: C2

Review coverage: 2026-07-01 through 2027-06-30.

- [FWC 2026-2027 seasons and bag limits](https://myfwc.com/hunting/season-dates/) — checked 2026-10-12. Zone A-D antlered/antlerless dates and daily, possession, annual limits checked; excludes WMAs.
- [FWC recreational licenses and permits](https://myfwc.com/license/recreational/hunting/) — checked 2026-10-12. Hunting/deer and season permits checked; individual statutory exemptions require confirmation.
- [FWC general hunting rules](https://myfwc.com/hunting/regulations/general-information/) — checked 2026-10-12. Shooting hours, safety, access and general restrictions checked.
- [FWC deer harvest reporting](https://myfwc.com/hunting/deer/harvest-report/) — checked 2026-10-12. Log before moving and official reporting deadlines checked.
- [FWC youth deer weekend](https://myfwc.com/hunting/get-started/youth-deer-hunting/) — checked 2026-10-12. Eligible ages, supervision, no youth permit requirement and participating-adult restrictions checked.
- [FWC DMU A antler rules](https://myfwc.com/hunting/season-dates/dmu-a/) — checked 2026-10-12. DMU-specific antler criteria and location exceptions checked.
- [FWC DMU B antler rules](https://myfwc.com/hunting/season-dates/dmu-b/) — checked 2026-10-12. DMU-specific antler criteria and location exceptions checked.
- [FWC DMU C antler rules](https://myfwc.com/hunting/season-dates/dmu-c/) — checked 2026-10-12. DMU-specific antler criteria and location exceptions checked.
- [FWC DMU D antler rules](https://myfwc.com/hunting/season-dates/dmu-d/) — checked 2026-10-12. DMU-specific antler criteria and location exceptions checked.
- [FWC current area notices](https://myfwc.com/recreation/notices/) — checked 2026-10-12. Current closure directory checked; notices can change after this data check.
- [FWC conditional license exemptions](https://myfwc.com/license/recreational/do-i-need-one/) — checked 2026-10-12. Checked youth, resident senior and conditional exemptions; quota rules remain separate.
- [FWC legal deer equipment](https://myfwc.com/hunting/regulations/taking-game/) — checked 2026-10-12. Checked broadhead, PCP, muzzleloader and prohibited ammunition requirements.
- [FWC hunter safety](https://myfwc.com/hunting/safety-education/) — checked 2026-10-12. Checked birth-date/age certification requirement and supervised deferral option.

### Archery / Antlered deer

Dates: 2026-09-19 to 2026-10-18

Bag: Daily 2 deer; possession 4; annual 5, including no more than 2 antlerless.

Licenses: Hunting license and deer permit unless exempt. Archery season permit required unless exempt.

Methods: Bows only.

- For hunters 16+: one antler at least 5 inches long with 3 points of at least 1 inch, or a main beam of at least 10 inches.
- Youth 15 and under have a one-deer annual exception to DMU antler-point criteria; a 5-inch antler is still required.
- Spotted fawns may not be taken. Confirm the precise parcel, shooting hours, hunter safety and local restrictions.

### Crossbow / Antlered deer

Dates: 2026-09-19 to 2026-10-23

Bag: Daily 2 deer; possession 4; annual 5, including no more than 2 antlerless.

Licenses: Hunting license and deer permit unless exempt. Crossbow season permit required unless exempt.

Methods: Crossbows, bows and airbows.

- For hunters 16+: one antler at least 5 inches long with 3 points of at least 1 inch, or a main beam of at least 10 inches.
- Youth 15 and under have a one-deer annual exception to DMU antler-point criteria; a 5-inch antler is still required.
- Spotted fawns may not be taken. Confirm the precise parcel, shooting hours, hunter safety and local restrictions.

### Muzzleloading gun / Antlered deer

Dates: 2026-10-24 to 2026-11-06

Bag: Daily 2 deer; possession 4; annual 5, including no more than 2 antlerless.

Licenses: Hunting license and deer permit unless exempt. Muzzleloading gun season permit required unless exempt.

Methods: Muzzleloaders, crossbows, bows and airbows; muzzleloading design restrictions apply.

- For hunters 16+: one antler at least 5 inches long with 3 points of at least 1 inch, or a main beam of at least 10 inches.
- Youth 15 and under have a one-deer annual exception to DMU antler-point criteria; a 5-inch antler is still required.
- Spotted fawns may not be taken. Confirm the precise parcel, shooting hours, hunter safety and local restrictions.

### General gun / Antlered deer

Dates: 2026-11-07 to 2027-01-24

Bag: Daily 2 deer; possession 4; annual 5, including no more than 2 antlerless.

Licenses: Hunting license and deer permit unless exempt. Check individual exemptions.

Methods: Lawful centerfire rifles, shotguns, handguns, muzzleloaders, PCP air guns, crossbows and bows.

- For hunters 16+: one antler at least 5 inches long with 3 points of at least 1 inch, or a main beam of at least 10 inches.
- Youth 15 and under have a one-deer annual exception to DMU antler-point criteria; a 5-inch antler is still required.
- Spotted fawns may not be taken. Confirm the precise parcel, shooting hours, hunter safety and local restrictions.

### Youth weekend / Youth deer (DMU restrictions apply)

Dates: 2026-10-31 to 2026-11-01

Bag: 1 deer for the youth weekend, counted toward annual 5.

Licenses: No hunting license or permit for eligible youth 15 and under or an adult who only supervises. Participating adults have separate permit requirements.

Methods: Any legal method for an eligible youth hunter; supervision restrictions apply.

- Only hunters 15 and under, supervised by an adult 18+, qualify for the youth weekend; at most one antlered or antlerless deer where DMU restrictions permit.
- Participating adults 16+ need hunting, deer and muzzleloading permits unless exempt; muzzleloader/bow/crossbow and legal antlered deer only. Adults may not shoot during youth dog pursuits.
- For hunters 16+: one antler at least 5 inches long with 3 points of at least 1 inch, or a main beam of at least 10 inches.
- Youth 15 and under have a one-deer annual exception to DMU antler-point criteria; a 5-inch antler is still required.
- Spotted fawns may not be taken. Confirm the precise parcel, shooting hours, hunter safety and local restrictions.

### Archery / Antlerless deer (not spotted fawns)

Dates: 2026-09-19 to 2026-10-18

Bag: Daily 2 deer; possession 4; annual 5, including no more than 2 antlerless.

Licenses: Hunting license and deer permit unless exempt. Archery season permit required unless exempt.

Methods: Bows only.


### Crossbow / Antlerless deer (not spotted fawns)

Dates: 2026-09-19 to 2026-10-23

Bag: Daily 2 deer; possession 4; annual 5, including no more than 2 antlerless.

Licenses: Hunting license and deer permit unless exempt. Crossbow season permit required unless exempt.

Methods: Crossbows, bows and airbows.


### Muzzleloading gun / Antlerless deer (not spotted fawns)

Dates: 2026-10-24 to 2026-11-06

Bag: Daily 2 deer; possession 4; annual 5, including no more than 2 antlerless.

Licenses: Hunting license and deer permit unless exempt. Muzzleloading gun season permit required unless exempt.

Methods: Muzzleloaders, crossbows, bows and airbows; muzzleloading design restrictions apply.


### General gun / Antlerless deer (not spotted fawns)

Dates: 2026-11-21 to 2026-11-29

Bag: Daily 2 deer; possession 4; annual 5, including no more than 2 antlerless.

Licenses: Hunting license and deer permit unless exempt. Check individual exemptions.

Methods: Lawful centerfire rifles, shotguns, handguns, muzzleloaders, PCP air guns, crossbows and bows.


Conditions for the whole scope:

- Statewide schedules apply outside the WMA system. Special deer-program permits and other statutory exceptions are outside this standard lookup.
- All harvested deer must be logged before moving and officially reported within 24 hours or earlier processing/transfer/out-of-state deadline. HuntIt is not the FWC reporting system.
- Check the linked FWC area notices for temporary closures; this local dataset does not poll live closures.
- License/permit exemptions require the relevant proof and conditions: youth under 16; Florida residents age 65+; qualifying homestead hunting in the county of residence; Florida residents holding the qualifying disability license; qualifying resident military members home on leave for at most 30 days with orders; authorized military/disabled-veteran events; and qualifying licensed-preserve patrons. Check the official exemption page. An exemption does not change season dates, bag limits, access permission or harvest reporting.
- Ordinary deer shooting hours are one-half hour before sunrise through one-half hour after sunset; specific area restrictions still apply.
- Arrows/bolts for deer require broadheads at least 7/8 inch wide. Deer PCP projectiles must meet the .30-caliber requirement; rimfire and nonexpanding full-metal-case ammunition are prohibited.
- Deer muzzleloaders firing one bullet must be at least .30 caliber; guns firing multiple balls must be 20 gauge or larger. Season-specific method limits still apply.
- Hunters age 16+ born on or after June 1, 1975 need hunter-safety certification before buying a hunting license, unless using a lawful supervised deferral.
- Private-land deer dogs require FWC property registration, identification collars, remote tracking/correction and written landowner permission. Dogs cannot take deer during archery, crossbow or muzzleloading seasons.

## Deer: private land, DMU C3, 2026-2027

Key: `deer-private-c3-2026-2027`. proposed revision of existing approved draft.

Scope: zone: C; dmu: C3

Review coverage: 2026-07-01 through 2027-06-30.

- [FWC 2026-2027 seasons and bag limits](https://myfwc.com/hunting/season-dates/) — checked 2026-10-12. Zone A-D antlered/antlerless dates and daily, possession, annual limits checked; excludes WMAs.
- [FWC recreational licenses and permits](https://myfwc.com/license/recreational/hunting/) — checked 2026-10-12. Hunting/deer and season permits checked; individual statutory exemptions require confirmation.
- [FWC general hunting rules](https://myfwc.com/hunting/regulations/general-information/) — checked 2026-10-12. Shooting hours, safety, access and general restrictions checked.
- [FWC deer harvest reporting](https://myfwc.com/hunting/deer/harvest-report/) — checked 2026-10-12. Log before moving and official reporting deadlines checked.
- [FWC youth deer weekend](https://myfwc.com/hunting/get-started/youth-deer-hunting/) — checked 2026-10-12. Eligible ages, supervision, no youth permit requirement and participating-adult restrictions checked.
- [FWC DMU A antler rules](https://myfwc.com/hunting/season-dates/dmu-a/) — checked 2026-10-12. DMU-specific antler criteria and location exceptions checked.
- [FWC DMU B antler rules](https://myfwc.com/hunting/season-dates/dmu-b/) — checked 2026-10-12. DMU-specific antler criteria and location exceptions checked.
- [FWC DMU C antler rules](https://myfwc.com/hunting/season-dates/dmu-c/) — checked 2026-10-12. DMU-specific antler criteria and location exceptions checked.
- [FWC DMU D antler rules](https://myfwc.com/hunting/season-dates/dmu-d/) — checked 2026-10-12. DMU-specific antler criteria and location exceptions checked.
- [FWC current area notices](https://myfwc.com/recreation/notices/) — checked 2026-10-12. Current closure directory checked; notices can change after this data check.
- [FWC conditional license exemptions](https://myfwc.com/license/recreational/do-i-need-one/) — checked 2026-10-12. Checked youth, resident senior and conditional exemptions; quota rules remain separate.
- [FWC legal deer equipment](https://myfwc.com/hunting/regulations/taking-game/) — checked 2026-10-12. Checked broadhead, PCP, muzzleloader and prohibited ammunition requirements.
- [FWC hunter safety](https://myfwc.com/hunting/safety-education/) — checked 2026-10-12. Checked birth-date/age certification requirement and supervised deferral option.

### Archery / Antlered deer

Dates: 2026-09-19 to 2026-10-18

Bag: Daily 2 deer; possession 4; annual 5, including no more than 2 antlerless.

Licenses: Hunting license and deer permit unless exempt. Archery season permit required unless exempt.

Methods: Bows only.

- For hunters 16+: one antler at least 5 inches long with 2 points of at least 1 inch.
- Youth 15 and under have a one-deer annual exception to DMU antler-point criteria; a 5-inch antler is still required.
- Spotted fawns may not be taken. Confirm the precise parcel, shooting hours, hunter safety and local restrictions.

### Crossbow / Antlered deer

Dates: 2026-09-19 to 2026-10-23

Bag: Daily 2 deer; possession 4; annual 5, including no more than 2 antlerless.

Licenses: Hunting license and deer permit unless exempt. Crossbow season permit required unless exempt.

Methods: Crossbows, bows and airbows.

- For hunters 16+: one antler at least 5 inches long with 2 points of at least 1 inch.
- Youth 15 and under have a one-deer annual exception to DMU antler-point criteria; a 5-inch antler is still required.
- Spotted fawns may not be taken. Confirm the precise parcel, shooting hours, hunter safety and local restrictions.

### Muzzleloading gun / Antlered deer

Dates: 2026-10-24 to 2026-11-06

Bag: Daily 2 deer; possession 4; annual 5, including no more than 2 antlerless.

Licenses: Hunting license and deer permit unless exempt. Muzzleloading gun season permit required unless exempt.

Methods: Muzzleloaders, crossbows, bows and airbows; muzzleloading design restrictions apply.

- For hunters 16+: one antler at least 5 inches long with 2 points of at least 1 inch.
- Youth 15 and under have a one-deer annual exception to DMU antler-point criteria; a 5-inch antler is still required.
- Spotted fawns may not be taken. Confirm the precise parcel, shooting hours, hunter safety and local restrictions.

### General gun / Antlered deer

Dates: 2026-11-07 to 2027-01-24

Bag: Daily 2 deer; possession 4; annual 5, including no more than 2 antlerless.

Licenses: Hunting license and deer permit unless exempt. Check individual exemptions.

Methods: Lawful centerfire rifles, shotguns, handguns, muzzleloaders, PCP air guns, crossbows and bows.

- For hunters 16+: one antler at least 5 inches long with 2 points of at least 1 inch.
- Youth 15 and under have a one-deer annual exception to DMU antler-point criteria; a 5-inch antler is still required.
- Spotted fawns may not be taken. Confirm the precise parcel, shooting hours, hunter safety and local restrictions.

### Youth weekend / Youth deer (DMU restrictions apply)

Dates: 2026-10-31 to 2026-11-01

Bag: 1 deer for the youth weekend, counted toward annual 5.

Licenses: No hunting license or permit for eligible youth 15 and under or an adult who only supervises. Participating adults have separate permit requirements.

Methods: Any legal method for an eligible youth hunter; supervision restrictions apply.

- Only hunters 15 and under, supervised by an adult 18+, qualify for the youth weekend; at most one antlered or antlerless deer where DMU restrictions permit.
- Participating adults 16+ need hunting, deer and muzzleloading permits unless exempt; muzzleloader/bow/crossbow and legal antlered deer only. Adults may not shoot during youth dog pursuits.
- For hunters 16+: one antler at least 5 inches long with 2 points of at least 1 inch.
- Youth 15 and under have a one-deer annual exception to DMU antler-point criteria; a 5-inch antler is still required.
- Spotted fawns may not be taken. Confirm the precise parcel, shooting hours, hunter safety and local restrictions.

### Archery / Antlerless deer (not spotted fawns)

Dates: 2026-09-19 to 2026-10-18

Bag: Daily 2 deer; possession 4; annual 5, including no more than 2 antlerless.

Licenses: Hunting license and deer permit unless exempt. Archery season permit required unless exempt.

Methods: Bows only.


### Crossbow / Antlerless deer (not spotted fawns)

Dates: 2026-09-19 to 2026-10-23

Bag: Daily 2 deer; possession 4; annual 5, including no more than 2 antlerless.

Licenses: Hunting license and deer permit unless exempt. Crossbow season permit required unless exempt.

Methods: Crossbows, bows and airbows.


### Muzzleloading gun / Antlerless deer (not spotted fawns)

Dates: 2026-10-24 to 2026-11-06

Bag: Daily 2 deer; possession 4; annual 5, including no more than 2 antlerless.

Licenses: Hunting license and deer permit unless exempt. Muzzleloading gun season permit required unless exempt.

Methods: Muzzleloaders, crossbows, bows and airbows; muzzleloading design restrictions apply.


### General gun / Antlerless deer (not spotted fawns)

Dates: 2026-11-21 to 2026-11-29

Bag: Daily 2 deer; possession 4; annual 5, including no more than 2 antlerless.

Licenses: Hunting license and deer permit unless exempt. Check individual exemptions.

Methods: Lawful centerfire rifles, shotguns, handguns, muzzleloaders, PCP air guns, crossbows and bows.


Conditions for the whole scope:

- Statewide schedules apply outside the WMA system. Special deer-program permits and other statutory exceptions are outside this standard lookup.
- All harvested deer must be logged before moving and officially reported within 24 hours or earlier processing/transfer/out-of-state deadline. HuntIt is not the FWC reporting system.
- Check the linked FWC area notices for temporary closures; this local dataset does not poll live closures.
- License/permit exemptions require the relevant proof and conditions: youth under 16; Florida residents age 65+; qualifying homestead hunting in the county of residence; Florida residents holding the qualifying disability license; qualifying resident military members home on leave for at most 30 days with orders; authorized military/disabled-veteran events; and qualifying licensed-preserve patrons. Check the official exemption page. An exemption does not change season dates, bag limits, access permission or harvest reporting.
- Ordinary deer shooting hours are one-half hour before sunrise through one-half hour after sunset; specific area restrictions still apply.
- Arrows/bolts for deer require broadheads at least 7/8 inch wide. Deer PCP projectiles must meet the .30-caliber requirement; rimfire and nonexpanding full-metal-case ammunition are prohibited.
- Deer muzzleloaders firing one bullet must be at least .30 caliber; guns firing multiple balls must be 20 gauge or larger. Season-specific method limits still apply.
- Hunters age 16+ born on or after June 1, 1975 need hunter-safety certification before buying a hunting license, unless using a lawful supervised deferral.
- Private-land deer dogs require FWC property registration, identification collars, remote tracking/correction and written landowner permission. Dogs cannot take deer during archery, crossbow or muzzleloading seasons.

## Deer: private land, DMU C4, 2026-2027

Key: `deer-private-c4-2026-2027`. proposed revision of existing approved draft.

Scope: zone: C; dmu: C4

Review coverage: 2026-07-01 through 2027-06-30.

- [FWC 2026-2027 seasons and bag limits](https://myfwc.com/hunting/season-dates/) — checked 2026-10-12. Zone A-D antlered/antlerless dates and daily, possession, annual limits checked; excludes WMAs.
- [FWC recreational licenses and permits](https://myfwc.com/license/recreational/hunting/) — checked 2026-10-12. Hunting/deer and season permits checked; individual statutory exemptions require confirmation.
- [FWC general hunting rules](https://myfwc.com/hunting/regulations/general-information/) — checked 2026-10-12. Shooting hours, safety, access and general restrictions checked.
- [FWC deer harvest reporting](https://myfwc.com/hunting/deer/harvest-report/) — checked 2026-10-12. Log before moving and official reporting deadlines checked.
- [FWC youth deer weekend](https://myfwc.com/hunting/get-started/youth-deer-hunting/) — checked 2026-10-12. Eligible ages, supervision, no youth permit requirement and participating-adult restrictions checked.
- [FWC DMU A antler rules](https://myfwc.com/hunting/season-dates/dmu-a/) — checked 2026-10-12. DMU-specific antler criteria and location exceptions checked.
- [FWC DMU B antler rules](https://myfwc.com/hunting/season-dates/dmu-b/) — checked 2026-10-12. DMU-specific antler criteria and location exceptions checked.
- [FWC DMU C antler rules](https://myfwc.com/hunting/season-dates/dmu-c/) — checked 2026-10-12. DMU-specific antler criteria and location exceptions checked.
- [FWC DMU D antler rules](https://myfwc.com/hunting/season-dates/dmu-d/) — checked 2026-10-12. DMU-specific antler criteria and location exceptions checked.
- [FWC current area notices](https://myfwc.com/recreation/notices/) — checked 2026-10-12. Current closure directory checked; notices can change after this data check.
- [FWC conditional license exemptions](https://myfwc.com/license/recreational/do-i-need-one/) — checked 2026-10-12. Checked youth, resident senior and conditional exemptions; quota rules remain separate.
- [FWC legal deer equipment](https://myfwc.com/hunting/regulations/taking-game/) — checked 2026-10-12. Checked broadhead, PCP, muzzleloader and prohibited ammunition requirements.
- [FWC hunter safety](https://myfwc.com/hunting/safety-education/) — checked 2026-10-12. Checked birth-date/age certification requirement and supervised deferral option.

### Archery / Antlered deer

Dates: 2026-09-19 to 2026-10-18

Bag: Daily 2 deer; possession 4; annual 5, including no more than 2 antlerless.

Licenses: Hunting license and deer permit unless exempt. Archery season permit required unless exempt.

Methods: Bows only.

- For hunters 16+: one antler at least 5 inches long with 3 points of at least 1 inch, or a main beam of at least 10 inches.
- Youth 15 and under have a one-deer annual exception to DMU antler-point criteria; a 5-inch antler is still required.
- Spotted fawns may not be taken. Confirm the precise parcel, shooting hours, hunter safety and local restrictions.

### Crossbow / Antlered deer

Dates: 2026-09-19 to 2026-10-23

Bag: Daily 2 deer; possession 4; annual 5, including no more than 2 antlerless.

Licenses: Hunting license and deer permit unless exempt. Crossbow season permit required unless exempt.

Methods: Crossbows, bows and airbows.

- For hunters 16+: one antler at least 5 inches long with 3 points of at least 1 inch, or a main beam of at least 10 inches.
- Youth 15 and under have a one-deer annual exception to DMU antler-point criteria; a 5-inch antler is still required.
- Spotted fawns may not be taken. Confirm the precise parcel, shooting hours, hunter safety and local restrictions.

### Muzzleloading gun / Antlered deer

Dates: 2026-10-24 to 2026-11-06

Bag: Daily 2 deer; possession 4; annual 5, including no more than 2 antlerless.

Licenses: Hunting license and deer permit unless exempt. Muzzleloading gun season permit required unless exempt.

Methods: Muzzleloaders, crossbows, bows and airbows; muzzleloading design restrictions apply.

- For hunters 16+: one antler at least 5 inches long with 3 points of at least 1 inch, or a main beam of at least 10 inches.
- Youth 15 and under have a one-deer annual exception to DMU antler-point criteria; a 5-inch antler is still required.
- Spotted fawns may not be taken. Confirm the precise parcel, shooting hours, hunter safety and local restrictions.

### General gun / Antlered deer

Dates: 2026-11-07 to 2027-01-24

Bag: Daily 2 deer; possession 4; annual 5, including no more than 2 antlerless.

Licenses: Hunting license and deer permit unless exempt. Check individual exemptions.

Methods: Lawful centerfire rifles, shotguns, handguns, muzzleloaders, PCP air guns, crossbows and bows.

- For hunters 16+: one antler at least 5 inches long with 3 points of at least 1 inch, or a main beam of at least 10 inches.
- Youth 15 and under have a one-deer annual exception to DMU antler-point criteria; a 5-inch antler is still required.
- Spotted fawns may not be taken. Confirm the precise parcel, shooting hours, hunter safety and local restrictions.

### Youth weekend / Youth deer (DMU restrictions apply)

Dates: 2026-10-31 to 2026-11-01

Bag: 1 deer for the youth weekend, counted toward annual 5.

Licenses: No hunting license or permit for eligible youth 15 and under or an adult who only supervises. Participating adults have separate permit requirements.

Methods: Any legal method for an eligible youth hunter; supervision restrictions apply.

- Only hunters 15 and under, supervised by an adult 18+, qualify for the youth weekend; at most one antlered or antlerless deer where DMU restrictions permit.
- Participating adults 16+ need hunting, deer and muzzleloading permits unless exempt; muzzleloader/bow/crossbow and legal antlered deer only. Adults may not shoot during youth dog pursuits.
- For hunters 16+: one antler at least 5 inches long with 3 points of at least 1 inch, or a main beam of at least 10 inches.
- Youth 15 and under have a one-deer annual exception to DMU antler-point criteria; a 5-inch antler is still required.
- Spotted fawns may not be taken. Confirm the precise parcel, shooting hours, hunter safety and local restrictions.

### Archery / Antlerless deer (not spotted fawns)

Dates: 2026-09-19 to 2026-10-18

Bag: Daily 2 deer; possession 4; annual 5, including no more than 2 antlerless.

Licenses: Hunting license and deer permit unless exempt. Archery season permit required unless exempt.

Methods: Bows only.


### Crossbow / Antlerless deer (not spotted fawns)

Dates: 2026-09-19 to 2026-10-23

Bag: Daily 2 deer; possession 4; annual 5, including no more than 2 antlerless.

Licenses: Hunting license and deer permit unless exempt. Crossbow season permit required unless exempt.

Methods: Crossbows, bows and airbows.


### Muzzleloading gun / Antlerless deer (not spotted fawns)

Dates: 2026-10-24 to 2026-11-06

Bag: Daily 2 deer; possession 4; annual 5, including no more than 2 antlerless.

Licenses: Hunting license and deer permit unless exempt. Muzzleloading gun season permit required unless exempt.

Methods: Muzzleloaders, crossbows, bows and airbows; muzzleloading design restrictions apply.


### General gun / Antlerless deer (not spotted fawns)

Dates: 2026-11-21 to 2026-11-29

Bag: Daily 2 deer; possession 4; annual 5, including no more than 2 antlerless.

Licenses: Hunting license and deer permit unless exempt. Check individual exemptions.

Methods: Lawful centerfire rifles, shotguns, handguns, muzzleloaders, PCP air guns, crossbows and bows.


Conditions for the whole scope:

- Statewide schedules apply outside the WMA system. Special deer-program permits and other statutory exceptions are outside this standard lookup.
- All harvested deer must be logged before moving and officially reported within 24 hours or earlier processing/transfer/out-of-state deadline. HuntIt is not the FWC reporting system.
- Check the linked FWC area notices for temporary closures; this local dataset does not poll live closures.
- License/permit exemptions require the relevant proof and conditions: youth under 16; Florida residents age 65+; qualifying homestead hunting in the county of residence; Florida residents holding the qualifying disability license; qualifying resident military members home on leave for at most 30 days with orders; authorized military/disabled-veteran events; and qualifying licensed-preserve patrons. Check the official exemption page. An exemption does not change season dates, bag limits, access permission or harvest reporting.
- Ordinary deer shooting hours are one-half hour before sunrise through one-half hour after sunset; specific area restrictions still apply.
- Arrows/bolts for deer require broadheads at least 7/8 inch wide. Deer PCP projectiles must meet the .30-caliber requirement; rimfire and nonexpanding full-metal-case ammunition are prohibited.
- Deer muzzleloaders firing one bullet must be at least .30 caliber; guns firing multiple balls must be 20 gauge or larger. Season-specific method limits still apply.
- Hunters age 16+ born on or after June 1, 1975 need hunter-safety certification before buying a hunting license, unless using a lawful supervised deferral.
- Private-land deer dogs require FWC property registration, identification collars, remote tracking/correction and written landowner permission. Dogs cannot take deer during archery, crossbow or muzzleloading seasons.

## Deer: private land, DMU C5, 2026-2027

Key: `deer-private-c5-2026-2027`. proposed revision of existing approved draft.

Scope: zone: C; dmu: C5

Review coverage: 2026-07-01 through 2027-06-30.

- [FWC 2026-2027 seasons and bag limits](https://myfwc.com/hunting/season-dates/) — checked 2026-10-12. Zone A-D antlered/antlerless dates and daily, possession, annual limits checked; excludes WMAs.
- [FWC recreational licenses and permits](https://myfwc.com/license/recreational/hunting/) — checked 2026-10-12. Hunting/deer and season permits checked; individual statutory exemptions require confirmation.
- [FWC general hunting rules](https://myfwc.com/hunting/regulations/general-information/) — checked 2026-10-12. Shooting hours, safety, access and general restrictions checked.
- [FWC deer harvest reporting](https://myfwc.com/hunting/deer/harvest-report/) — checked 2026-10-12. Log before moving and official reporting deadlines checked.
- [FWC youth deer weekend](https://myfwc.com/hunting/get-started/youth-deer-hunting/) — checked 2026-10-12. Eligible ages, supervision, no youth permit requirement and participating-adult restrictions checked.
- [FWC DMU A antler rules](https://myfwc.com/hunting/season-dates/dmu-a/) — checked 2026-10-12. DMU-specific antler criteria and location exceptions checked.
- [FWC DMU B antler rules](https://myfwc.com/hunting/season-dates/dmu-b/) — checked 2026-10-12. DMU-specific antler criteria and location exceptions checked.
- [FWC DMU C antler rules](https://myfwc.com/hunting/season-dates/dmu-c/) — checked 2026-10-12. DMU-specific antler criteria and location exceptions checked.
- [FWC DMU D antler rules](https://myfwc.com/hunting/season-dates/dmu-d/) — checked 2026-10-12. DMU-specific antler criteria and location exceptions checked.
- [FWC current area notices](https://myfwc.com/recreation/notices/) — checked 2026-10-12. Current closure directory checked; notices can change after this data check.
- [FWC conditional license exemptions](https://myfwc.com/license/recreational/do-i-need-one/) — checked 2026-10-12. Checked youth, resident senior and conditional exemptions; quota rules remain separate.
- [FWC legal deer equipment](https://myfwc.com/hunting/regulations/taking-game/) — checked 2026-10-12. Checked broadhead, PCP, muzzleloader and prohibited ammunition requirements.
- [FWC hunter safety](https://myfwc.com/hunting/safety-education/) — checked 2026-10-12. Checked birth-date/age certification requirement and supervised deferral option.

### Archery / Antlered deer

Dates: 2026-09-19 to 2026-10-18

Bag: Daily 2 deer; possession 4; annual 5, including no more than 2 antlerless.

Licenses: Hunting license and deer permit unless exempt. Archery season permit required unless exempt.

Methods: Bows only.

- For hunters 16+: one antler at least 5 inches long with 3 points of at least 1 inch, or a main beam of at least 10 inches.
- Youth 15 and under have a one-deer annual exception to DMU antler-point criteria; a 5-inch antler is still required.
- Spotted fawns may not be taken. Confirm the precise parcel, shooting hours, hunter safety and local restrictions.

### Crossbow / Antlered deer

Dates: 2026-09-19 to 2026-10-23

Bag: Daily 2 deer; possession 4; annual 5, including no more than 2 antlerless.

Licenses: Hunting license and deer permit unless exempt. Crossbow season permit required unless exempt.

Methods: Crossbows, bows and airbows.

- For hunters 16+: one antler at least 5 inches long with 3 points of at least 1 inch, or a main beam of at least 10 inches.
- Youth 15 and under have a one-deer annual exception to DMU antler-point criteria; a 5-inch antler is still required.
- Spotted fawns may not be taken. Confirm the precise parcel, shooting hours, hunter safety and local restrictions.

### Muzzleloading gun / Antlered deer

Dates: 2026-10-24 to 2026-11-06

Bag: Daily 2 deer; possession 4; annual 5, including no more than 2 antlerless.

Licenses: Hunting license and deer permit unless exempt. Muzzleloading gun season permit required unless exempt.

Methods: Muzzleloaders, crossbows, bows and airbows; muzzleloading design restrictions apply.

- For hunters 16+: one antler at least 5 inches long with 3 points of at least 1 inch, or a main beam of at least 10 inches.
- Youth 15 and under have a one-deer annual exception to DMU antler-point criteria; a 5-inch antler is still required.
- Spotted fawns may not be taken. Confirm the precise parcel, shooting hours, hunter safety and local restrictions.

### General gun / Antlered deer

Dates: 2026-11-07 to 2027-01-24

Bag: Daily 2 deer; possession 4; annual 5, including no more than 2 antlerless.

Licenses: Hunting license and deer permit unless exempt. Check individual exemptions.

Methods: Lawful centerfire rifles, shotguns, handguns, muzzleloaders, PCP air guns, crossbows and bows.

- For hunters 16+: one antler at least 5 inches long with 3 points of at least 1 inch, or a main beam of at least 10 inches.
- Youth 15 and under have a one-deer annual exception to DMU antler-point criteria; a 5-inch antler is still required.
- Spotted fawns may not be taken. Confirm the precise parcel, shooting hours, hunter safety and local restrictions.

### Youth weekend / Youth deer (DMU restrictions apply)

Dates: 2026-10-31 to 2026-11-01

Bag: 1 deer for the youth weekend, counted toward annual 5.

Licenses: No hunting license or permit for eligible youth 15 and under or an adult who only supervises. Participating adults have separate permit requirements.

Methods: Any legal method for an eligible youth hunter; supervision restrictions apply.

- Only hunters 15 and under, supervised by an adult 18+, qualify for the youth weekend; at most one antlered or antlerless deer where DMU restrictions permit.
- Participating adults 16+ need hunting, deer and muzzleloading permits unless exempt; muzzleloader/bow/crossbow and legal antlered deer only. Adults may not shoot during youth dog pursuits.
- For hunters 16+: one antler at least 5 inches long with 3 points of at least 1 inch, or a main beam of at least 10 inches.
- Youth 15 and under have a one-deer annual exception to DMU antler-point criteria; a 5-inch antler is still required.
- Spotted fawns may not be taken. Confirm the precise parcel, shooting hours, hunter safety and local restrictions.

### Archery / Antlerless deer (not spotted fawns)

Dates: 2026-09-19 to 2026-10-18

Bag: Daily 2 deer; possession 4; annual 5, including no more than 2 antlerless.

Licenses: Hunting license and deer permit unless exempt. Archery season permit required unless exempt.

Methods: Bows only.


### Crossbow / Antlerless deer (not spotted fawns)

Dates: 2026-09-19 to 2026-10-23

Bag: Daily 2 deer; possession 4; annual 5, including no more than 2 antlerless.

Licenses: Hunting license and deer permit unless exempt. Crossbow season permit required unless exempt.

Methods: Crossbows, bows and airbows.


### Muzzleloading gun / Antlerless deer (not spotted fawns)

Dates: 2026-10-24 to 2026-11-06

Bag: Daily 2 deer; possession 4; annual 5, including no more than 2 antlerless.

Licenses: Hunting license and deer permit unless exempt. Muzzleloading gun season permit required unless exempt.

Methods: Muzzleloaders, crossbows, bows and airbows; muzzleloading design restrictions apply.


### General gun / Antlerless deer (not spotted fawns)

Dates: 2026-11-07 to 2026-12-06

Bag: Daily 2 deer; possession 4; annual 5, including no more than 2 antlerless.

Licenses: Hunting license and deer permit unless exempt. Check individual exemptions.

Methods: Lawful centerfire rifles, shotguns, handguns, muzzleloaders, PCP air guns, crossbows and bows.


Conditions for the whole scope:

- Statewide schedules apply outside the WMA system. Special deer-program permits and other statutory exceptions are outside this standard lookup.
- All harvested deer must be logged before moving and officially reported within 24 hours or earlier processing/transfer/out-of-state deadline. HuntIt is not the FWC reporting system.
- Check the linked FWC area notices for temporary closures; this local dataset does not poll live closures.
- License/permit exemptions require the relevant proof and conditions: youth under 16; Florida residents age 65+; qualifying homestead hunting in the county of residence; Florida residents holding the qualifying disability license; qualifying resident military members home on leave for at most 30 days with orders; authorized military/disabled-veteran events; and qualifying licensed-preserve patrons. Check the official exemption page. An exemption does not change season dates, bag limits, access permission or harvest reporting.
- Ordinary deer shooting hours are one-half hour before sunrise through one-half hour after sunset; specific area restrictions still apply.
- Arrows/bolts for deer require broadheads at least 7/8 inch wide. Deer PCP projectiles must meet the .30-caliber requirement; rimfire and nonexpanding full-metal-case ammunition are prohibited.
- Deer muzzleloaders firing one bullet must be at least .30 caliber; guns firing multiple balls must be 20 gauge or larger. Season-specific method limits still apply.
- Hunters age 16+ born on or after June 1, 1975 need hunter-safety certification before buying a hunting license, unless using a lawful supervised deferral.
- Private-land deer dogs require FWC property registration, identification collars, remote tracking/correction and written landowner permission. Dogs cannot take deer during archery, crossbow or muzzleloading seasons.

## Deer: private land, DMU C6, 2026-2027

Key: `deer-private-c6-2026-2027`. proposed revision of existing approved draft.

Scope: zone: C; dmu: C6

Review coverage: 2026-07-01 through 2027-06-30.

- [FWC 2026-2027 seasons and bag limits](https://myfwc.com/hunting/season-dates/) — checked 2026-10-12. Zone A-D antlered/antlerless dates and daily, possession, annual limits checked; excludes WMAs.
- [FWC recreational licenses and permits](https://myfwc.com/license/recreational/hunting/) — checked 2026-10-12. Hunting/deer and season permits checked; individual statutory exemptions require confirmation.
- [FWC general hunting rules](https://myfwc.com/hunting/regulations/general-information/) — checked 2026-10-12. Shooting hours, safety, access and general restrictions checked.
- [FWC deer harvest reporting](https://myfwc.com/hunting/deer/harvest-report/) — checked 2026-10-12. Log before moving and official reporting deadlines checked.
- [FWC youth deer weekend](https://myfwc.com/hunting/get-started/youth-deer-hunting/) — checked 2026-10-12. Eligible ages, supervision, no youth permit requirement and participating-adult restrictions checked.
- [FWC DMU A antler rules](https://myfwc.com/hunting/season-dates/dmu-a/) — checked 2026-10-12. DMU-specific antler criteria and location exceptions checked.
- [FWC DMU B antler rules](https://myfwc.com/hunting/season-dates/dmu-b/) — checked 2026-10-12. DMU-specific antler criteria and location exceptions checked.
- [FWC DMU C antler rules](https://myfwc.com/hunting/season-dates/dmu-c/) — checked 2026-10-12. DMU-specific antler criteria and location exceptions checked.
- [FWC DMU D antler rules](https://myfwc.com/hunting/season-dates/dmu-d/) — checked 2026-10-12. DMU-specific antler criteria and location exceptions checked.
- [FWC current area notices](https://myfwc.com/recreation/notices/) — checked 2026-10-12. Current closure directory checked; notices can change after this data check.
- [FWC conditional license exemptions](https://myfwc.com/license/recreational/do-i-need-one/) — checked 2026-10-12. Checked youth, resident senior and conditional exemptions; quota rules remain separate.
- [FWC legal deer equipment](https://myfwc.com/hunting/regulations/taking-game/) — checked 2026-10-12. Checked broadhead, PCP, muzzleloader and prohibited ammunition requirements.
- [FWC hunter safety](https://myfwc.com/hunting/safety-education/) — checked 2026-10-12. Checked birth-date/age certification requirement and supervised deferral option.

### Archery / Antlered deer

Dates: 2026-09-19 to 2026-10-18

Bag: Daily 2 deer; possession 4; annual 5, including no more than 2 antlerless.

Licenses: Hunting license and deer permit unless exempt. Archery season permit required unless exempt.

Methods: Bows only.

- For hunters 16+: one antler at least 5 inches long with 3 points of at least 1 inch, or a main beam of at least 10 inches.
- Youth 15 and under have a one-deer annual exception to DMU antler-point criteria; a 5-inch antler is still required.
- Spotted fawns may not be taken. Confirm the precise parcel, shooting hours, hunter safety and local restrictions.

### Crossbow / Antlered deer

Dates: 2026-09-19 to 2026-10-23

Bag: Daily 2 deer; possession 4; annual 5, including no more than 2 antlerless.

Licenses: Hunting license and deer permit unless exempt. Crossbow season permit required unless exempt.

Methods: Crossbows, bows and airbows.

- For hunters 16+: one antler at least 5 inches long with 3 points of at least 1 inch, or a main beam of at least 10 inches.
- Youth 15 and under have a one-deer annual exception to DMU antler-point criteria; a 5-inch antler is still required.
- Spotted fawns may not be taken. Confirm the precise parcel, shooting hours, hunter safety and local restrictions.

### Muzzleloading gun / Antlered deer

Dates: 2026-10-24 to 2026-11-06

Bag: Daily 2 deer; possession 4; annual 5, including no more than 2 antlerless.

Licenses: Hunting license and deer permit unless exempt. Muzzleloading gun season permit required unless exempt.

Methods: Muzzleloaders, crossbows, bows and airbows; muzzleloading design restrictions apply.

- For hunters 16+: one antler at least 5 inches long with 3 points of at least 1 inch, or a main beam of at least 10 inches.
- Youth 15 and under have a one-deer annual exception to DMU antler-point criteria; a 5-inch antler is still required.
- Spotted fawns may not be taken. Confirm the precise parcel, shooting hours, hunter safety and local restrictions.

### General gun / Antlered deer

Dates: 2026-11-07 to 2027-01-24

Bag: Daily 2 deer; possession 4; annual 5, including no more than 2 antlerless.

Licenses: Hunting license and deer permit unless exempt. Check individual exemptions.

Methods: Lawful centerfire rifles, shotguns, handguns, muzzleloaders, PCP air guns, crossbows and bows.

- For hunters 16+: one antler at least 5 inches long with 3 points of at least 1 inch, or a main beam of at least 10 inches.
- Youth 15 and under have a one-deer annual exception to DMU antler-point criteria; a 5-inch antler is still required.
- Spotted fawns may not be taken. Confirm the precise parcel, shooting hours, hunter safety and local restrictions.

### Youth weekend / Youth deer (DMU restrictions apply)

Dates: 2026-10-31 to 2026-11-01

Bag: 1 deer for the youth weekend, counted toward annual 5.

Licenses: No hunting license or permit for eligible youth 15 and under or an adult who only supervises. Participating adults have separate permit requirements.

Methods: Any legal method for an eligible youth hunter; supervision restrictions apply.

- Only hunters 15 and under, supervised by an adult 18+, qualify for the youth weekend; at most one antlered or antlerless deer where DMU restrictions permit.
- Participating adults 16+ need hunting, deer and muzzleloading permits unless exempt; muzzleloader/bow/crossbow and legal antlered deer only. Adults may not shoot during youth dog pursuits.
- For hunters 16+: one antler at least 5 inches long with 3 points of at least 1 inch, or a main beam of at least 10 inches.
- Youth 15 and under have a one-deer annual exception to DMU antler-point criteria; a 5-inch antler is still required.
- Spotted fawns may not be taken. Confirm the precise parcel, shooting hours, hunter safety and local restrictions.

### Archery / Antlerless deer (not spotted fawns)

Dates: 2026-09-19 to 2026-10-18

Bag: Daily 2 deer; possession 4; annual 5, including no more than 2 antlerless.

Licenses: Hunting license and deer permit unless exempt. Archery season permit required unless exempt.

Methods: Bows only.


### Crossbow / Antlerless deer (not spotted fawns)

Dates: 2026-09-19 to 2026-10-23

Bag: Daily 2 deer; possession 4; annual 5, including no more than 2 antlerless.

Licenses: Hunting license and deer permit unless exempt. Crossbow season permit required unless exempt.

Methods: Crossbows, bows and airbows.


### Muzzleloading gun / Antlerless deer (not spotted fawns)

Dates: 2026-10-24 to 2026-11-06

Bag: Daily 2 deer; possession 4; annual 5, including no more than 2 antlerless.

Licenses: Hunting license and deer permit unless exempt. Muzzleloading gun season permit required unless exempt.

Methods: Muzzleloaders, crossbows, bows and airbows; muzzleloading design restrictions apply.


### General gun / Antlerless deer (not spotted fawns)

Dates: 2026-11-21 to 2026-11-29

Bag: Daily 2 deer; possession 4; annual 5, including no more than 2 antlerless.

Licenses: Hunting license and deer permit unless exempt. Check individual exemptions.

Methods: Lawful centerfire rifles, shotguns, handguns, muzzleloaders, PCP air guns, crossbows and bows.


Conditions for the whole scope:

- Statewide schedules apply outside the WMA system. Special deer-program permits and other statutory exceptions are outside this standard lookup.
- All harvested deer must be logged before moving and officially reported within 24 hours or earlier processing/transfer/out-of-state deadline. HuntIt is not the FWC reporting system.
- Check the linked FWC area notices for temporary closures; this local dataset does not poll live closures.
- License/permit exemptions require the relevant proof and conditions: youth under 16; Florida residents age 65+; qualifying homestead hunting in the county of residence; Florida residents holding the qualifying disability license; qualifying resident military members home on leave for at most 30 days with orders; authorized military/disabled-veteran events; and qualifying licensed-preserve patrons. Check the official exemption page. An exemption does not change season dates, bag limits, access permission or harvest reporting.
- Ordinary deer shooting hours are one-half hour before sunrise through one-half hour after sunset; specific area restrictions still apply.
- Arrows/bolts for deer require broadheads at least 7/8 inch wide. Deer PCP projectiles must meet the .30-caliber requirement; rimfire and nonexpanding full-metal-case ammunition are prohibited.
- Deer muzzleloaders firing one bullet must be at least .30 caliber; guns firing multiple balls must be 20 gauge or larger. Season-specific method limits still apply.
- Hunters age 16+ born on or after June 1, 1975 need hunter-safety certification before buying a hunting license, unless using a lawful supervised deferral.
- Private-land deer dogs require FWC property registration, identification collars, remote tracking/correction and written landowner permission. Dogs cannot take deer during archery, crossbow or muzzleloading seasons.

## Deer: private land, DMU D1, 2026-2027

Key: `deer-private-d1-2026-2027`. proposed revision of existing approved draft.

Scope: zone: D; dmu: D1

Review coverage: 2026-07-01 through 2027-06-30.

- [FWC 2026-2027 seasons and bag limits](https://myfwc.com/hunting/season-dates/) — checked 2026-10-12. Zone A-D antlered/antlerless dates and daily, possession, annual limits checked; excludes WMAs.
- [FWC recreational licenses and permits](https://myfwc.com/license/recreational/hunting/) — checked 2026-10-12. Hunting/deer and season permits checked; individual statutory exemptions require confirmation.
- [FWC general hunting rules](https://myfwc.com/hunting/regulations/general-information/) — checked 2026-10-12. Shooting hours, safety, access and general restrictions checked.
- [FWC deer harvest reporting](https://myfwc.com/hunting/deer/harvest-report/) — checked 2026-10-12. Log before moving and official reporting deadlines checked.
- [FWC youth deer weekend](https://myfwc.com/hunting/get-started/youth-deer-hunting/) — checked 2026-10-12. Eligible ages, supervision, no youth permit requirement and participating-adult restrictions checked.
- [FWC DMU A antler rules](https://myfwc.com/hunting/season-dates/dmu-a/) — checked 2026-10-12. DMU-specific antler criteria and location exceptions checked.
- [FWC DMU B antler rules](https://myfwc.com/hunting/season-dates/dmu-b/) — checked 2026-10-12. DMU-specific antler criteria and location exceptions checked.
- [FWC DMU C antler rules](https://myfwc.com/hunting/season-dates/dmu-c/) — checked 2026-10-12. DMU-specific antler criteria and location exceptions checked.
- [FWC DMU D antler rules](https://myfwc.com/hunting/season-dates/dmu-d/) — checked 2026-10-12. DMU-specific antler criteria and location exceptions checked.
- [FWC current area notices](https://myfwc.com/recreation/notices/) — checked 2026-10-12. Current closure directory checked; notices can change after this data check.
- [FWC conditional license exemptions](https://myfwc.com/license/recreational/do-i-need-one/) — checked 2026-10-12. Checked youth, resident senior and conditional exemptions; quota rules remain separate.
- [FWC legal deer equipment](https://myfwc.com/hunting/regulations/taking-game/) — checked 2026-10-12. Checked broadhead, PCP, muzzleloader and prohibited ammunition requirements.
- [FWC hunter safety](https://myfwc.com/hunting/safety-education/) — checked 2026-10-12. Checked birth-date/age certification requirement and supervised deferral option.

### Archery / Antlered deer

Dates: 2026-10-24 to 2026-11-25

Bag: Daily 2 deer; possession 4; annual 5, including no more than 2 antlerless.

Licenses: Hunting license and deer permit unless exempt. Archery season permit required unless exempt.

Methods: Bows only.

- For hunters 16+: one antler at least 5 inches long with 2 points of at least 1 inch.
- Youth 15 and under have a one-deer annual exception to DMU antler-point criteria; a 5-inch antler is still required.
- Spotted fawns may not be taken. Confirm the precise parcel, shooting hours, hunter safety and local restrictions.

### Crossbow / Antlered deer

Dates: 2026-10-24 to 2026-11-25; 2026-11-30 to 2026-12-04

Bag: Daily 2 deer; possession 4; annual 5, including no more than 2 antlerless.

Licenses: Hunting license and deer permit unless exempt. Crossbow season permit required unless exempt.

Methods: Crossbows, bows and airbows.

- For hunters 16+: one antler at least 5 inches long with 2 points of at least 1 inch.
- Youth 15 and under have a one-deer annual exception to DMU antler-point criteria; a 5-inch antler is still required.
- Spotted fawns may not be taken. Confirm the precise parcel, shooting hours, hunter safety and local restrictions.

### Muzzleloading gun / Antlered deer

Dates: 2026-12-05 to 2026-12-11; 2027-02-22 to 2027-02-28

Bag: Daily 2 deer; possession 4; annual 5, including no more than 2 antlerless.

Licenses: Hunting license and deer permit unless exempt. Muzzleloading gun season permit required unless exempt.

Methods: Muzzleloaders, crossbows, bows and airbows; muzzleloading design restrictions apply.

- For hunters 16+: one antler at least 5 inches long with 2 points of at least 1 inch.
- Youth 15 and under have a one-deer annual exception to DMU antler-point criteria; a 5-inch antler is still required.
- Spotted fawns may not be taken. Confirm the precise parcel, shooting hours, hunter safety and local restrictions.

### General gun / Antlered deer

Dates: 2026-11-26 to 2026-11-29; 2026-12-12 to 2027-02-21

Bag: Daily 2 deer; possession 4; annual 5, including no more than 2 antlerless.

Licenses: Hunting license and deer permit unless exempt. Check individual exemptions.

Methods: Lawful centerfire rifles, shotguns, handguns, muzzleloaders, PCP air guns, crossbows and bows.

- For hunters 16+: one antler at least 5 inches long with 2 points of at least 1 inch.
- Youth 15 and under have a one-deer annual exception to DMU antler-point criteria; a 5-inch antler is still required.
- Spotted fawns may not be taken. Confirm the precise parcel, shooting hours, hunter safety and local restrictions.

### Youth weekend / Youth deer (DMU restrictions apply)

Dates: 2026-12-05 to 2026-12-06

Bag: 1 deer for the youth weekend, counted toward annual 5.

Licenses: No hunting license or permit for eligible youth 15 and under or an adult who only supervises. Participating adults have separate permit requirements.

Methods: Any legal method for an eligible youth hunter; supervision restrictions apply.

- Only hunters 15 and under, supervised by an adult 18+, qualify for the youth weekend; at most one antlered or antlerless deer where DMU restrictions permit.
- Participating adults 16+ need hunting, deer and muzzleloading permits unless exempt; muzzleloader/bow/crossbow and legal antlered deer only. Adults may not shoot during youth dog pursuits.
- For hunters 16+: one antler at least 5 inches long with 2 points of at least 1 inch.
- Youth 15 and under have a one-deer annual exception to DMU antler-point criteria; a 5-inch antler is still required.
- Spotted fawns may not be taken. Confirm the precise parcel, shooting hours, hunter safety and local restrictions.

### Archery / Antlerless deer (not spotted fawns)

Dates: 2026-10-24 to 2026-11-25

Bag: Daily 2 deer; possession 4; annual 5, including no more than 2 antlerless.

Licenses: Hunting license and deer permit unless exempt. Archery season permit required unless exempt.

Methods: Bows only.


### Crossbow / Antlerless deer (not spotted fawns)

Dates: 2026-10-24 to 2026-11-25; 2026-11-30 to 2026-12-04

Bag: Daily 2 deer; possession 4; annual 5, including no more than 2 antlerless.

Licenses: Hunting license and deer permit unless exempt. Crossbow season permit required unless exempt.

Methods: Crossbows, bows and airbows.


### Muzzleloading gun / Antlerless deer (not spotted fawns)

Dates: 2026-12-05 to 2026-12-11; 2027-02-22 to 2027-02-28

Bag: Daily 2 deer; possession 4; annual 5, including no more than 2 antlerless.

Licenses: Hunting license and deer permit unless exempt. Muzzleloading gun season permit required unless exempt.

Methods: Muzzleloaders, crossbows, bows and airbows; muzzleloading design restrictions apply.


### General gun / Antlerless deer (not spotted fawns)

Dates: 2026-11-26 to 2026-11-29; 2026-12-12 to 2027-02-21

Bag: Daily 2 deer; possession 4; annual 5, including no more than 2 antlerless.

Licenses: Hunting license and deer permit unless exempt. Check individual exemptions.

Methods: Lawful centerfire rifles, shotguns, handguns, muzzleloaders, PCP air guns, crossbows and bows.


Conditions for the whole scope:

- Statewide schedules apply outside the WMA system. Special deer-program permits and other statutory exceptions are outside this standard lookup.
- All harvested deer must be logged before moving and officially reported within 24 hours or earlier processing/transfer/out-of-state deadline. HuntIt is not the FWC reporting system.
- Check the linked FWC area notices for temporary closures; this local dataset does not poll live closures.
- License/permit exemptions require the relevant proof and conditions: youth under 16; Florida residents age 65+; qualifying homestead hunting in the county of residence; Florida residents holding the qualifying disability license; qualifying resident military members home on leave for at most 30 days with orders; authorized military/disabled-veteran events; and qualifying licensed-preserve patrons. Check the official exemption page. An exemption does not change season dates, bag limits, access permission or harvest reporting.
- Ordinary deer shooting hours are one-half hour before sunrise through one-half hour after sunset; specific area restrictions still apply.
- Arrows/bolts for deer require broadheads at least 7/8 inch wide. Deer PCP projectiles must meet the .30-caliber requirement; rimfire and nonexpanding full-metal-case ammunition are prohibited.
- Deer muzzleloaders firing one bullet must be at least .30 caliber; guns firing multiple balls must be 20 gauge or larger. Season-specific method limits still apply.
- Hunters age 16+ born on or after June 1, 1975 need hunter-safety certification before buying a hunting license, unless using a lawful supervised deferral.
- Private-land deer dogs require FWC property registration, identification collars, remote tracking/correction and written landowner permission. Dogs cannot take deer during archery, crossbow or muzzleloading seasons.

## Deer: private land, DMU D2, 2026-2027

Key: `deer-private-d2-2026-2027`. proposed revision of existing approved draft.

Scope: zone: D; dmu: D2

Review coverage: 2026-07-01 through 2027-06-30.

- [FWC 2026-2027 seasons and bag limits](https://myfwc.com/hunting/season-dates/) — checked 2026-10-12. Zone A-D antlered/antlerless dates and daily, possession, annual limits checked; excludes WMAs.
- [FWC recreational licenses and permits](https://myfwc.com/license/recreational/hunting/) — checked 2026-10-12. Hunting/deer and season permits checked; individual statutory exemptions require confirmation.
- [FWC general hunting rules](https://myfwc.com/hunting/regulations/general-information/) — checked 2026-10-12. Shooting hours, safety, access and general restrictions checked.
- [FWC deer harvest reporting](https://myfwc.com/hunting/deer/harvest-report/) — checked 2026-10-12. Log before moving and official reporting deadlines checked.
- [FWC youth deer weekend](https://myfwc.com/hunting/get-started/youth-deer-hunting/) — checked 2026-10-12. Eligible ages, supervision, no youth permit requirement and participating-adult restrictions checked.
- [FWC DMU A antler rules](https://myfwc.com/hunting/season-dates/dmu-a/) — checked 2026-10-12. DMU-specific antler criteria and location exceptions checked.
- [FWC DMU B antler rules](https://myfwc.com/hunting/season-dates/dmu-b/) — checked 2026-10-12. DMU-specific antler criteria and location exceptions checked.
- [FWC DMU C antler rules](https://myfwc.com/hunting/season-dates/dmu-c/) — checked 2026-10-12. DMU-specific antler criteria and location exceptions checked.
- [FWC DMU D antler rules](https://myfwc.com/hunting/season-dates/dmu-d/) — checked 2026-10-12. DMU-specific antler criteria and location exceptions checked.
- [FWC current area notices](https://myfwc.com/recreation/notices/) — checked 2026-10-12. Current closure directory checked; notices can change after this data check.
- [FWC conditional license exemptions](https://myfwc.com/license/recreational/do-i-need-one/) — checked 2026-10-12. Checked youth, resident senior and conditional exemptions; quota rules remain separate.
- [FWC legal deer equipment](https://myfwc.com/hunting/regulations/taking-game/) — checked 2026-10-12. Checked broadhead, PCP, muzzleloader and prohibited ammunition requirements.
- [FWC hunter safety](https://myfwc.com/hunting/safety-education/) — checked 2026-10-12. Checked birth-date/age certification requirement and supervised deferral option.

### Archery / Antlered deer

Dates: 2026-10-24 to 2026-11-25

Bag: Daily 2 deer; possession 4; annual 5, including no more than 3 antlerless in DMU D2 outside WMAs.

Licenses: Hunting license and deer permit unless exempt. Archery season permit required unless exempt.

Methods: Bows only.

- For hunters 16+: one antler at least 5 inches long with 3 points of at least 1 inch, or a main beam of at least 10 inches.
- Youth 15 and under have a one-deer annual exception to DMU antler-point criteria; a 5-inch antler is still required.
- Spotted fawns may not be taken. Confirm the precise parcel, shooting hours, hunter safety and local restrictions.

### Crossbow / Antlered deer

Dates: 2026-10-24 to 2026-11-25; 2026-11-30 to 2026-12-04

Bag: Daily 2 deer; possession 4; annual 5, including no more than 3 antlerless in DMU D2 outside WMAs.

Licenses: Hunting license and deer permit unless exempt. Crossbow season permit required unless exempt.

Methods: Crossbows, bows and airbows.

- For hunters 16+: one antler at least 5 inches long with 3 points of at least 1 inch, or a main beam of at least 10 inches.
- Youth 15 and under have a one-deer annual exception to DMU antler-point criteria; a 5-inch antler is still required.
- Spotted fawns may not be taken. Confirm the precise parcel, shooting hours, hunter safety and local restrictions.

### Muzzleloading gun / Antlered deer

Dates: 2026-12-05 to 2026-12-11; 2027-02-22 to 2027-02-28

Bag: Daily 2 deer; possession 4; annual 5, including no more than 3 antlerless in DMU D2 outside WMAs.

Licenses: Hunting license and deer permit unless exempt. Muzzleloading gun season permit required unless exempt.

Methods: Muzzleloaders, crossbows, bows and airbows; muzzleloading design restrictions apply.

- For hunters 16+: one antler at least 5 inches long with 3 points of at least 1 inch, or a main beam of at least 10 inches.
- Youth 15 and under have a one-deer annual exception to DMU antler-point criteria; a 5-inch antler is still required.
- Spotted fawns may not be taken. Confirm the precise parcel, shooting hours, hunter safety and local restrictions.

### General gun / Antlered deer

Dates: 2026-11-26 to 2026-11-29; 2026-12-12 to 2027-02-21

Bag: Daily 2 deer; possession 4; annual 5, including no more than 3 antlerless in DMU D2 outside WMAs.

Licenses: Hunting license and deer permit unless exempt. Check individual exemptions.

Methods: Lawful centerfire rifles, shotguns, handguns, muzzleloaders, PCP air guns, crossbows and bows.

- For hunters 16+: one antler at least 5 inches long with 3 points of at least 1 inch, or a main beam of at least 10 inches.
- Youth 15 and under have a one-deer annual exception to DMU antler-point criteria; a 5-inch antler is still required.
- Spotted fawns may not be taken. Confirm the precise parcel, shooting hours, hunter safety and local restrictions.

### Youth weekend / Youth deer (DMU restrictions apply)

Dates: 2026-12-05 to 2026-12-06

Bag: 1 deer for the youth weekend, counted toward annual 5.

Licenses: No hunting license or permit for eligible youth 15 and under or an adult who only supervises. Participating adults have separate permit requirements.

Methods: Any legal method for an eligible youth hunter; supervision restrictions apply.

- Only hunters 15 and under, supervised by an adult 18+, qualify for the youth weekend; at most one antlered or antlerless deer where DMU restrictions permit.
- Participating adults 16+ need hunting, deer and muzzleloading permits unless exempt; muzzleloader/bow/crossbow and legal antlered deer only. Adults may not shoot during youth dog pursuits.
- For hunters 16+: one antler at least 5 inches long with 3 points of at least 1 inch, or a main beam of at least 10 inches.
- Youth 15 and under have a one-deer annual exception to DMU antler-point criteria; a 5-inch antler is still required.
- Spotted fawns may not be taken. Confirm the precise parcel, shooting hours, hunter safety and local restrictions.

### Archery / Antlerless deer (not spotted fawns)

Dates: 2026-10-24 to 2026-11-25

Bag: Daily 2 deer; possession 4; annual 5, including no more than 3 antlerless in DMU D2 outside WMAs.

Licenses: Hunting license and deer permit unless exempt. Archery season permit required unless exempt.

Methods: Bows only.


### Crossbow / Antlerless deer (not spotted fawns)

Dates: 2026-10-24 to 2026-11-25; 2026-11-30 to 2026-12-04

Bag: Daily 2 deer; possession 4; annual 5, including no more than 3 antlerless in DMU D2 outside WMAs.

Licenses: Hunting license and deer permit unless exempt. Crossbow season permit required unless exempt.

Methods: Crossbows, bows and airbows.


### Muzzleloading gun / Antlerless deer (not spotted fawns)

Dates: 2026-12-05 to 2026-12-11; 2027-02-22 to 2027-02-28

Bag: Daily 2 deer; possession 4; annual 5, including no more than 3 antlerless in DMU D2 outside WMAs.

Licenses: Hunting license and deer permit unless exempt. Muzzleloading gun season permit required unless exempt.

Methods: Muzzleloaders, crossbows, bows and airbows; muzzleloading design restrictions apply.


### General gun / Antlerless deer (not spotted fawns)

Dates: 2026-11-26 to 2026-11-29; 2026-12-12 to 2027-02-21

Bag: Daily 2 deer; possession 4; annual 5, including no more than 3 antlerless in DMU D2 outside WMAs.

Licenses: Hunting license and deer permit unless exempt. Check individual exemptions.

Methods: Lawful centerfire rifles, shotguns, handguns, muzzleloaders, PCP air guns, crossbows and bows.


Conditions for the whole scope:

- Statewide schedules apply outside the WMA system. Special deer-program permits and other statutory exceptions are outside this standard lookup.
- All harvested deer must be logged before moving and officially reported within 24 hours or earlier processing/transfer/out-of-state deadline. HuntIt is not the FWC reporting system.
- Check the linked FWC area notices for temporary closures; this local dataset does not poll live closures.
- License/permit exemptions require the relevant proof and conditions: youth under 16; Florida residents age 65+; qualifying homestead hunting in the county of residence; Florida residents holding the qualifying disability license; qualifying resident military members home on leave for at most 30 days with orders; authorized military/disabled-veteran events; and qualifying licensed-preserve patrons. Check the official exemption page. An exemption does not change season dates, bag limits, access permission or harvest reporting.
- Ordinary deer shooting hours are one-half hour before sunrise through one-half hour after sunset; specific area restrictions still apply.
- Arrows/bolts for deer require broadheads at least 7/8 inch wide. Deer PCP projectiles must meet the .30-caliber requirement; rimfire and nonexpanding full-metal-case ammunition are prohibited.
- Deer muzzleloaders firing one bullet must be at least .30 caliber; guns firing multiple balls must be 20 gauge or larger. Season-specific method limits still apply.
- Hunters age 16+ born on or after June 1, 1975 need hunter-safety certification before buying a hunting license, unless using a lawful supervised deferral.
- Private-land deer dogs require FWC property registration, identification collars, remote tracking/correction and written landowner permission. Dogs cannot take deer during archery, crossbow or muzzleloading seasons.

## White Tailed Deer: Rotenberger WMA / Wildlife Management Area (WMA), 2026-2027 expansion

Key: `deer-rotenberger-2-2026-2027-expanded`. new draft.

Scope: managed_area: Rotenberger WMA

Review coverage: 2026-07-01 through 2027-06-30.

- [FWC Rotenberger WMA 2026-2027 regulations and map](https://app.myfwc.com/hgm/hgmsearch/wmad?brochureTitle=Rotenberger) — checked 2026-10-12. Interactive brochure checked: area dates, legal species, bag limits, methods, permits, access and exceptions; PDF map available on the same page.
- [FWC hunting licenses and permits](https://myfwc.com/license/recreational/hunting/) — checked 2026-10-12. General license, management-area and season permits; brochure exemptions and area-specific quota restrictions retained.
- [FWC legal resident-game equipment](https://myfwc.com/hunting/regulations/taking-game/) — checked 2026-10-12. Checked broadhead minimum width, species-specific PCP minimums and deer muzzleloader design requirements; area season-method restrictions remain controlling.

### Archery / Antlered deer only

Dates: 2026-08-08 to 2026-08-30

Bag: Area season limit 1 antlered deer during archery, muzzleloading gun and general gun-walk seasons. Statewide annual limit 5 deer, including no more than 2 antlerless; daily 2 and possession 4 also apply.

Licenses: Hunting license, management area permit and deer permit required unless exempt. Nonresident game hunters require an annual hunting license. Archery season permit required unless exempt. No quota permit required for this listed season.

Methods: Bows only; crossbows, airbows and draw-lock bows require the brochure's Persons With Disabilities Crossbow Permit exception.

- Entry/exit is limited to the L-4, Powerline, Miami Canal and Manley Ditch levees. Hunting on roads, ramps, parking/camping areas, levees or adjacent powerline pads, and gun hunting on/from/across levees, is prohibited.
- Vehicle, scouting-period and flag requirements apply; airboats are prohibited during archery, muzzleloading and general gun-walk seasons. Do not infer a general gun-vehicle hunt from access text: the 2026-2027 brochure lists none.
- Dogs may not hunt deer or wild hog. Leashed dogs may trail wounded game, subject to the brochure's restrictions.
- When weekend check stations are staffed, check deer at the southeast Holey Land station before quartering, dismembering or removing them.
- Antlered deer must have at least one antler 5 inches or longer with at least 2 points, each at least 1 inch. Youth under 16 have the statewide one-deer annual antler-point exception, still requiring a 5-inch antler. Antlerless deer and spotted fawns are not authorized by these area seasons.
- Arrows and bolts used for deer must have broadheads at least 7/8 inch wide. Any otherwise-authorized deer PCP airgun projectile must satisfy the statewide .30-caliber minimum; this does not authorize PCP equipment during bows-only or muzzleloader-only seasons.
- Muzzleloaders used for deer must be at least .30 caliber for a single bullet or at least 20 gauge when firing 2 or more balls.
- Log harvested deer before moving them and report to FWC within 24 hours of recovery, in addition to the area's check-station duties.

### Muzzleloading gun / Antlered deer only

Dates: 2026-09-05 to 2026-09-13

Bag: Area season limit 1 antlered deer during archery, muzzleloading gun and general gun-walk seasons. Statewide annual limit 5 deer, including no more than 2 antlerless; daily 2 and possession 4 also apply.

Licenses: Hunting license, management area permit and deer permit required unless exempt. Nonresident game hunters require an annual hunting license. Muzzleloading gun season permit required unless exempt. No quota permit required for this listed season.

Methods: Muzzleloading guns only for deer or hog; ordinary archery equipment is prohibited.

- Entry/exit is limited to the L-4, Powerline, Miami Canal and Manley Ditch levees. Hunting on roads, ramps, parking/camping areas, levees or adjacent powerline pads, and gun hunting on/from/across levees, is prohibited.
- Vehicle, scouting-period and flag requirements apply; airboats are prohibited during archery, muzzleloading and general gun-walk seasons. Do not infer a general gun-vehicle hunt from access text: the 2026-2027 brochure lists none.
- Dogs may not hunt deer or wild hog. Leashed dogs may trail wounded game, subject to the brochure's restrictions.
- When weekend check stations are staffed, check deer at the southeast Holey Land station before quartering, dismembering or removing them.
- Antlered deer must have at least one antler 5 inches or longer with at least 2 points, each at least 1 inch. Youth under 16 have the statewide one-deer annual antler-point exception, still requiring a 5-inch antler. Antlerless deer and spotted fawns are not authorized by these area seasons.
- Arrows and bolts used for deer must have broadheads at least 7/8 inch wide. Any otherwise-authorized deer PCP airgun projectile must satisfy the statewide .30-caliber minimum; this does not authorize PCP equipment during bows-only or muzzleloader-only seasons.
- Muzzleloaders used for deer must be at least .30 caliber for a single bullet or at least 20 gauge when firing 2 or more balls.
- Log harvested deer before moving them and report to FWC within 24 hours of recovery, in addition to the area's check-station duties.

### General gun-walk / Antlered deer only

Dates: 2026-10-03 to 2026-10-18

Bag: Area season limit 1 antlered deer during archery, muzzleloading gun and general gun-walk seasons. Statewide annual limit 5 deer, including no more than 2 antlerless; daily 2 and possession 4 also apply.

Licenses: Hunting license, management area permit and deer permit required unless exempt. Nonresident game hunters require an annual hunting license. No quota permit required for this listed season.

Methods: Lawful shotguns, rifles, muzzleloading guns, pistols, airguns, bows and crossbows, subject to brochure restrictions. No rimfire or non-expanding full-metal-jacket ammunition for deer; PCP airguns must propel a bolt, arrow or bullet of at least .30 caliber.

- Entry/exit is limited to the L-4, Powerline, Miami Canal and Manley Ditch levees. Hunting on roads, ramps, parking/camping areas, levees or adjacent powerline pads, and gun hunting on/from/across levees, is prohibited.
- Vehicle, scouting-period and flag requirements apply; airboats are prohibited during archery, muzzleloading and general gun-walk seasons. Do not infer a general gun-vehicle hunt from access text: the 2026-2027 brochure lists none.
- Dogs may not hunt deer or wild hog. Leashed dogs may trail wounded game, subject to the brochure's restrictions.
- When weekend check stations are staffed, check deer at the southeast Holey Land station before quartering, dismembering or removing them.
- Antlered deer must have at least one antler 5 inches or longer with at least 2 points, each at least 1 inch. Youth under 16 have the statewide one-deer annual antler-point exception, still requiring a 5-inch antler. Antlerless deer and spotted fawns are not authorized by these area seasons.
- Arrows and bolts used for deer must have broadheads at least 7/8 inch wide. Any otherwise-authorized deer PCP airgun projectile must satisfy the statewide .30-caliber minimum; this does not authorize PCP equipment during bows-only or muzzleloader-only seasons.
- Muzzleloaders used for deer must be at least .30 caliber for a single bullet or at least 20 gauge when firing 2 or more balls.
- Log harvested deer before moving them and report to FWC within 24 hours of recovery, in addition to the area's check-station duties.

Conditions for the whole scope:

- Hunting over bait, taking swimming deer or spotted fawns, and hunting in posted closed areas are prohibited.
- Ordinary shooting hours are half an hour before sunrise through half an hour after sunset; turkey has separate hours.
- Night gun hunting, fully automatic firearms and centerfire semiautomatic rifles with magazines capable of more than 5 rounds are prohibited.
- Deer hunters and companions need 500 square inches of fluorescent orange above the waist, except bow-and-arrow hunting during archery season.
- Brochure license/permit exemptions include children under 16, Florida residents 65+, residents with a qualifying disabled-person certificate, and qualifying resident military personnel home on leave. They do not override quota permits marked no exemptions or required deer tags. Hunters born on/after June 1, 1975 need hunter-safety certification or the lawful supervised mentoring exception. Youth require adult supervision; mentoring license holders require a licensed supervisor aged 21+. Consult the complete brochure.
- The official brochure includes PDF BROCHURE and PDF MAP ONLY controls. Follow its current maps, access restrictions and FWC closure notices.

## White Tailed Deer: Rotenberger WMA / Commission-Managed Land, 2026-2027 expansion

Key: `deer-rotenberger-3-2026-2027-expanded`. new draft.

Scope: managed_area: Rotenberger WMA

Review coverage: 2026-07-01 through 2027-06-30.

- [FWC Rotenberger WMA 2026-2027 regulations and map](https://app.myfwc.com/hgm/hgmsearch/wmad?brochureTitle=Rotenberger) — checked 2026-10-12. Interactive brochure checked: area dates, legal species, bag limits, methods, permits, access and exceptions; PDF map available on the same page.
- [FWC hunting licenses and permits](https://myfwc.com/license/recreational/hunting/) — checked 2026-10-12. General license, management-area and season permits; brochure exemptions and area-specific quota restrictions retained.
- [FWC legal resident-game equipment](https://myfwc.com/hunting/regulations/taking-game/) — checked 2026-10-12. Checked broadhead minimum width, species-specific PCP minimums and deer muzzleloader design requirements; area season-method restrictions remain controlling.

### Archery / Antlered deer only

Dates: 2026-08-08 to 2026-08-30

Bag: Area season limit 1 antlered deer during archery, muzzleloading gun and general gun-walk seasons. Statewide annual limit 5 deer, including no more than 2 antlerless; daily 2 and possession 4 also apply.

Licenses: Hunting license, management area permit and deer permit required unless exempt. Nonresident game hunters require an annual hunting license. Archery season permit required unless exempt. No quota permit required for this listed season.

Methods: Bows only; crossbows, airbows and draw-lock bows require the brochure's Persons With Disabilities Crossbow Permit exception.

- Entry/exit is limited to the L-4, Powerline, Miami Canal and Manley Ditch levees. Hunting on roads, ramps, parking/camping areas, levees or adjacent powerline pads, and gun hunting on/from/across levees, is prohibited.
- Vehicle, scouting-period and flag requirements apply; airboats are prohibited during archery, muzzleloading and general gun-walk seasons. Do not infer a general gun-vehicle hunt from access text: the 2026-2027 brochure lists none.
- Dogs may not hunt deer or wild hog. Leashed dogs may trail wounded game, subject to the brochure's restrictions.
- When weekend check stations are staffed, check deer at the southeast Holey Land station before quartering, dismembering or removing them.
- Antlered deer must have at least one antler 5 inches or longer with at least 2 points, each at least 1 inch. Youth under 16 have the statewide one-deer annual antler-point exception, still requiring a 5-inch antler. Antlerless deer and spotted fawns are not authorized by these area seasons.
- Arrows and bolts used for deer must have broadheads at least 7/8 inch wide. Any otherwise-authorized deer PCP airgun projectile must satisfy the statewide .30-caliber minimum; this does not authorize PCP equipment during bows-only or muzzleloader-only seasons.
- Muzzleloaders used for deer must be at least .30 caliber for a single bullet or at least 20 gauge when firing 2 or more balls.
- Log harvested deer before moving them and report to FWC within 24 hours of recovery, in addition to the area's check-station duties.

### Muzzleloading gun / Antlered deer only

Dates: 2026-09-05 to 2026-09-13

Bag: Area season limit 1 antlered deer during archery, muzzleloading gun and general gun-walk seasons. Statewide annual limit 5 deer, including no more than 2 antlerless; daily 2 and possession 4 also apply.

Licenses: Hunting license, management area permit and deer permit required unless exempt. Nonresident game hunters require an annual hunting license. Muzzleloading gun season permit required unless exempt. No quota permit required for this listed season.

Methods: Muzzleloading guns only for deer or hog; ordinary archery equipment is prohibited.

- Entry/exit is limited to the L-4, Powerline, Miami Canal and Manley Ditch levees. Hunting on roads, ramps, parking/camping areas, levees or adjacent powerline pads, and gun hunting on/from/across levees, is prohibited.
- Vehicle, scouting-period and flag requirements apply; airboats are prohibited during archery, muzzleloading and general gun-walk seasons. Do not infer a general gun-vehicle hunt from access text: the 2026-2027 brochure lists none.
- Dogs may not hunt deer or wild hog. Leashed dogs may trail wounded game, subject to the brochure's restrictions.
- When weekend check stations are staffed, check deer at the southeast Holey Land station before quartering, dismembering or removing them.
- Antlered deer must have at least one antler 5 inches or longer with at least 2 points, each at least 1 inch. Youth under 16 have the statewide one-deer annual antler-point exception, still requiring a 5-inch antler. Antlerless deer and spotted fawns are not authorized by these area seasons.
- Arrows and bolts used for deer must have broadheads at least 7/8 inch wide. Any otherwise-authorized deer PCP airgun projectile must satisfy the statewide .30-caliber minimum; this does not authorize PCP equipment during bows-only or muzzleloader-only seasons.
- Muzzleloaders used for deer must be at least .30 caliber for a single bullet or at least 20 gauge when firing 2 or more balls.
- Log harvested deer before moving them and report to FWC within 24 hours of recovery, in addition to the area's check-station duties.

### General gun-walk / Antlered deer only

Dates: 2026-10-03 to 2026-10-18

Bag: Area season limit 1 antlered deer during archery, muzzleloading gun and general gun-walk seasons. Statewide annual limit 5 deer, including no more than 2 antlerless; daily 2 and possession 4 also apply.

Licenses: Hunting license, management area permit and deer permit required unless exempt. Nonresident game hunters require an annual hunting license. No quota permit required for this listed season.

Methods: Lawful shotguns, rifles, muzzleloading guns, pistols, airguns, bows and crossbows, subject to brochure restrictions. No rimfire or non-expanding full-metal-jacket ammunition for deer; PCP airguns must propel a bolt, arrow or bullet of at least .30 caliber.

- Entry/exit is limited to the L-4, Powerline, Miami Canal and Manley Ditch levees. Hunting on roads, ramps, parking/camping areas, levees or adjacent powerline pads, and gun hunting on/from/across levees, is prohibited.
- Vehicle, scouting-period and flag requirements apply; airboats are prohibited during archery, muzzleloading and general gun-walk seasons. Do not infer a general gun-vehicle hunt from access text: the 2026-2027 brochure lists none.
- Dogs may not hunt deer or wild hog. Leashed dogs may trail wounded game, subject to the brochure's restrictions.
- When weekend check stations are staffed, check deer at the southeast Holey Land station before quartering, dismembering or removing them.
- Antlered deer must have at least one antler 5 inches or longer with at least 2 points, each at least 1 inch. Youth under 16 have the statewide one-deer annual antler-point exception, still requiring a 5-inch antler. Antlerless deer and spotted fawns are not authorized by these area seasons.
- Arrows and bolts used for deer must have broadheads at least 7/8 inch wide. Any otherwise-authorized deer PCP airgun projectile must satisfy the statewide .30-caliber minimum; this does not authorize PCP equipment during bows-only or muzzleloader-only seasons.
- Muzzleloaders used for deer must be at least .30 caliber for a single bullet or at least 20 gauge when firing 2 or more balls.
- Log harvested deer before moving them and report to FWC within 24 hours of recovery, in addition to the area's check-station duties.

Conditions for the whole scope:

- Hunting over bait, taking swimming deer or spotted fawns, and hunting in posted closed areas are prohibited.
- Ordinary shooting hours are half an hour before sunrise through half an hour after sunset; turkey has separate hours.
- Night gun hunting, fully automatic firearms and centerfire semiautomatic rifles with magazines capable of more than 5 rounds are prohibited.
- Deer hunters and companions need 500 square inches of fluorescent orange above the waist, except bow-and-arrow hunting during archery season.
- Brochure license/permit exemptions include children under 16, Florida residents 65+, residents with a qualifying disabled-person certificate, and qualifying resident military personnel home on leave. They do not override quota permits marked no exemptions or required deer tags. Hunters born on/after June 1, 1975 need hunter-safety certification or the lawful supervised mentoring exception. Youth require adult supervision; mentoring license holders require a licensed supervisor aged 21+. Consult the complete brochure.
- The official brochure includes PDF BROCHURE and PDF MAP ONLY controls. Follow its current maps, access restrictions and FWC closure notices.

## Wild Hog: J. W. Corbett WMA / Wildlife Management Area (WMA), 2026-2027 expansion

Key: `hog-corbett-2-2026-2027-expanded`. new draft.

Scope: managed_area: J. W. Corbett WMA

Review coverage: 2026-07-01 through 2027-06-30.

- [FWC J. W. Corbett WMA 2026-2027 regulations and map](https://app.myfwc.com/hgm/hgmsearch/wmad?brochureTitle=J.W.+Corbett) — checked 2026-10-12. Interactive brochure checked: area dates, legal species, bag limits, methods, permits, access and exceptions; PDF map available on the same page.
- [FWC hunting licenses and permits](https://myfwc.com/license/recreational/hunting/) — checked 2026-10-12. General license, management-area and season permits; brochure exemptions and area-specific quota restrictions retained.

### Archery / Wild hog, either sex

Dates: 2026-08-29 to 2026-09-20

Bag: No bag limit or size restriction. Wild hogs may not be removed alive.

Licenses: No hunting license is required for wild hog. Management area permit required unless exempt. Archery season permit required unless exempt. No quota permit required for this listed season.

Methods: Bows only; crossbows, airbows and draw-lock bows require the brochure's Persons With Disabilities Crossbow Permit exception.

- Bruce Bowman archery still-hunt area permits bows only, with the brochure's disability crossbow/airbow/draw-lock exceptions. Closed-to-hunting trails, boardwalk, parking and adjacent areas remain closed.
- Centerfire rifles are prohibited south and east of Stumper's Grade; all rifles are prohibited in the Pratt-Whitney buffer and within a quarter mile of the railroad and Mecca Farms.
- Enter/exit at designated entrances; when staffed, report at a check station on entry and departure and check harvested wildlife. No night gun hunting for these species.
- Motorized travel is restricted to named roads and designated access routes. From July 31, 2026 an OHV Hunting Permit is required for allowed off-road hunting vehicle use; airboats, ATVs, tracked vehicles and unregistered motorcycles remain prohibited.
- The area closes August 16 at midnight through August 28 at 8 a.m., with the brochure's limited road, through-hiking and boardwalk exceptions.
- Dogs may hunt hog only during general gun season, outside the designated still-hunt areas. Tracking and behavior-correction devices are required; small-game season does not authorize hog dogs.

### Muzzleloading gun / Wild hog, either sex

Dates: 2026-10-03 to 2026-10-18

Bag: No bag limit or size restriction. Wild hogs may not be removed alive.

Licenses: No hunting license is required for wild hog. Management area permit required unless exempt. Muzzleloading gun season permit required unless exempt. No quota permit required for this listed season.

Methods: Muzzleloading guns only, except bows in the Bruce Bowman area; muzzleloading season permit still required there.

- Bruce Bowman archery still-hunt area permits bows only, with the brochure's disability crossbow/airbow/draw-lock exceptions. Closed-to-hunting trails, boardwalk, parking and adjacent areas remain closed.
- Centerfire rifles are prohibited south and east of Stumper's Grade; all rifles are prohibited in the Pratt-Whitney buffer and within a quarter mile of the railroad and Mecca Farms.
- Enter/exit at designated entrances; when staffed, report at a check station on entry and departure and check harvested wildlife. No night gun hunting for these species.
- Motorized travel is restricted to named roads and designated access routes. From July 31, 2026 an OHV Hunting Permit is required for allowed off-road hunting vehicle use; airboats, ATVs, tracked vehicles and unregistered motorcycles remain prohibited.
- The area closes August 16 at midnight through August 28 at 8 a.m., with the brochure's limited road, through-hiking and boardwalk exceptions.
- Dogs may hunt hog only during general gun season, outside the designated still-hunt areas. Tracking and behavior-correction devices are required; small-game season does not authorize hog dogs.

### General gun / Wild hog, either sex

Dates: 2026-11-07 to 2027-01-03

Bag: No bag limit or size restriction. Wild hogs may not be removed alive.

Licenses: No hunting license is required for wild hog. Management area permit required unless exempt. No quota permit required for this listed season.

Methods: Lawful shotguns, rifles, muzzleloading guns, pistols, airguns, bows and crossbows, subject to brochure restrictions.

- Bruce Bowman archery still-hunt area permits bows only, with the brochure's disability crossbow/airbow/draw-lock exceptions. Closed-to-hunting trails, boardwalk, parking and adjacent areas remain closed.
- Centerfire rifles are prohibited south and east of Stumper's Grade; all rifles are prohibited in the Pratt-Whitney buffer and within a quarter mile of the railroad and Mecca Farms.
- Enter/exit at designated entrances; when staffed, report at a check station on entry and departure and check harvested wildlife. No night gun hunting for these species.
- Motorized travel is restricted to named roads and designated access routes. From July 31, 2026 an OHV Hunting Permit is required for allowed off-road hunting vehicle use; airboats, ATVs, tracked vehicles and unregistered motorcycles remain prohibited.
- The area closes August 16 at midnight through August 28 at 8 a.m., with the brochure's limited road, through-hiking and boardwalk exceptions.
- Dogs may hunt hog only during general gun season, outside the designated still-hunt areas. Tracking and behavior-correction devices are required; small-game season does not authorize hog dogs.

### Small game / Wild hog, either sex

Dates: 2027-01-04 to 2027-02-21

Bag: No bag limit or size restriction. Wild hogs may not be removed alive.

Licenses: No hunting license is required for wild hog. Management area permit required unless exempt. No quota permit required for this listed season.

Methods: Lawful shotguns, rifles, muzzleloading guns, pistols, airguns, bows and crossbows, subject to brochure restrictions.

- Bruce Bowman archery still-hunt area permits bows only, with the brochure's disability crossbow/airbow/draw-lock exceptions. Closed-to-hunting trails, boardwalk, parking and adjacent areas remain closed.
- Centerfire rifles are prohibited south and east of Stumper's Grade; all rifles are prohibited in the Pratt-Whitney buffer and within a quarter mile of the railroad and Mecca Farms.
- Enter/exit at designated entrances; when staffed, report at a check station on entry and departure and check harvested wildlife. No night gun hunting for these species.
- Motorized travel is restricted to named roads and designated access routes. From July 31, 2026 an OHV Hunting Permit is required for allowed off-road hunting vehicle use; airboats, ATVs, tracked vehicles and unregistered motorcycles remain prohibited.
- The area closes August 16 at midnight through August 28 at 8 a.m., with the brochure's limited road, through-hiking and boardwalk exceptions.
- Dogs may hunt hog only during general gun season, outside the designated still-hunt areas. Tracking and behavior-correction devices are required; small-game season does not authorize hog dogs.

Conditions for the whole scope:

- Hunting over bait, taking swimming deer or spotted fawns, and hunting in posted closed areas are prohibited.
- Ordinary shooting hours are half an hour before sunrise through half an hour after sunset; turkey has separate hours.
- Night gun hunting, fully automatic firearms and centerfire semiautomatic rifles with magazines capable of more than 5 rounds are prohibited.
- Deer hunters and companions need 500 square inches of fluorescent orange above the waist, except bow-and-arrow hunting during archery season.
- Brochure license/permit exemptions include children under 16, Florida residents 65+, residents with a qualifying disabled-person certificate, and qualifying resident military personnel home on leave. They do not override quota permits marked no exemptions or required deer tags. Hunters born on/after June 1, 1975 need hunter-safety certification or the lawful supervised mentoring exception. Youth require adult supervision; mentoring license holders require a licensed supervisor aged 21+. Consult the complete brochure.
- The official brochure includes PDF BROCHURE and PDF MAP ONLY controls. Follow its current maps, access restrictions and FWC closure notices.

## Wild Hog: J. W. Corbett WMA / Commission-Managed Land, 2026-2027 expansion

Key: `hog-corbett-3-2026-2027-expanded`. new draft.

Scope: managed_area: J. W. Corbett WMA

Review coverage: 2026-07-01 through 2027-06-30.

- [FWC J. W. Corbett WMA 2026-2027 regulations and map](https://app.myfwc.com/hgm/hgmsearch/wmad?brochureTitle=J.W.+Corbett) — checked 2026-10-12. Interactive brochure checked: area dates, legal species, bag limits, methods, permits, access and exceptions; PDF map available on the same page.
- [FWC hunting licenses and permits](https://myfwc.com/license/recreational/hunting/) — checked 2026-10-12. General license, management-area and season permits; brochure exemptions and area-specific quota restrictions retained.

### Archery / Wild hog, either sex

Dates: 2026-08-29 to 2026-09-20

Bag: No bag limit or size restriction. Wild hogs may not be removed alive.

Licenses: No hunting license is required for wild hog. Management area permit required unless exempt. Archery season permit required unless exempt. No quota permit required for this listed season.

Methods: Bows only; crossbows, airbows and draw-lock bows require the brochure's Persons With Disabilities Crossbow Permit exception.

- Bruce Bowman archery still-hunt area permits bows only, with the brochure's disability crossbow/airbow/draw-lock exceptions. Closed-to-hunting trails, boardwalk, parking and adjacent areas remain closed.
- Centerfire rifles are prohibited south and east of Stumper's Grade; all rifles are prohibited in the Pratt-Whitney buffer and within a quarter mile of the railroad and Mecca Farms.
- Enter/exit at designated entrances; when staffed, report at a check station on entry and departure and check harvested wildlife. No night gun hunting for these species.
- Motorized travel is restricted to named roads and designated access routes. From July 31, 2026 an OHV Hunting Permit is required for allowed off-road hunting vehicle use; airboats, ATVs, tracked vehicles and unregistered motorcycles remain prohibited.
- The area closes August 16 at midnight through August 28 at 8 a.m., with the brochure's limited road, through-hiking and boardwalk exceptions.
- Dogs may hunt hog only during general gun season, outside the designated still-hunt areas. Tracking and behavior-correction devices are required; small-game season does not authorize hog dogs.

### Muzzleloading gun / Wild hog, either sex

Dates: 2026-10-03 to 2026-10-18

Bag: No bag limit or size restriction. Wild hogs may not be removed alive.

Licenses: No hunting license is required for wild hog. Management area permit required unless exempt. Muzzleloading gun season permit required unless exempt. No quota permit required for this listed season.

Methods: Muzzleloading guns only, except bows in the Bruce Bowman area; muzzleloading season permit still required there.

- Bruce Bowman archery still-hunt area permits bows only, with the brochure's disability crossbow/airbow/draw-lock exceptions. Closed-to-hunting trails, boardwalk, parking and adjacent areas remain closed.
- Centerfire rifles are prohibited south and east of Stumper's Grade; all rifles are prohibited in the Pratt-Whitney buffer and within a quarter mile of the railroad and Mecca Farms.
- Enter/exit at designated entrances; when staffed, report at a check station on entry and departure and check harvested wildlife. No night gun hunting for these species.
- Motorized travel is restricted to named roads and designated access routes. From July 31, 2026 an OHV Hunting Permit is required for allowed off-road hunting vehicle use; airboats, ATVs, tracked vehicles and unregistered motorcycles remain prohibited.
- The area closes August 16 at midnight through August 28 at 8 a.m., with the brochure's limited road, through-hiking and boardwalk exceptions.
- Dogs may hunt hog only during general gun season, outside the designated still-hunt areas. Tracking and behavior-correction devices are required; small-game season does not authorize hog dogs.

### General gun / Wild hog, either sex

Dates: 2026-11-07 to 2027-01-03

Bag: No bag limit or size restriction. Wild hogs may not be removed alive.

Licenses: No hunting license is required for wild hog. Management area permit required unless exempt. No quota permit required for this listed season.

Methods: Lawful shotguns, rifles, muzzleloading guns, pistols, airguns, bows and crossbows, subject to brochure restrictions.

- Bruce Bowman archery still-hunt area permits bows only, with the brochure's disability crossbow/airbow/draw-lock exceptions. Closed-to-hunting trails, boardwalk, parking and adjacent areas remain closed.
- Centerfire rifles are prohibited south and east of Stumper's Grade; all rifles are prohibited in the Pratt-Whitney buffer and within a quarter mile of the railroad and Mecca Farms.
- Enter/exit at designated entrances; when staffed, report at a check station on entry and departure and check harvested wildlife. No night gun hunting for these species.
- Motorized travel is restricted to named roads and designated access routes. From July 31, 2026 an OHV Hunting Permit is required for allowed off-road hunting vehicle use; airboats, ATVs, tracked vehicles and unregistered motorcycles remain prohibited.
- The area closes August 16 at midnight through August 28 at 8 a.m., with the brochure's limited road, through-hiking and boardwalk exceptions.
- Dogs may hunt hog only during general gun season, outside the designated still-hunt areas. Tracking and behavior-correction devices are required; small-game season does not authorize hog dogs.

### Small game / Wild hog, either sex

Dates: 2027-01-04 to 2027-02-21

Bag: No bag limit or size restriction. Wild hogs may not be removed alive.

Licenses: No hunting license is required for wild hog. Management area permit required unless exempt. No quota permit required for this listed season.

Methods: Lawful shotguns, rifles, muzzleloading guns, pistols, airguns, bows and crossbows, subject to brochure restrictions.

- Bruce Bowman archery still-hunt area permits bows only, with the brochure's disability crossbow/airbow/draw-lock exceptions. Closed-to-hunting trails, boardwalk, parking and adjacent areas remain closed.
- Centerfire rifles are prohibited south and east of Stumper's Grade; all rifles are prohibited in the Pratt-Whitney buffer and within a quarter mile of the railroad and Mecca Farms.
- Enter/exit at designated entrances; when staffed, report at a check station on entry and departure and check harvested wildlife. No night gun hunting for these species.
- Motorized travel is restricted to named roads and designated access routes. From July 31, 2026 an OHV Hunting Permit is required for allowed off-road hunting vehicle use; airboats, ATVs, tracked vehicles and unregistered motorcycles remain prohibited.
- The area closes August 16 at midnight through August 28 at 8 a.m., with the brochure's limited road, through-hiking and boardwalk exceptions.
- Dogs may hunt hog only during general gun season, outside the designated still-hunt areas. Tracking and behavior-correction devices are required; small-game season does not authorize hog dogs.

Conditions for the whole scope:

- Hunting over bait, taking swimming deer or spotted fawns, and hunting in posted closed areas are prohibited.
- Ordinary shooting hours are half an hour before sunrise through half an hour after sunset; turkey has separate hours.
- Night gun hunting, fully automatic firearms and centerfire semiautomatic rifles with magazines capable of more than 5 rounds are prohibited.
- Deer hunters and companions need 500 square inches of fluorescent orange above the waist, except bow-and-arrow hunting during archery season.
- Brochure license/permit exemptions include children under 16, Florida residents 65+, residents with a qualifying disabled-person certificate, and qualifying resident military personnel home on leave. They do not override quota permits marked no exemptions or required deer tags. Hunters born on/after June 1, 1975 need hunter-safety certification or the lawful supervised mentoring exception. Youth require adult supervision; mentoring license holders require a licensed supervisor aged 21+. Consult the complete brochure.
- The official brochure includes PDF BROCHURE and PDF MAP ONLY controls. Follow its current maps, access restrictions and FWC closure notices.

## Wild Hog: Dinner Island Ranch / Wildlife Management Area (WMA), 2026-2027

Key: `hog-dinner-island-2-2026-2027`. new draft.

Scope: managed_area: Dinner Island Ranch WMA

Review coverage: 2026-07-01 through 2027-06-30.

- [FWC Dinner Island Ranch 2026-2027 area brochure](https://app.myfwc.com/hgm/hgmsearch/wmad?brochureTitle=Dinner+Island+Ranch) — checked 2026-10-12. Read complete interactive brochure: season dates, antlered-only deer, quota/shared bags, turkey restrictions, hog methods, access and check-station waiver.
- [FWC Dinner Island Ranch 2026-2027 hunt calendar](https://app.myfwc.com/hsc/wmahuntcalendar/?areaName=dinner+island+ranch) — checked 2026-10-12. Corroborated every archery, muzzleloading, family, general gun, small-game and youth/spring turkey endpoint; Caracara Unit excluded.
- [FWC hunting licenses and permits](https://myfwc.com/license/recreational/hunting/) — checked 2026-10-12. Species/season permits and individual exemptions are separate from no-exemption area quota permits.
- [FWC wild hog public-land guidance](https://myfwc.com/hunting/wild-hog/) — checked 2026-10-12. A hunting license is never required for wild hog; area/season/quota permits and area methods still apply.

### Dinner Island Ranch archery / Wild hog, either sex

Dates: 2026-08-07 to 2026-08-10; 2026-08-14 to 2026-08-17; 2026-08-21 to 2026-08-24; 2026-08-28 to 2026-08-31

Bag: No bag limit or size restriction. Do not remove wild hogs alive.

Licenses: No hunting license is required for wild hog. Management area permit required unless exempt. Archery season permit required unless exempt. A quota permit for this area and hunt is required; no quota exemptions.

Methods: Bows only. Crossbows, airbows and draw-lock bows are prohibited except the brochure's Persons With Disabilities Crossbow Permit exception.

- Quota permits are nontransferable and require positive identification except for youth. Where a guest permit is allowed, one guest and the host must enter/exit together, share a street-legal vehicle and hunt with the host present. Deer and turkey limits are shared per quota permit.

### Dinner Island Ranch muzzleloading gun / Wild hog, either sex

Dates: 2026-09-11 to 2026-09-13

Bag: No bag limit or size restriction. Do not remove wild hogs alive.

Licenses: No hunting license is required for wild hog. Management area permit required unless exempt. Muzzleloading gun season permit required unless exempt. A quota permit for this area and hunt is required; no quota exemptions.

Methods: Muzzleloading guns only for deer or hog; ordinary archery equipment is prohibited during this season.

- Quota permits are nontransferable and require positive identification except for youth. Where a guest permit is allowed, one guest and the host must enter/exit together, share a street-legal vehicle and hunt with the host present. Deer and turkey limits are shared per quota permit.

### Dinner Island Ranch family hunt / Wild hog, either sex

Dates: 2026-09-19 to 2026-09-20; 2026-10-17 to 2026-10-18

Bag: No bag limit or size restriction. Do not remove wild hogs alive.

Licenses: No hunting license is required for wild hog. Management area permit required unless exempt. A quota permit for this area and hunt is required; no quota exemptions.

Methods: Lawful shotguns, rifles, muzzleloading guns, pistols, airguns, bows and crossbows, subject to the area brochure. No dogs for wild hog.

- Quota permits are nontransferable and require positive identification except for youth. Where a guest permit is allowed, one guest and the host must enter/exit together, share a street-legal vehicle and hunt with the host present. Deer and turkey limits are shared per quota permit.
- Family hunt: the quota holder must be at least 18 and directly supervise up to 2 youth ages 8-15. The adult may hunt only with at least one youth present. Guest hunting permits are not allowed for this hunt.

### Dinner Island Ranch general gun / Wild hog, either sex

Dates: 2026-09-25 to 2026-09-27; 2026-10-02 to 2026-10-04; 2026-10-09 to 2026-10-11

Bag: No bag limit or size restriction. Do not remove wild hogs alive.

Licenses: No hunting license is required for wild hog. Management area permit required unless exempt. A quota permit for this area and hunt is required; no quota exemptions.

Methods: Lawful shotguns, rifles, muzzleloading guns, pistols, airguns, bows and crossbows, subject to the area brochure. No dogs for wild hog.

- Quota permits are nontransferable and require positive identification except for youth. Where a guest permit is allowed, one guest and the host must enter/exit together, share a street-legal vehicle and hunt with the host present. Deer and turkey limits are shared per quota permit.

### Dinner Island Ranch small-game season hog / Wild hog, either sex

Dates: 2026-10-19 to 2027-02-20

Bag: No bag limit or size restriction. Do not remove wild hogs alive.

Licenses: No hunting license is required for wild hog. Management area permit required unless exempt. No quota permit required for the small-game season.

Methods: Lawful area methods, including centerfire rifles expressly permitted during this small-game season. No dogs for wild hog; no nighttime gun hunting.


### Dinner Island Ranch spring/youth turkey restriction / Wild hog prohibited

Dates: 2027-02-26 to 2027-03-01; 2027-03-06 to 2027-03-08; 2027-03-13 to 2027-03-15; 2027-04-03 to 2027-04-05

Bag: No wild hog harvest during youth or spring turkey hunts.

Licenses: A turkey quota permit does not authorize wild hog hunting.

Methods: Wild hog hunting is prohibited during these turkey hunts.

**Explicit prohibition. Search must remain closed throughout these dates.**


Conditions for the whole scope:

- Dinner Island Ranch coverage excludes the separately regulated Caracara Unit. Enter and exit at the designated entrance; posted closed areas remain closed.
- The 2026-2027 Attention Hunters notice says there is no operating check station and waives all check-station duties. Deer and turkey must still be logged before moving and officially reported within 24 hours. HuntIt does not submit the FWC report.
- Vehicles may use named and numbered roads only, except valid Alternative Mobility Permit allowances. Vehicles are prohibited from 1.5 hours after sunset until 1.5 hours before sunrise, except camping-permit holders and guests accessing their designated campsite.
- Airboats, ATVs, swamp buggies, tracked vehicles and unregistered motorcycles are prohibited, except quota hunters and their guest permit holders may use ATVs and swamp buggies on named/numbered roads during their permitted archery, muzzleloading gun, family or general gun hunt. This exception does not authorize off-road travel.
- Camping requires an FWC permit and is limited to designated campgrounds. Horses are prohibited during archery, muzzleloading gun, family, general gun and spring turkey seasons; otherwise use designated roads.
- On posted dove fields, hunting during dove season is limited to Saturdays; otherwise only hunting allowed by the applicable area season is authorized. Check the brochure map and current closures before selecting a hunting site.
- No hunting over bait, night gun hunting, fully automatic firearms or centerfire semiautomatic rifles with magazines holding more than 5 rounds. The brochure's ammunition, equipment and closed-area restrictions apply.
- Ordinary shooting hours are half an hour before sunrise through half an hour after sunset. Turkey shooting ends at sunset.
- Dogs may not hunt deer, wild hog or furbearers; leashed dogs may trail wounded game under the brochure's conditions. No dogs may pursue non-native reptiles.
- License/season-permit exemptions do not waive a quota permit marked no exemptions. Check hunter-safety requirements and individual exemptions in the full brochure.
- Nonresident hunters taking native game need the applicable annual hunting license unless exempt. A hunting license is not required when hunting wild hog or removing python within the stated exception.

## Wild Hog: Dinner Island Ranch / Commission-Managed Land, 2026-2027

Key: `hog-dinner-island-3-2026-2027`. new draft.

Scope: managed_area: Dinner Island Ranch WMA

Review coverage: 2026-07-01 through 2027-06-30.

- [FWC Dinner Island Ranch 2026-2027 area brochure](https://app.myfwc.com/hgm/hgmsearch/wmad?brochureTitle=Dinner+Island+Ranch) — checked 2026-10-12. Read complete interactive brochure: season dates, antlered-only deer, quota/shared bags, turkey restrictions, hog methods, access and check-station waiver.
- [FWC Dinner Island Ranch 2026-2027 hunt calendar](https://app.myfwc.com/hsc/wmahuntcalendar/?areaName=dinner+island+ranch) — checked 2026-10-12. Corroborated every archery, muzzleloading, family, general gun, small-game and youth/spring turkey endpoint; Caracara Unit excluded.
- [FWC hunting licenses and permits](https://myfwc.com/license/recreational/hunting/) — checked 2026-10-12. Species/season permits and individual exemptions are separate from no-exemption area quota permits.
- [FWC wild hog public-land guidance](https://myfwc.com/hunting/wild-hog/) — checked 2026-10-12. A hunting license is never required for wild hog; area/season/quota permits and area methods still apply.

### Dinner Island Ranch archery / Wild hog, either sex

Dates: 2026-08-07 to 2026-08-10; 2026-08-14 to 2026-08-17; 2026-08-21 to 2026-08-24; 2026-08-28 to 2026-08-31

Bag: No bag limit or size restriction. Do not remove wild hogs alive.

Licenses: No hunting license is required for wild hog. Management area permit required unless exempt. Archery season permit required unless exempt. A quota permit for this area and hunt is required; no quota exemptions.

Methods: Bows only. Crossbows, airbows and draw-lock bows are prohibited except the brochure's Persons With Disabilities Crossbow Permit exception.

- Quota permits are nontransferable and require positive identification except for youth. Where a guest permit is allowed, one guest and the host must enter/exit together, share a street-legal vehicle and hunt with the host present. Deer and turkey limits are shared per quota permit.

### Dinner Island Ranch muzzleloading gun / Wild hog, either sex

Dates: 2026-09-11 to 2026-09-13

Bag: No bag limit or size restriction. Do not remove wild hogs alive.

Licenses: No hunting license is required for wild hog. Management area permit required unless exempt. Muzzleloading gun season permit required unless exempt. A quota permit for this area and hunt is required; no quota exemptions.

Methods: Muzzleloading guns only for deer or hog; ordinary archery equipment is prohibited during this season.

- Quota permits are nontransferable and require positive identification except for youth. Where a guest permit is allowed, one guest and the host must enter/exit together, share a street-legal vehicle and hunt with the host present. Deer and turkey limits are shared per quota permit.

### Dinner Island Ranch family hunt / Wild hog, either sex

Dates: 2026-09-19 to 2026-09-20; 2026-10-17 to 2026-10-18

Bag: No bag limit or size restriction. Do not remove wild hogs alive.

Licenses: No hunting license is required for wild hog. Management area permit required unless exempt. A quota permit for this area and hunt is required; no quota exemptions.

Methods: Lawful shotguns, rifles, muzzleloading guns, pistols, airguns, bows and crossbows, subject to the area brochure. No dogs for wild hog.

- Quota permits are nontransferable and require positive identification except for youth. Where a guest permit is allowed, one guest and the host must enter/exit together, share a street-legal vehicle and hunt with the host present. Deer and turkey limits are shared per quota permit.
- Family hunt: the quota holder must be at least 18 and directly supervise up to 2 youth ages 8-15. The adult may hunt only with at least one youth present. Guest hunting permits are not allowed for this hunt.

### Dinner Island Ranch general gun / Wild hog, either sex

Dates: 2026-09-25 to 2026-09-27; 2026-10-02 to 2026-10-04; 2026-10-09 to 2026-10-11

Bag: No bag limit or size restriction. Do not remove wild hogs alive.

Licenses: No hunting license is required for wild hog. Management area permit required unless exempt. A quota permit for this area and hunt is required; no quota exemptions.

Methods: Lawful shotguns, rifles, muzzleloading guns, pistols, airguns, bows and crossbows, subject to the area brochure. No dogs for wild hog.

- Quota permits are nontransferable and require positive identification except for youth. Where a guest permit is allowed, one guest and the host must enter/exit together, share a street-legal vehicle and hunt with the host present. Deer and turkey limits are shared per quota permit.

### Dinner Island Ranch small-game season hog / Wild hog, either sex

Dates: 2026-10-19 to 2027-02-20

Bag: No bag limit or size restriction. Do not remove wild hogs alive.

Licenses: No hunting license is required for wild hog. Management area permit required unless exempt. No quota permit required for the small-game season.

Methods: Lawful area methods, including centerfire rifles expressly permitted during this small-game season. No dogs for wild hog; no nighttime gun hunting.


### Dinner Island Ranch spring/youth turkey restriction / Wild hog prohibited

Dates: 2027-02-26 to 2027-03-01; 2027-03-06 to 2027-03-08; 2027-03-13 to 2027-03-15; 2027-04-03 to 2027-04-05

Bag: No wild hog harvest during youth or spring turkey hunts.

Licenses: A turkey quota permit does not authorize wild hog hunting.

Methods: Wild hog hunting is prohibited during these turkey hunts.

**Explicit prohibition. Search must remain closed throughout these dates.**


Conditions for the whole scope:

- Dinner Island Ranch coverage excludes the separately regulated Caracara Unit. Enter and exit at the designated entrance; posted closed areas remain closed.
- The 2026-2027 Attention Hunters notice says there is no operating check station and waives all check-station duties. Deer and turkey must still be logged before moving and officially reported within 24 hours. HuntIt does not submit the FWC report.
- Vehicles may use named and numbered roads only, except valid Alternative Mobility Permit allowances. Vehicles are prohibited from 1.5 hours after sunset until 1.5 hours before sunrise, except camping-permit holders and guests accessing their designated campsite.
- Airboats, ATVs, swamp buggies, tracked vehicles and unregistered motorcycles are prohibited, except quota hunters and their guest permit holders may use ATVs and swamp buggies on named/numbered roads during their permitted archery, muzzleloading gun, family or general gun hunt. This exception does not authorize off-road travel.
- Camping requires an FWC permit and is limited to designated campgrounds. Horses are prohibited during archery, muzzleloading gun, family, general gun and spring turkey seasons; otherwise use designated roads.
- On posted dove fields, hunting during dove season is limited to Saturdays; otherwise only hunting allowed by the applicable area season is authorized. Check the brochure map and current closures before selecting a hunting site.
- No hunting over bait, night gun hunting, fully automatic firearms or centerfire semiautomatic rifles with magazines holding more than 5 rounds. The brochure's ammunition, equipment and closed-area restrictions apply.
- Ordinary shooting hours are half an hour before sunrise through half an hour after sunset. Turkey shooting ends at sunset.
- Dogs may not hunt deer, wild hog or furbearers; leashed dogs may trail wounded game under the brochure's conditions. No dogs may pursue non-native reptiles.
- License/season-permit exemptions do not waive a quota permit marked no exemptions. Check hunter-safety requirements and individual exemptions in the full brochure.
- Nonresident hunters taking native game need the applicable annual hunting license unless exempt. A hunting license is not required when hunting wild hog or removing python within the stated exception.

## Wild Hog: Holey Land WMA / Wildlife Management Area (WMA), 2026-2027 expansion

Key: `hog-holey-land-2-2026-2027-expanded`. new draft.

Scope: managed_area: Holey Land WMA

Review coverage: 2026-07-01 through 2027-06-30.

- [FWC Holey Land WMA 2026-2027 regulations and map](https://app.myfwc.com/hgm/hgmsearch/wmad?brochureTitle=Holey+Land) — checked 2026-10-12. Interactive brochure checked: area dates, legal species, bag limits, methods, permits, access and exceptions; PDF map available on the same page.
- [FWC hunting licenses and permits](https://myfwc.com/license/recreational/hunting/) — checked 2026-10-12. General license, management-area and season permits; brochure exemptions and area-specific quota restrictions retained.

### Archery / Wild hog, either sex

Dates: 2026-08-08 to 2026-08-30

Bag: No bag limit or size restriction. Wild hogs may not be removed alive.

Licenses: No hunting license is required for wild hog. Management area permit required unless exempt. Archery season permit required unless exempt. No quota permit required for this listed season.

Methods: Bows only; crossbows, airbows and draw-lock bows require the brochure's Persons With Disabilities Crossbow Permit exception.

- Entry/exit is limited to the L-5 and Miami Canal levees. Hunting on roads, ramps, parking/camping areas, levees or adjacent powerline pads, and gun hunting on/from/across levees, is prohibited.
- Motorized use, scouting periods, flags and access routes are restricted. During general gun-vehicle season walk-hunting is closed and only vehicles authorized by its permits may operate; consult the map and permit conditions.
- Dogs may hunt deer/hog only during general gun-vehicle season; deer-dog hunting needs a valid WMA deer-dog permit, and dogs pursuing deer/hog need remote tracking and correction devices.
- When weekend check stations are staffed, check deer at the L-5 levee station before quartering, dismembering or removing them. General gun-vehicle deer must be immediately tagged with the FWC antlered deer tag.

### Muzzleloading gun / Wild hog, either sex

Dates: 2026-09-05 to 2026-09-13

Bag: No bag limit or size restriction. Wild hogs may not be removed alive.

Licenses: No hunting license is required for wild hog. Management area permit required unless exempt. Muzzleloading gun season permit required unless exempt. No quota permit required for this listed season.

Methods: Muzzleloading guns only for deer or hog; ordinary archery equipment is prohibited.

- Entry/exit is limited to the L-5 and Miami Canal levees. Hunting on roads, ramps, parking/camping areas, levees or adjacent powerline pads, and gun hunting on/from/across levees, is prohibited.
- Motorized use, scouting periods, flags and access routes are restricted. During general gun-vehicle season walk-hunting is closed and only vehicles authorized by its permits may operate; consult the map and permit conditions.
- Dogs may hunt deer/hog only during general gun-vehicle season; deer-dog hunting needs a valid WMA deer-dog permit, and dogs pursuing deer/hog need remote tracking and correction devices.
- When weekend check stations are staffed, check deer at the L-5 levee station before quartering, dismembering or removing them. General gun-vehicle deer must be immediately tagged with the FWC antlered deer tag.

### General gun-walk / Wild hog, either sex

Dates: 2026-10-03 to 2026-10-18

Bag: No bag limit or size restriction. Wild hogs may not be removed alive.

Licenses: No hunting license is required for wild hog. Management area permit required unless exempt. No quota permit required for this listed season.

Methods: Lawful shotguns, rifles, muzzleloading guns, pistols, airguns, bows and crossbows, subject to brochure restrictions.

- Entry/exit is limited to the L-5 and Miami Canal levees. Hunting on roads, ramps, parking/camping areas, levees or adjacent powerline pads, and gun hunting on/from/across levees, is prohibited.
- Motorized use, scouting periods, flags and access routes are restricted. During general gun-vehicle season walk-hunting is closed and only vehicles authorized by its permits may operate; consult the map and permit conditions.
- Dogs may hunt deer/hog only during general gun-vehicle season; deer-dog hunting needs a valid WMA deer-dog permit, and dogs pursuing deer/hog need remote tracking and correction devices.
- When weekend check stations are staffed, check deer at the L-5 levee station before quartering, dismembering or removing them. General gun-vehicle deer must be immediately tagged with the FWC antlered deer tag.

### General gun-vehicle / Wild hog, either sex

Dates: 2026-11-21 to 2026-12-06

Bag: No bag limit or size restriction. Wild hogs may not be removed alive.

Licenses: No hunting license is required for wild hog. Management area permit required unless exempt. General gun-vehicle quota/track permit and its antlered deer tag are required by this hunt; no quota exemptions and no guest hunters. Deer require the supplied tag; a WMA deer-dog permit is required if hunting deer with dogs.

Methods: Lawful shotguns, rifles, muzzleloading guns, pistols, airguns, bows and crossbows, subject to brochure restrictions.

- Entry/exit is limited to the L-5 and Miami Canal levees. Hunting on roads, ramps, parking/camping areas, levees or adjacent powerline pads, and gun hunting on/from/across levees, is prohibited.
- Motorized use, scouting periods, flags and access routes are restricted. During general gun-vehicle season walk-hunting is closed and only vehicles authorized by its permits may operate; consult the map and permit conditions.
- Dogs may hunt deer/hog only during general gun-vehicle season; deer-dog hunting needs a valid WMA deer-dog permit, and dogs pursuing deer/hog need remote tracking and correction devices.
- When weekend check stations are staffed, check deer at the L-5 levee station before quartering, dismembering or removing them. General gun-vehicle deer must be immediately tagged with the FWC antlered deer tag.

Conditions for the whole scope:

- Hunting over bait, taking swimming deer or spotted fawns, and hunting in posted closed areas are prohibited.
- Ordinary shooting hours are half an hour before sunrise through half an hour after sunset; turkey has separate hours.
- Night gun hunting, fully automatic firearms and centerfire semiautomatic rifles with magazines capable of more than 5 rounds are prohibited.
- Deer hunters and companions need 500 square inches of fluorescent orange above the waist, except bow-and-arrow hunting during archery season.
- Brochure license/permit exemptions include children under 16, Florida residents 65+, residents with a qualifying disabled-person certificate, and qualifying resident military personnel home on leave. They do not override quota permits marked no exemptions or required deer tags. Hunters born on/after June 1, 1975 need hunter-safety certification or the lawful supervised mentoring exception. Youth require adult supervision; mentoring license holders require a licensed supervisor aged 21+. Consult the complete brochure.
- The official brochure includes PDF BROCHURE and PDF MAP ONLY controls. Follow its current maps, access restrictions and FWC closure notices.
- The small-game legal-species list does not include wild hog; do not infer a hog season from the small-game dates.

## Wild Hog: Holey Land WMA / Commission-Managed Land, 2026-2027 expansion

Key: `hog-holey-land-3-2026-2027-expanded`. new draft.

Scope: managed_area: Holey Land WMA

Review coverage: 2026-07-01 through 2027-06-30.

- [FWC Holey Land WMA 2026-2027 regulations and map](https://app.myfwc.com/hgm/hgmsearch/wmad?brochureTitle=Holey+Land) — checked 2026-10-12. Interactive brochure checked: area dates, legal species, bag limits, methods, permits, access and exceptions; PDF map available on the same page.
- [FWC hunting licenses and permits](https://myfwc.com/license/recreational/hunting/) — checked 2026-10-12. General license, management-area and season permits; brochure exemptions and area-specific quota restrictions retained.

### Archery / Wild hog, either sex

Dates: 2026-08-08 to 2026-08-30

Bag: No bag limit or size restriction. Wild hogs may not be removed alive.

Licenses: No hunting license is required for wild hog. Management area permit required unless exempt. Archery season permit required unless exempt. No quota permit required for this listed season.

Methods: Bows only; crossbows, airbows and draw-lock bows require the brochure's Persons With Disabilities Crossbow Permit exception.

- Entry/exit is limited to the L-5 and Miami Canal levees. Hunting on roads, ramps, parking/camping areas, levees or adjacent powerline pads, and gun hunting on/from/across levees, is prohibited.
- Motorized use, scouting periods, flags and access routes are restricted. During general gun-vehicle season walk-hunting is closed and only vehicles authorized by its permits may operate; consult the map and permit conditions.
- Dogs may hunt deer/hog only during general gun-vehicle season; deer-dog hunting needs a valid WMA deer-dog permit, and dogs pursuing deer/hog need remote tracking and correction devices.
- When weekend check stations are staffed, check deer at the L-5 levee station before quartering, dismembering or removing them. General gun-vehicle deer must be immediately tagged with the FWC antlered deer tag.

### Muzzleloading gun / Wild hog, either sex

Dates: 2026-09-05 to 2026-09-13

Bag: No bag limit or size restriction. Wild hogs may not be removed alive.

Licenses: No hunting license is required for wild hog. Management area permit required unless exempt. Muzzleloading gun season permit required unless exempt. No quota permit required for this listed season.

Methods: Muzzleloading guns only for deer or hog; ordinary archery equipment is prohibited.

- Entry/exit is limited to the L-5 and Miami Canal levees. Hunting on roads, ramps, parking/camping areas, levees or adjacent powerline pads, and gun hunting on/from/across levees, is prohibited.
- Motorized use, scouting periods, flags and access routes are restricted. During general gun-vehicle season walk-hunting is closed and only vehicles authorized by its permits may operate; consult the map and permit conditions.
- Dogs may hunt deer/hog only during general gun-vehicle season; deer-dog hunting needs a valid WMA deer-dog permit, and dogs pursuing deer/hog need remote tracking and correction devices.
- When weekend check stations are staffed, check deer at the L-5 levee station before quartering, dismembering or removing them. General gun-vehicle deer must be immediately tagged with the FWC antlered deer tag.

### General gun-walk / Wild hog, either sex

Dates: 2026-10-03 to 2026-10-18

Bag: No bag limit or size restriction. Wild hogs may not be removed alive.

Licenses: No hunting license is required for wild hog. Management area permit required unless exempt. No quota permit required for this listed season.

Methods: Lawful shotguns, rifles, muzzleloading guns, pistols, airguns, bows and crossbows, subject to brochure restrictions.

- Entry/exit is limited to the L-5 and Miami Canal levees. Hunting on roads, ramps, parking/camping areas, levees or adjacent powerline pads, and gun hunting on/from/across levees, is prohibited.
- Motorized use, scouting periods, flags and access routes are restricted. During general gun-vehicle season walk-hunting is closed and only vehicles authorized by its permits may operate; consult the map and permit conditions.
- Dogs may hunt deer/hog only during general gun-vehicle season; deer-dog hunting needs a valid WMA deer-dog permit, and dogs pursuing deer/hog need remote tracking and correction devices.
- When weekend check stations are staffed, check deer at the L-5 levee station before quartering, dismembering or removing them. General gun-vehicle deer must be immediately tagged with the FWC antlered deer tag.

### General gun-vehicle / Wild hog, either sex

Dates: 2026-11-21 to 2026-12-06

Bag: No bag limit or size restriction. Wild hogs may not be removed alive.

Licenses: No hunting license is required for wild hog. Management area permit required unless exempt. General gun-vehicle quota/track permit and its antlered deer tag are required by this hunt; no quota exemptions and no guest hunters. Deer require the supplied tag; a WMA deer-dog permit is required if hunting deer with dogs.

Methods: Lawful shotguns, rifles, muzzleloading guns, pistols, airguns, bows and crossbows, subject to brochure restrictions.

- Entry/exit is limited to the L-5 and Miami Canal levees. Hunting on roads, ramps, parking/camping areas, levees or adjacent powerline pads, and gun hunting on/from/across levees, is prohibited.
- Motorized use, scouting periods, flags and access routes are restricted. During general gun-vehicle season walk-hunting is closed and only vehicles authorized by its permits may operate; consult the map and permit conditions.
- Dogs may hunt deer/hog only during general gun-vehicle season; deer-dog hunting needs a valid WMA deer-dog permit, and dogs pursuing deer/hog need remote tracking and correction devices.
- When weekend check stations are staffed, check deer at the L-5 levee station before quartering, dismembering or removing them. General gun-vehicle deer must be immediately tagged with the FWC antlered deer tag.

Conditions for the whole scope:

- Hunting over bait, taking swimming deer or spotted fawns, and hunting in posted closed areas are prohibited.
- Ordinary shooting hours are half an hour before sunrise through half an hour after sunset; turkey has separate hours.
- Night gun hunting, fully automatic firearms and centerfire semiautomatic rifles with magazines capable of more than 5 rounds are prohibited.
- Deer hunters and companions need 500 square inches of fluorescent orange above the waist, except bow-and-arrow hunting during archery season.
- Brochure license/permit exemptions include children under 16, Florida residents 65+, residents with a qualifying disabled-person certificate, and qualifying resident military personnel home on leave. They do not override quota permits marked no exemptions or required deer tags. Hunters born on/after June 1, 1975 need hunter-safety certification or the lawful supervised mentoring exception. Youth require adult supervision; mentoring license holders require a licensed supervisor aged 21+. Consult the complete brochure.
- The official brochure includes PDF BROCHURE and PDF MAP ONLY controls. Follow its current maps, access restrictions and FWC closure notices.
- The small-game legal-species list does not include wild hog; do not infer a hog season from the small-game dates.

## Wild hog: private land, 2026

Key: `hog-private-2026`. proposed revision of existing approved draft.

Scope: Private-land statewide exception

Review coverage: 2026-01-01 through 2026-12-31.

- [FWC Wild Hog](https://myfwc.com/hunting/wild-hog/) — checked 2026-10-12. Private-property year-round exception, permission, license/night permit, bag and methods checked.
- [FWC current area notices](https://myfwc.com/recreation/notices/) — checked 2026-10-12. Current closure directory checked; notices can change after this data check.
- [FWC general hog exception](https://myfwc.com/hunting/regulations/general-information/) — checked 2026-10-12. Checked private-land day/night exception, no possession limit and landowner permission.

### Year-round private-land hog / Either sex

Dates: 2026-01-01 to 2026-12-31

Bag: No size or bag limit.

Licenses: No hunting license or nighttime gun-and-light permit required with landowner permission.

Methods: Lawful rifle, shotgun, bow, crossbow, pistol or air gun; lawful trapping and dogs subject to restrictions.

- With dogs, carry written landowner permission; identification collars and remote tracking/correction rules apply.
- Live transport or holding wild hogs requires the applicable FDACS authorization.

Conditions for the whole scope:

- Check the linked FWC area notices for temporary closures; this local dataset does not poll live closures.
- The private-land hog exception permits lawful day or night hunting with permission and has no possession limit. It does not apply on WMAs.

## Wild Hog: Rotenberger WMA / Wildlife Management Area (WMA), 2026-2027 expansion

Key: `hog-rotenberger-2-2026-2027-expanded`. new draft.

Scope: managed_area: Rotenberger WMA

Review coverage: 2026-07-01 through 2027-06-30.

- [FWC Rotenberger WMA 2026-2027 regulations and map](https://app.myfwc.com/hgm/hgmsearch/wmad?brochureTitle=Rotenberger) — checked 2026-10-12. Interactive brochure checked: area dates, legal species, bag limits, methods, permits, access and exceptions; PDF map available on the same page.
- [FWC hunting licenses and permits](https://myfwc.com/license/recreational/hunting/) — checked 2026-10-12. General license, management-area and season permits; brochure exemptions and area-specific quota restrictions retained.

### Archery / Wild hog, either sex

Dates: 2026-08-08 to 2026-08-30

Bag: No bag limit or size restriction. Wild hogs may not be removed alive.

Licenses: No hunting license is required for wild hog. Management area permit required unless exempt. Archery season permit required unless exempt. No quota permit required for this listed season.

Methods: Bows only; crossbows, airbows and draw-lock bows require the brochure's Persons With Disabilities Crossbow Permit exception.

- Entry/exit is limited to the L-4, Powerline, Miami Canal and Manley Ditch levees. Hunting on roads, ramps, parking/camping areas, levees or adjacent powerline pads, and gun hunting on/from/across levees, is prohibited.
- Vehicle, scouting-period and flag requirements apply; airboats are prohibited during archery, muzzleloading and general gun-walk seasons. Do not infer a general gun-vehicle hunt from access text: the 2026-2027 brochure lists none.
- Dogs may not hunt deer or wild hog. Leashed dogs may trail wounded game, subject to the brochure's restrictions.
- When weekend check stations are staffed, check deer at the southeast Holey Land station before quartering, dismembering or removing them.

### Muzzleloading gun / Wild hog, either sex

Dates: 2026-09-05 to 2026-09-13

Bag: No bag limit or size restriction. Wild hogs may not be removed alive.

Licenses: No hunting license is required for wild hog. Management area permit required unless exempt. Muzzleloading gun season permit required unless exempt. No quota permit required for this listed season.

Methods: Muzzleloading guns only for deer or hog; ordinary archery equipment is prohibited.

- Entry/exit is limited to the L-4, Powerline, Miami Canal and Manley Ditch levees. Hunting on roads, ramps, parking/camping areas, levees or adjacent powerline pads, and gun hunting on/from/across levees, is prohibited.
- Vehicle, scouting-period and flag requirements apply; airboats are prohibited during archery, muzzleloading and general gun-walk seasons. Do not infer a general gun-vehicle hunt from access text: the 2026-2027 brochure lists none.
- Dogs may not hunt deer or wild hog. Leashed dogs may trail wounded game, subject to the brochure's restrictions.
- When weekend check stations are staffed, check deer at the southeast Holey Land station before quartering, dismembering or removing them.

### General gun-walk / Wild hog, either sex

Dates: 2026-10-03 to 2026-10-18

Bag: No bag limit or size restriction. Wild hogs may not be removed alive.

Licenses: No hunting license is required for wild hog. Management area permit required unless exempt. No quota permit required for this listed season.

Methods: Lawful shotguns, rifles, muzzleloading guns, pistols, airguns, bows and crossbows, subject to brochure restrictions.

- Entry/exit is limited to the L-4, Powerline, Miami Canal and Manley Ditch levees. Hunting on roads, ramps, parking/camping areas, levees or adjacent powerline pads, and gun hunting on/from/across levees, is prohibited.
- Vehicle, scouting-period and flag requirements apply; airboats are prohibited during archery, muzzleloading and general gun-walk seasons. Do not infer a general gun-vehicle hunt from access text: the 2026-2027 brochure lists none.
- Dogs may not hunt deer or wild hog. Leashed dogs may trail wounded game, subject to the brochure's restrictions.
- When weekend check stations are staffed, check deer at the southeast Holey Land station before quartering, dismembering or removing them.

Conditions for the whole scope:

- Hunting over bait, taking swimming deer or spotted fawns, and hunting in posted closed areas are prohibited.
- Ordinary shooting hours are half an hour before sunrise through half an hour after sunset; turkey has separate hours.
- Night gun hunting, fully automatic firearms and centerfire semiautomatic rifles with magazines capable of more than 5 rounds are prohibited.
- Deer hunters and companions need 500 square inches of fluorescent orange above the waist, except bow-and-arrow hunting during archery season.
- Brochure license/permit exemptions include children under 16, Florida residents 65+, residents with a qualifying disabled-person certificate, and qualifying resident military personnel home on leave. They do not override quota permits marked no exemptions or required deer tags. Hunters born on/after June 1, 1975 need hunter-safety certification or the lawful supervised mentoring exception. Youth require adult supervision; mentoring license holders require a licensed supervisor aged 21+. Consult the complete brochure.
- The official brochure includes PDF BROCHURE and PDF MAP ONLY controls. Follow its current maps, access restrictions and FWC closure notices.
- The small-game legal-species list does not include wild hog; do not infer a hog season from the small-game dates.

## Wild Hog: Rotenberger WMA / Commission-Managed Land, 2026-2027 expansion

Key: `hog-rotenberger-3-2026-2027-expanded`. new draft.

Scope: managed_area: Rotenberger WMA

Review coverage: 2026-07-01 through 2027-06-30.

- [FWC Rotenberger WMA 2026-2027 regulations and map](https://app.myfwc.com/hgm/hgmsearch/wmad?brochureTitle=Rotenberger) — checked 2026-10-12. Interactive brochure checked: area dates, legal species, bag limits, methods, permits, access and exceptions; PDF map available on the same page.
- [FWC hunting licenses and permits](https://myfwc.com/license/recreational/hunting/) — checked 2026-10-12. General license, management-area and season permits; brochure exemptions and area-specific quota restrictions retained.

### Archery / Wild hog, either sex

Dates: 2026-08-08 to 2026-08-30

Bag: No bag limit or size restriction. Wild hogs may not be removed alive.

Licenses: No hunting license is required for wild hog. Management area permit required unless exempt. Archery season permit required unless exempt. No quota permit required for this listed season.

Methods: Bows only; crossbows, airbows and draw-lock bows require the brochure's Persons With Disabilities Crossbow Permit exception.

- Entry/exit is limited to the L-4, Powerline, Miami Canal and Manley Ditch levees. Hunting on roads, ramps, parking/camping areas, levees or adjacent powerline pads, and gun hunting on/from/across levees, is prohibited.
- Vehicle, scouting-period and flag requirements apply; airboats are prohibited during archery, muzzleloading and general gun-walk seasons. Do not infer a general gun-vehicle hunt from access text: the 2026-2027 brochure lists none.
- Dogs may not hunt deer or wild hog. Leashed dogs may trail wounded game, subject to the brochure's restrictions.
- When weekend check stations are staffed, check deer at the southeast Holey Land station before quartering, dismembering or removing them.

### Muzzleloading gun / Wild hog, either sex

Dates: 2026-09-05 to 2026-09-13

Bag: No bag limit or size restriction. Wild hogs may not be removed alive.

Licenses: No hunting license is required for wild hog. Management area permit required unless exempt. Muzzleloading gun season permit required unless exempt. No quota permit required for this listed season.

Methods: Muzzleloading guns only for deer or hog; ordinary archery equipment is prohibited.

- Entry/exit is limited to the L-4, Powerline, Miami Canal and Manley Ditch levees. Hunting on roads, ramps, parking/camping areas, levees or adjacent powerline pads, and gun hunting on/from/across levees, is prohibited.
- Vehicle, scouting-period and flag requirements apply; airboats are prohibited during archery, muzzleloading and general gun-walk seasons. Do not infer a general gun-vehicle hunt from access text: the 2026-2027 brochure lists none.
- Dogs may not hunt deer or wild hog. Leashed dogs may trail wounded game, subject to the brochure's restrictions.
- When weekend check stations are staffed, check deer at the southeast Holey Land station before quartering, dismembering or removing them.

### General gun-walk / Wild hog, either sex

Dates: 2026-10-03 to 2026-10-18

Bag: No bag limit or size restriction. Wild hogs may not be removed alive.

Licenses: No hunting license is required for wild hog. Management area permit required unless exempt. No quota permit required for this listed season.

Methods: Lawful shotguns, rifles, muzzleloading guns, pistols, airguns, bows and crossbows, subject to brochure restrictions.

- Entry/exit is limited to the L-4, Powerline, Miami Canal and Manley Ditch levees. Hunting on roads, ramps, parking/camping areas, levees or adjacent powerline pads, and gun hunting on/from/across levees, is prohibited.
- Vehicle, scouting-period and flag requirements apply; airboats are prohibited during archery, muzzleloading and general gun-walk seasons. Do not infer a general gun-vehicle hunt from access text: the 2026-2027 brochure lists none.
- Dogs may not hunt deer or wild hog. Leashed dogs may trail wounded game, subject to the brochure's restrictions.
- When weekend check stations are staffed, check deer at the southeast Holey Land station before quartering, dismembering or removing them.

Conditions for the whole scope:

- Hunting over bait, taking swimming deer or spotted fawns, and hunting in posted closed areas are prohibited.
- Ordinary shooting hours are half an hour before sunrise through half an hour after sunset; turkey has separate hours.
- Night gun hunting, fully automatic firearms and centerfire semiautomatic rifles with magazines capable of more than 5 rounds are prohibited.
- Deer hunters and companions need 500 square inches of fluorescent orange above the waist, except bow-and-arrow hunting during archery season.
- Brochure license/permit exemptions include children under 16, Florida residents 65+, residents with a qualifying disabled-person certificate, and qualifying resident military personnel home on leave. They do not override quota permits marked no exemptions or required deer tags. Hunters born on/after June 1, 1975 need hunter-safety certification or the lawful supervised mentoring exception. Youth require adult supervision; mentoring license holders require a licensed supervisor aged 21+. Consult the complete brochure.
- The official brochure includes PDF BROCHURE and PDF MAP ONLY controls. Follow its current maps, access restrictions and FWC closure notices.
- The small-game legal-species list does not include wild hog; do not infer a hog season from the small-game dates.

## Burmese Python: J. W. Corbett WMA / Wildlife Management Area (WMA), 2026-2027 expansion

Key: `python-corbett-2-2026-2027-expanded`. new draft.

Scope: managed_area: J. W. Corbett WMA

Review coverage: 2026-07-01 through 2027-06-30.

- [FWC J. W. Corbett WMA 2026-2027 regulations and map](https://app.myfwc.com/hgm/hgmsearch/wmad?brochureTitle=J.W.+Corbett) — checked 2026-10-12. Interactive brochure checked: area dates, legal species, bag limits, methods, permits, access and exceptions; PDF map available on the same page.
- [FWC hunting licenses and permits](https://myfwc.com/license/recreational/hunting/) — checked 2026-10-12. General license, management-area and season permits; brochure exemptions and area-specific quota restrictions retained.
- [FWC Executive Order 23-16](https://myfwc.com/media/31857/eo-23-16.pdf) — checked 2026-10-12. Page 2: traps and modified/free-bolt captive-bolt stunners prohibited; firearms need specific area authorization.
- [FWC python removal](https://myfwc.com/wildlifehabitats/nonnatives/python/removing/) — checked 2026-10-12. Area-specific removal is subject to the brochure and current FWC orders.
- [FWC humane killing methods](https://myfwc.com/wildlifehabitats/nonnatives/python/humane-killing-methods/) — checked 2026-10-12. Humane onsite killing and required second step; no public live transport.

### Year-round python removal / Burmese python

Dates: 2026-07-01 to 2027-06-30

Bag: No bag limit.

Licenses: No license or removal permit required for non-native reptiles; vehicle/access permits still apply where required.

Methods: Non-firearm removal is allowed year-round subject to access and humane-killing rules. Firearms may be used only during open brochure hunting seasons and only as allowed by that season. Follow the linked FWC humane-killing guidance.

- Bruce Bowman archery still-hunt area permits bows only, with the brochure's disability crossbow/airbow/draw-lock exceptions. Closed-to-hunting trails, boardwalk, parking and adjacent areas remain closed.
- Centerfire rifles are prohibited south and east of Stumper's Grade; all rifles are prohibited in the Pratt-Whitney buffer and within a quarter mile of the railroad and Mecca Farms.
- Enter/exit at designated entrances; when staffed, report at a check station on entry and departure and check harvested wildlife. No night gun hunting for these species.
- Motorized travel is restricted to named roads and designated access routes. From July 31, 2026 an OHV Hunting Permit is required for allowed off-road hunting vehicle use; airboats, ATVs, tracked vehicles and unregistered motorcycles remain prohibited.
- The area closes August 16 at midnight through August 28 at 8 a.m., with the brochure's limited road, through-hiking and boardwalk exceptions.
- EO23-16 prohibits traps and modified/free-bolt captive-bolt stunners; all other area access and equipment restrictions still apply.
- No live python may be removed from the area. Florida anti-cruelty law and FWC humane-killing guidance apply; the required second step prevents recovery after immediate loss of consciousness.
- A year-round python removal opportunity does not open deer/hog/turkey seasons or authorize firearm discharge outside lawful hunting seasons. Follow each season's allowed firearm methods and property closures.
- Python shooting hours are half an hour before sunrise until half an hour after sunset. Report sightings/take through FWC's non-native wildlife reporting service.
- In Bruce Bowman only hand tools and bows may take reptiles, except qualifying disability crossbow/airbow/draw-lock permits. Dogs may only search for reptiles during general gun season.
- Spring turkey rules prohibit hunting other animals; confirm the interaction with the separate reptile provisions with FWC before attempting firearm reptile removal during spring turkey dates.

Conditions for the whole scope:

- Hunting over bait, taking swimming deer or spotted fawns, and hunting in posted closed areas are prohibited.
- Ordinary shooting hours are half an hour before sunrise through half an hour after sunset; turkey has separate hours.
- Night gun hunting, fully automatic firearms and centerfire semiautomatic rifles with magazines capable of more than 5 rounds are prohibited.
- Deer hunters and companions need 500 square inches of fluorescent orange above the waist, except bow-and-arrow hunting during archery season.
- Brochure license/permit exemptions include children under 16, Florida residents 65+, residents with a qualifying disabled-person certificate, and qualifying resident military personnel home on leave. They do not override quota permits marked no exemptions or required deer tags. Hunters born on/after June 1, 1975 need hunter-safety certification or the lawful supervised mentoring exception. Youth require adult supervision; mentoring license holders require a licensed supervisor aged 21+. Consult the complete brochure.
- The official brochure includes PDF BROCHURE and PDF MAP ONLY controls. Follow its current maps, access restrictions and FWC closure notices.

## Burmese Python: J. W. Corbett WMA / Commission-Managed Land, 2026-2027 expansion

Key: `python-corbett-3-2026-2027-expanded`. new draft.

Scope: managed_area: J. W. Corbett WMA

Review coverage: 2026-07-01 through 2027-06-30.

- [FWC J. W. Corbett WMA 2026-2027 regulations and map](https://app.myfwc.com/hgm/hgmsearch/wmad?brochureTitle=J.W.+Corbett) — checked 2026-10-12. Interactive brochure checked: area dates, legal species, bag limits, methods, permits, access and exceptions; PDF map available on the same page.
- [FWC hunting licenses and permits](https://myfwc.com/license/recreational/hunting/) — checked 2026-10-12. General license, management-area and season permits; brochure exemptions and area-specific quota restrictions retained.
- [FWC Executive Order 23-16](https://myfwc.com/media/31857/eo-23-16.pdf) — checked 2026-10-12. Page 2: traps and modified/free-bolt captive-bolt stunners prohibited; firearms need specific area authorization.
- [FWC python removal](https://myfwc.com/wildlifehabitats/nonnatives/python/removing/) — checked 2026-10-12. Area-specific removal is subject to the brochure and current FWC orders.
- [FWC humane killing methods](https://myfwc.com/wildlifehabitats/nonnatives/python/humane-killing-methods/) — checked 2026-10-12. Humane onsite killing and required second step; no public live transport.

### Year-round python removal / Burmese python

Dates: 2026-07-01 to 2027-06-30

Bag: No bag limit.

Licenses: No license or removal permit required for non-native reptiles; vehicle/access permits still apply where required.

Methods: Non-firearm removal is allowed year-round subject to access and humane-killing rules. Firearms may be used only during open brochure hunting seasons and only as allowed by that season. Follow the linked FWC humane-killing guidance.

- Bruce Bowman archery still-hunt area permits bows only, with the brochure's disability crossbow/airbow/draw-lock exceptions. Closed-to-hunting trails, boardwalk, parking and adjacent areas remain closed.
- Centerfire rifles are prohibited south and east of Stumper's Grade; all rifles are prohibited in the Pratt-Whitney buffer and within a quarter mile of the railroad and Mecca Farms.
- Enter/exit at designated entrances; when staffed, report at a check station on entry and departure and check harvested wildlife. No night gun hunting for these species.
- Motorized travel is restricted to named roads and designated access routes. From July 31, 2026 an OHV Hunting Permit is required for allowed off-road hunting vehicle use; airboats, ATVs, tracked vehicles and unregistered motorcycles remain prohibited.
- The area closes August 16 at midnight through August 28 at 8 a.m., with the brochure's limited road, through-hiking and boardwalk exceptions.
- EO23-16 prohibits traps and modified/free-bolt captive-bolt stunners; all other area access and equipment restrictions still apply.
- No live python may be removed from the area. Florida anti-cruelty law and FWC humane-killing guidance apply; the required second step prevents recovery after immediate loss of consciousness.
- A year-round python removal opportunity does not open deer/hog/turkey seasons or authorize firearm discharge outside lawful hunting seasons. Follow each season's allowed firearm methods and property closures.
- Python shooting hours are half an hour before sunrise until half an hour after sunset. Report sightings/take through FWC's non-native wildlife reporting service.
- In Bruce Bowman only hand tools and bows may take reptiles, except qualifying disability crossbow/airbow/draw-lock permits. Dogs may only search for reptiles during general gun season.
- Spring turkey rules prohibit hunting other animals; confirm the interaction with the separate reptile provisions with FWC before attempting firearm reptile removal during spring turkey dates.

Conditions for the whole scope:

- Hunting over bait, taking swimming deer or spotted fawns, and hunting in posted closed areas are prohibited.
- Ordinary shooting hours are half an hour before sunrise through half an hour after sunset; turkey has separate hours.
- Night gun hunting, fully automatic firearms and centerfire semiautomatic rifles with magazines capable of more than 5 rounds are prohibited.
- Deer hunters and companions need 500 square inches of fluorescent orange above the waist, except bow-and-arrow hunting during archery season.
- Brochure license/permit exemptions include children under 16, Florida residents 65+, residents with a qualifying disabled-person certificate, and qualifying resident military personnel home on leave. They do not override quota permits marked no exemptions or required deer tags. Hunters born on/after June 1, 1975 need hunter-safety certification or the lawful supervised mentoring exception. Youth require adult supervision; mentoring license holders require a licensed supervisor aged 21+. Consult the complete brochure.
- The official brochure includes PDF BROCHURE and PDF MAP ONLY controls. Follow its current maps, access restrictions and FWC closure notices.

## Burmese Python: Dinner Island Ranch / Wildlife Management Area (WMA), 2026-2027

Key: `python-dinner-island-2-2026-2027`. new draft.

Scope: managed_area: Dinner Island Ranch WMA

Review coverage: 2026-07-01 through 2027-06-30.

- [FWC Executive Order 23-16](https://myfwc.com/media/31857/eo-23-16.pdf) — checked 2026-10-12. Page 2 checked: traps and modified/free-bolt captive-bolt stunners prohibited; firearms need specific area authorization.
- [FWC Dinner Island Ranch 2026-2027 area brochure](https://app.myfwc.com/hgm/hgmsearch/wmad?brochureTitle=Dinner+Island+Ranch) — checked 2026-10-12. Read complete interactive brochure: season dates, antlered-only deer, quota/shared bags, turkey restrictions, hog methods, access and check-station waiver.
- [FWC Dinner Island Ranch 2026-2027 hunt calendar](https://app.myfwc.com/hsc/wmahuntcalendar/?areaName=dinner+island+ranch) — checked 2026-10-12. Corroborated every archery, muzzleloading, family, general gun, small-game and youth/spring turkey endpoint; Caracara Unit excluded.
- [FWC public python removal](https://myfwc.com/wildlifehabitats/nonnatives/python/removing/) — checked 2026-10-12. Dinner Island Ranch is on the named public-removal list; no license/removal permit/bag limit does not override area firearm or access restrictions.
- [FWC humane python removal](https://myfwc.com/wildlifehabitats/nonnatives/python/humane-killing-methods/) — checked 2026-10-12. Humane onsite two-step removal and public prohibition on live transport checked; follow training and property-specific firearm rules.

### Dinner Island Ranch non-native reptile removal / Burmese python

Dates: 2026-07-01 to 2027-06-30

Bag: No bag limit.

Licenses: No hunting license or removal permit is required for public python removal within FWC's listed area scope; access and vehicle/camping permits are separate.

Methods: Non-firearm methods may be used year-round. Firearms may be used only during open area hunting seasons, with methods allowed for that season and the brochure's shooting restrictions. Follow FWC humane-removal training and the required two-step method; the first step alone is insufficient.

- EO23-16 prohibits traps and modified/free-bolt captive-bolt stunners; all other area access and equipment restrictions still apply.
- No dogs for non-native reptile removal. Humanely kill on site; members of the public may not remove live pythons. Florida anti-cruelty requirements apply.
- Firearm reptile removal is limited to half an hour before sunrise through half an hour after sunset and does not override a season's weapon or access restrictions.
- The spring turkey section prohibits hunting other animals, while the non-native reptile section qualifies firearm take by open seasons. This lookup does not establish a spring/youth-turkey firearm exception; confirm this interaction with FWC before using a firearm for python removal during those hunts.

Conditions for the whole scope:

- Dinner Island Ranch coverage excludes the separately regulated Caracara Unit. Enter and exit at the designated entrance; posted closed areas remain closed.
- The 2026-2027 Attention Hunters notice says there is no operating check station and waives all check-station duties. Deer and turkey must still be logged before moving and officially reported within 24 hours. HuntIt does not submit the FWC report.
- Vehicles may use named and numbered roads only, except valid Alternative Mobility Permit allowances. Vehicles are prohibited from 1.5 hours after sunset until 1.5 hours before sunrise, except camping-permit holders and guests accessing their designated campsite.
- Airboats, ATVs, swamp buggies, tracked vehicles and unregistered motorcycles are prohibited, except quota hunters and their guest permit holders may use ATVs and swamp buggies on named/numbered roads during their permitted archery, muzzleloading gun, family or general gun hunt. This exception does not authorize off-road travel.
- Camping requires an FWC permit and is limited to designated campgrounds. Horses are prohibited during archery, muzzleloading gun, family, general gun and spring turkey seasons; otherwise use designated roads.
- On posted dove fields, hunting during dove season is limited to Saturdays; otherwise only hunting allowed by the applicable area season is authorized. Check the brochure map and current closures before selecting a hunting site.
- No hunting over bait, night gun hunting, fully automatic firearms or centerfire semiautomatic rifles with magazines holding more than 5 rounds. The brochure's ammunition, equipment and closed-area restrictions apply.
- Ordinary shooting hours are half an hour before sunrise through half an hour after sunset. Turkey shooting ends at sunset.
- Dogs may not hunt deer, wild hog or furbearers; leashed dogs may trail wounded game under the brochure's conditions. No dogs may pursue non-native reptiles.
- License/season-permit exemptions do not waive a quota permit marked no exemptions. Check hunter-safety requirements and individual exemptions in the full brochure.
- Nonresident hunters taking native game need the applicable annual hunting license unless exempt. A hunting license is not required when hunting wild hog or removing python within the stated exception.

## Burmese Python: Dinner Island Ranch / Commission-Managed Land, 2026-2027

Key: `python-dinner-island-3-2026-2027`. new draft.

Scope: managed_area: Dinner Island Ranch WMA

Review coverage: 2026-07-01 through 2027-06-30.

- [FWC Executive Order 23-16](https://myfwc.com/media/31857/eo-23-16.pdf) — checked 2026-10-12. Page 2 checked: traps and modified/free-bolt captive-bolt stunners prohibited; firearms need specific area authorization.
- [FWC Dinner Island Ranch 2026-2027 area brochure](https://app.myfwc.com/hgm/hgmsearch/wmad?brochureTitle=Dinner+Island+Ranch) — checked 2026-10-12. Read complete interactive brochure: season dates, antlered-only deer, quota/shared bags, turkey restrictions, hog methods, access and check-station waiver.
- [FWC Dinner Island Ranch 2026-2027 hunt calendar](https://app.myfwc.com/hsc/wmahuntcalendar/?areaName=dinner+island+ranch) — checked 2026-10-12. Corroborated every archery, muzzleloading, family, general gun, small-game and youth/spring turkey endpoint; Caracara Unit excluded.
- [FWC public python removal](https://myfwc.com/wildlifehabitats/nonnatives/python/removing/) — checked 2026-10-12. Dinner Island Ranch is on the named public-removal list; no license/removal permit/bag limit does not override area firearm or access restrictions.
- [FWC humane python removal](https://myfwc.com/wildlifehabitats/nonnatives/python/humane-killing-methods/) — checked 2026-10-12. Humane onsite two-step removal and public prohibition on live transport checked; follow training and property-specific firearm rules.

### Dinner Island Ranch non-native reptile removal / Burmese python

Dates: 2026-07-01 to 2027-06-30

Bag: No bag limit.

Licenses: No hunting license or removal permit is required for public python removal within FWC's listed area scope; access and vehicle/camping permits are separate.

Methods: Non-firearm methods may be used year-round. Firearms may be used only during open area hunting seasons, with methods allowed for that season and the brochure's shooting restrictions. Follow FWC humane-removal training and the required two-step method; the first step alone is insufficient.

- EO23-16 prohibits traps and modified/free-bolt captive-bolt stunners; all other area access and equipment restrictions still apply.
- No dogs for non-native reptile removal. Humanely kill on site; members of the public may not remove live pythons. Florida anti-cruelty requirements apply.
- Firearm reptile removal is limited to half an hour before sunrise through half an hour after sunset and does not override a season's weapon or access restrictions.
- The spring turkey section prohibits hunting other animals, while the non-native reptile section qualifies firearm take by open seasons. This lookup does not establish a spring/youth-turkey firearm exception; confirm this interaction with FWC before using a firearm for python removal during those hunts.

Conditions for the whole scope:

- Dinner Island Ranch coverage excludes the separately regulated Caracara Unit. Enter and exit at the designated entrance; posted closed areas remain closed.
- The 2026-2027 Attention Hunters notice says there is no operating check station and waives all check-station duties. Deer and turkey must still be logged before moving and officially reported within 24 hours. HuntIt does not submit the FWC report.
- Vehicles may use named and numbered roads only, except valid Alternative Mobility Permit allowances. Vehicles are prohibited from 1.5 hours after sunset until 1.5 hours before sunrise, except camping-permit holders and guests accessing their designated campsite.
- Airboats, ATVs, swamp buggies, tracked vehicles and unregistered motorcycles are prohibited, except quota hunters and their guest permit holders may use ATVs and swamp buggies on named/numbered roads during their permitted archery, muzzleloading gun, family or general gun hunt. This exception does not authorize off-road travel.
- Camping requires an FWC permit and is limited to designated campgrounds. Horses are prohibited during archery, muzzleloading gun, family, general gun and spring turkey seasons; otherwise use designated roads.
- On posted dove fields, hunting during dove season is limited to Saturdays; otherwise only hunting allowed by the applicable area season is authorized. Check the brochure map and current closures before selecting a hunting site.
- No hunting over bait, night gun hunting, fully automatic firearms or centerfire semiautomatic rifles with magazines holding more than 5 rounds. The brochure's ammunition, equipment and closed-area restrictions apply.
- Ordinary shooting hours are half an hour before sunrise through half an hour after sunset. Turkey shooting ends at sunset.
- Dogs may not hunt deer, wild hog or furbearers; leashed dogs may trail wounded game under the brochure's conditions. No dogs may pursue non-native reptiles.
- License/season-permit exemptions do not waive a quota permit marked no exemptions. Check hunter-safety requirements and individual exemptions in the full brochure.
- Nonresident hunters taking native game need the applicable annual hunting license unless exempt. A hunting license is not required when hunting wild hog or removing python within the stated exception.

## Burmese python: Fisheating Creek east of US27 / Wildlife Management Area (WMA), 2026-2027

Key: `python-fisheating-east-2-2026-2027`. new draft.

Scope: managed_area: Fisheating Creek WMA; regulatory_area: Fisheating Creek east of U.S. Highway 27: special-opportunity turkey area only

Review coverage: 2026-07-01 through 2027-06-30.

- [FWC EO 23-16 public non-native reptile exceptions](https://myfwc.com/media/31857/eo-23-16.pdf) — checked 2026-10-12. Page 2 checked: west gun/management-area exception, east special-opportunity season/permit restriction, traps and captive-bolt restrictions.
- [FWC Fisheating Creek 2026-2027 area brochure](https://app.myfwc.com/hgm/hgmsearch/wmad?brochureTitle=Fisheating+Creek) — checked 2026-10-12. Interactive 2026-2027 reptile section checked: west year-round excludes firearms/airguns/bows/crossbows, east special-opportunity conditions, methods, hours and no dogs/live removal.
- [FWC Fisheating Creek 2026-2027 hunt calendar](https://app.myfwc.com/hsc/wmahuntcalendar/?areaName=fisheating+creek) — checked 2026-10-12. Confirmed east special-opportunity spring turkey periods March 6-12 and March 20-26, 2027, distinct from the west-side spring turkey hunts.
- [FWC public python removal](https://myfwc.com/wildlifehabitats/nonnatives/python/removing/) — checked 2026-10-12. Listed-area opportunity and no bag limit are qualified by EO 23-16 and the specific area rules.
- [FWC humane python killing guidance](https://myfwc.com/wildlifehabitats/nonnatives/python/humane-killing-methods/) — checked 2026-10-12. Required humane onsite two-step killing; public live transport is prohibited and equipment must satisfy the area order.

### Fisheating Creek east special-opportunity reptile removal / Burmese python in the east-side special-opportunity spring turkey area only

Dates: 2027-03-06 to 2027-03-12; 2027-03-20 to 2027-03-26

Bag: No python bag limit; turkey quota/bag limits do not authorize a separate turkey harvest.

Licenses: A valid Fisheating Creek Special-Opportunity Spring Turkey Permit for the selected hunt is required for python removal, including removal without a firearm. The EO does not require a separate hunting license for reptile take; turkey hunting has its own license and permit requirements.

Methods: Only methods allowed for the special-opportunity spring turkey season: bows, crossbows, PCP airguns propelling a bolt or arrow, and shotguns using No. 2 or smaller shot, subject to brochure conditions and humane killing rules. Rifles, pistols and PCP bullets are not authorized by this season's methods.

- East of U.S. Highway 27, reptiles may be taken only inside the designated Special-Opportunity Spring Turkey Area, during March 6-12 or March 20-26, 2027, by holders of the valid special-opportunity permit. There is no year-round east-side removal exception.
- The brochure expressly authorizes the east-side reptile opportunity under the special-opportunity conditions; it is not an inference from general turkey dates or another WMA's year-round rules.
- Turkey shooting on this area has an earlier 1 p.m. cutoff; do not apply the reptile shooting-hours provision to turkey. Area access and permit conditions can further limit the reptile opportunity.

Conditions for the whole scope:

- Select the correct side of U.S. Highway 27 and confirm the exact hunting parcel on the official brochure map. Posted closed areas and access restrictions remain controlling.
- EO 23-16 prohibits traps and modified or free-bolt captive-bolt stunners on these public areas. It does not authorize entry onto private property without permission.
- No live python may be removed. Humanely kill on site under Florida anti-cruelty law and FWC training; the required second step must prevent recovery after immediate loss of consciousness.
- Dogs may not be used for non-native reptile removal. Reptile shooting hours are half an hour before sunrise through half an hour after sunset, subject to area access and firearm restrictions.
- Python removal does not authorize deer, hog or turkey hunting, replace a permit required for another activity, or override closures. Check current FWC notices and the full brochure.

## Burmese python: Fisheating Creek east of US27 / Commission-Managed Land, 2026-2027

Key: `python-fisheating-east-3-2026-2027`. new draft.

Scope: managed_area: Fisheating Creek WMA; regulatory_area: Fisheating Creek east of U.S. Highway 27: special-opportunity turkey area only

Review coverage: 2026-07-01 through 2027-06-30.

- [FWC EO 23-16 public non-native reptile exceptions](https://myfwc.com/media/31857/eo-23-16.pdf) — checked 2026-10-12. Page 2 checked: west gun/management-area exception, east special-opportunity season/permit restriction, traps and captive-bolt restrictions.
- [FWC Fisheating Creek 2026-2027 area brochure](https://app.myfwc.com/hgm/hgmsearch/wmad?brochureTitle=Fisheating+Creek) — checked 2026-10-12. Interactive 2026-2027 reptile section checked: west year-round excludes firearms/airguns/bows/crossbows, east special-opportunity conditions, methods, hours and no dogs/live removal.
- [FWC Fisheating Creek 2026-2027 hunt calendar](https://app.myfwc.com/hsc/wmahuntcalendar/?areaName=fisheating+creek) — checked 2026-10-12. Confirmed east special-opportunity spring turkey periods March 6-12 and March 20-26, 2027, distinct from the west-side spring turkey hunts.
- [FWC public python removal](https://myfwc.com/wildlifehabitats/nonnatives/python/removing/) — checked 2026-10-12. Listed-area opportunity and no bag limit are qualified by EO 23-16 and the specific area rules.
- [FWC humane python killing guidance](https://myfwc.com/wildlifehabitats/nonnatives/python/humane-killing-methods/) — checked 2026-10-12. Required humane onsite two-step killing; public live transport is prohibited and equipment must satisfy the area order.

### Fisheating Creek east special-opportunity reptile removal / Burmese python in the east-side special-opportunity spring turkey area only

Dates: 2027-03-06 to 2027-03-12; 2027-03-20 to 2027-03-26

Bag: No python bag limit; turkey quota/bag limits do not authorize a separate turkey harvest.

Licenses: A valid Fisheating Creek Special-Opportunity Spring Turkey Permit for the selected hunt is required for python removal, including removal without a firearm. The EO does not require a separate hunting license for reptile take; turkey hunting has its own license and permit requirements.

Methods: Only methods allowed for the special-opportunity spring turkey season: bows, crossbows, PCP airguns propelling a bolt or arrow, and shotguns using No. 2 or smaller shot, subject to brochure conditions and humane killing rules. Rifles, pistols and PCP bullets are not authorized by this season's methods.

- East of U.S. Highway 27, reptiles may be taken only inside the designated Special-Opportunity Spring Turkey Area, during March 6-12 or March 20-26, 2027, by holders of the valid special-opportunity permit. There is no year-round east-side removal exception.
- The brochure expressly authorizes the east-side reptile opportunity under the special-opportunity conditions; it is not an inference from general turkey dates or another WMA's year-round rules.
- Turkey shooting on this area has an earlier 1 p.m. cutoff; do not apply the reptile shooting-hours provision to turkey. Area access and permit conditions can further limit the reptile opportunity.

Conditions for the whole scope:

- Select the correct side of U.S. Highway 27 and confirm the exact hunting parcel on the official brochure map. Posted closed areas and access restrictions remain controlling.
- EO 23-16 prohibits traps and modified or free-bolt captive-bolt stunners on these public areas. It does not authorize entry onto private property without permission.
- No live python may be removed. Humanely kill on site under Florida anti-cruelty law and FWC training; the required second step must prevent recovery after immediate loss of consciousness.
- Dogs may not be used for non-native reptile removal. Reptile shooting hours are half an hour before sunrise through half an hour after sunset, subject to area access and firearm restrictions.
- Python removal does not authorize deer, hog or turkey hunting, replace a permit required for another activity, or override closures. Check current FWC notices and the full brochure.

## Burmese python: Fisheating Creek west of US27 / Wildlife Management Area (WMA), 2026-2027

Key: `python-fisheating-west-2-2026-2027`. new draft.

Scope: managed_area: Fisheating Creek WMA; regulatory_area: Fisheating Creek west of U.S. Highway 27

Review coverage: 2026-07-01 through 2027-06-30.

- [FWC EO 23-16 public non-native reptile exceptions](https://myfwc.com/media/31857/eo-23-16.pdf) — checked 2026-10-12. Page 2 checked: west gun/management-area exception, east special-opportunity season/permit restriction, traps and captive-bolt restrictions.
- [FWC Fisheating Creek 2026-2027 area brochure](https://app.myfwc.com/hgm/hgmsearch/wmad?brochureTitle=Fisheating+Creek) — checked 2026-10-12. Interactive 2026-2027 reptile section checked: west year-round excludes firearms/airguns/bows/crossbows, east special-opportunity conditions, methods, hours and no dogs/live removal.
- [FWC Fisheating Creek 2026-2027 hunt calendar](https://app.myfwc.com/hsc/wmahuntcalendar/?areaName=fisheating+creek) — checked 2026-10-12. Confirmed east special-opportunity spring turkey periods March 6-12 and March 20-26, 2027, distinct from the west-side spring turkey hunts.
- [FWC public python removal](https://myfwc.com/wildlifehabitats/nonnatives/python/removing/) — checked 2026-10-12. Listed-area opportunity and no bag limit are qualified by EO 23-16 and the specific area rules.
- [FWC humane python killing guidance](https://myfwc.com/wildlifehabitats/nonnatives/python/humane-killing-methods/) — checked 2026-10-12. Required humane onsite two-step killing; public live transport is prohibited and equipment must satisfy the area order.

### Fisheating Creek west year-round limited-equipment removal / Burmese python west of U.S. Highway 27

Dates: 2026-07-01 to 2027-06-30

Bag: No bag limit.

Licenses: No hunting license or management area permit required for year-round removal without a gun. A management area permit is required when using a gun west of U.S. Highway 27; other access and season restrictions still apply.

Methods: Year-round removal uses lawful humane methods other than firearms, airguns, bows or crossbows. Firearms, airguns, bows and crossbows may be used only during open brochure hunting seasons and only as allowed by the particular season. This year-round rule does not authorize those weapons outside an open hunt.

- The west-side year-round exception is narrower than 'non-firearm': it also excludes airguns, bows and crossbows outside open hunting seasons.
- When using any seasonal hunting equipment, confirm its lawful season, method, access conditions and any required hunt permit in the official brochure; the year-round limited-equipment rule is not a weapon-season authorization.
- A west-side gun removal requires a management area permit under EO 23-16 even though ordinary public python removal generally does not. The east-side special-opportunity permit is a separate condition.

Conditions for the whole scope:

- Select the correct side of U.S. Highway 27 and confirm the exact hunting parcel on the official brochure map. Posted closed areas and access restrictions remain controlling.
- EO 23-16 prohibits traps and modified or free-bolt captive-bolt stunners on these public areas. It does not authorize entry onto private property without permission.
- No live python may be removed. Humanely kill on site under Florida anti-cruelty law and FWC training; the required second step must prevent recovery after immediate loss of consciousness.
- Dogs may not be used for non-native reptile removal. Reptile shooting hours are half an hour before sunrise through half an hour after sunset, subject to area access and firearm restrictions.
- Python removal does not authorize deer, hog or turkey hunting, replace a permit required for another activity, or override closures. Check current FWC notices and the full brochure.

## Burmese python: Fisheating Creek west of US27 / Commission-Managed Land, 2026-2027

Key: `python-fisheating-west-3-2026-2027`. new draft.

Scope: managed_area: Fisheating Creek WMA; regulatory_area: Fisheating Creek west of U.S. Highway 27

Review coverage: 2026-07-01 through 2027-06-30.

- [FWC EO 23-16 public non-native reptile exceptions](https://myfwc.com/media/31857/eo-23-16.pdf) — checked 2026-10-12. Page 2 checked: west gun/management-area exception, east special-opportunity season/permit restriction, traps and captive-bolt restrictions.
- [FWC Fisheating Creek 2026-2027 area brochure](https://app.myfwc.com/hgm/hgmsearch/wmad?brochureTitle=Fisheating+Creek) — checked 2026-10-12. Interactive 2026-2027 reptile section checked: west year-round excludes firearms/airguns/bows/crossbows, east special-opportunity conditions, methods, hours and no dogs/live removal.
- [FWC Fisheating Creek 2026-2027 hunt calendar](https://app.myfwc.com/hsc/wmahuntcalendar/?areaName=fisheating+creek) — checked 2026-10-12. Confirmed east special-opportunity spring turkey periods March 6-12 and March 20-26, 2027, distinct from the west-side spring turkey hunts.
- [FWC public python removal](https://myfwc.com/wildlifehabitats/nonnatives/python/removing/) — checked 2026-10-12. Listed-area opportunity and no bag limit are qualified by EO 23-16 and the specific area rules.
- [FWC humane python killing guidance](https://myfwc.com/wildlifehabitats/nonnatives/python/humane-killing-methods/) — checked 2026-10-12. Required humane onsite two-step killing; public live transport is prohibited and equipment must satisfy the area order.

### Fisheating Creek west year-round limited-equipment removal / Burmese python west of U.S. Highway 27

Dates: 2026-07-01 to 2027-06-30

Bag: No bag limit.

Licenses: No hunting license or management area permit required for year-round removal without a gun. A management area permit is required when using a gun west of U.S. Highway 27; other access and season restrictions still apply.

Methods: Year-round removal uses lawful humane methods other than firearms, airguns, bows or crossbows. Firearms, airguns, bows and crossbows may be used only during open brochure hunting seasons and only as allowed by the particular season. This year-round rule does not authorize those weapons outside an open hunt.

- The west-side year-round exception is narrower than 'non-firearm': it also excludes airguns, bows and crossbows outside open hunting seasons.
- When using any seasonal hunting equipment, confirm its lawful season, method, access conditions and any required hunt permit in the official brochure; the year-round limited-equipment rule is not a weapon-season authorization.
- A west-side gun removal requires a management area permit under EO 23-16 even though ordinary public python removal generally does not. The east-side special-opportunity permit is a separate condition.

Conditions for the whole scope:

- Select the correct side of U.S. Highway 27 and confirm the exact hunting parcel on the official brochure map. Posted closed areas and access restrictions remain controlling.
- EO 23-16 prohibits traps and modified or free-bolt captive-bolt stunners on these public areas. It does not authorize entry onto private property without permission.
- No live python may be removed. Humanely kill on site under Florida anti-cruelty law and FWC training; the required second step must prevent recovery after immediate loss of consciousness.
- Dogs may not be used for non-native reptile removal. Reptile shooting hours are half an hour before sunrise through half an hour after sunset, subject to area access and firearm restrictions.
- Python removal does not authorize deer, hog or turkey hunting, replace a permit required for another activity, or override closures. Check current FWC notices and the full brochure.

## Burmese Python: Holey Land WMA / Wildlife Management Area (WMA), 2026-2027 expansion

Key: `python-holey-land-2-2026-2027-expanded`. new draft.

Scope: managed_area: Holey Land WMA

Review coverage: 2026-07-01 through 2027-06-30.

- [FWC Holey Land WMA 2026-2027 regulations and map](https://app.myfwc.com/hgm/hgmsearch/wmad?brochureTitle=Holey+Land) — checked 2026-10-12. Interactive brochure checked: area dates, legal species, bag limits, methods, permits, access and exceptions; PDF map available on the same page.
- [FWC hunting licenses and permits](https://myfwc.com/license/recreational/hunting/) — checked 2026-10-12. General license, management-area and season permits; brochure exemptions and area-specific quota restrictions retained.
- [FWC Executive Order 23-16](https://myfwc.com/media/31857/eo-23-16.pdf) — checked 2026-10-12. Page 2: traps and modified/free-bolt captive-bolt stunners prohibited; firearms need specific area authorization.
- [FWC python removal](https://myfwc.com/wildlifehabitats/nonnatives/python/removing/) — checked 2026-10-12. Area-specific removal is subject to the brochure and current FWC orders.
- [FWC humane killing methods](https://myfwc.com/wildlifehabitats/nonnatives/python/humane-killing-methods/) — checked 2026-10-12. Humane onsite killing and required second step; no public live transport.

### Year-round python removal / Burmese python

Dates: 2026-07-01 to 2027-06-30

Bag: No bag limit.

Licenses: No license or removal permit required for non-native reptiles; vehicle/access permits still apply where required.

Methods: Non-firearm removal is allowed year-round subject to access and humane-killing rules. Firearms may be used only during open brochure hunting seasons and only as allowed by that season. Follow the linked FWC humane-killing guidance.

- Entry/exit is limited to the L-5 and Miami Canal levees. Hunting on roads, ramps, parking/camping areas, levees or adjacent powerline pads, and gun hunting on/from/across levees, is prohibited.
- Motorized use, scouting periods, flags and access routes are restricted. During general gun-vehicle season walk-hunting is closed and only vehicles authorized by its permits may operate; consult the map and permit conditions.
- Dogs may hunt deer/hog only during general gun-vehicle season; deer-dog hunting needs a valid WMA deer-dog permit, and dogs pursuing deer/hog need remote tracking and correction devices.
- When weekend check stations are staffed, check deer at the L-5 levee station before quartering, dismembering or removing them. General gun-vehicle deer must be immediately tagged with the FWC antlered deer tag.
- EO23-16 prohibits traps and modified/free-bolt captive-bolt stunners; all other area access and equipment restrictions still apply.
- No live python may be removed from the area. Florida anti-cruelty law and FWC humane-killing guidance apply; the required second step prevents recovery after immediate loss of consciousness.
- A year-round python removal opportunity does not open deer/hog/turkey seasons or authorize firearm discharge outside lawful hunting seasons. Follow each season's allowed firearm methods and property closures.
- Python shooting hours are half an hour before sunrise until half an hour after sunset. Report sightings/take through FWC's non-native wildlife reporting service.
- Centerfire rifle take is prohibited March 8-April 11, 2027; the seasonal firearm restriction still applies at all other times. Dogs may only search for reptiles during general gun-vehicle season.

Conditions for the whole scope:

- Hunting over bait, taking swimming deer or spotted fawns, and hunting in posted closed areas are prohibited.
- Ordinary shooting hours are half an hour before sunrise through half an hour after sunset; turkey has separate hours.
- Night gun hunting, fully automatic firearms and centerfire semiautomatic rifles with magazines capable of more than 5 rounds are prohibited.
- Deer hunters and companions need 500 square inches of fluorescent orange above the waist, except bow-and-arrow hunting during archery season.
- Brochure license/permit exemptions include children under 16, Florida residents 65+, residents with a qualifying disabled-person certificate, and qualifying resident military personnel home on leave. They do not override quota permits marked no exemptions or required deer tags. Hunters born on/after June 1, 1975 need hunter-safety certification or the lawful supervised mentoring exception. Youth require adult supervision; mentoring license holders require a licensed supervisor aged 21+. Consult the complete brochure.
- The official brochure includes PDF BROCHURE and PDF MAP ONLY controls. Follow its current maps, access restrictions and FWC closure notices.

## Burmese Python: Holey Land WMA / Commission-Managed Land, 2026-2027 expansion

Key: `python-holey-land-3-2026-2027-expanded`. new draft.

Scope: managed_area: Holey Land WMA

Review coverage: 2026-07-01 through 2027-06-30.

- [FWC Holey Land WMA 2026-2027 regulations and map](https://app.myfwc.com/hgm/hgmsearch/wmad?brochureTitle=Holey+Land) — checked 2026-10-12. Interactive brochure checked: area dates, legal species, bag limits, methods, permits, access and exceptions; PDF map available on the same page.
- [FWC hunting licenses and permits](https://myfwc.com/license/recreational/hunting/) — checked 2026-10-12. General license, management-area and season permits; brochure exemptions and area-specific quota restrictions retained.
- [FWC Executive Order 23-16](https://myfwc.com/media/31857/eo-23-16.pdf) — checked 2026-10-12. Page 2: traps and modified/free-bolt captive-bolt stunners prohibited; firearms need specific area authorization.
- [FWC python removal](https://myfwc.com/wildlifehabitats/nonnatives/python/removing/) — checked 2026-10-12. Area-specific removal is subject to the brochure and current FWC orders.
- [FWC humane killing methods](https://myfwc.com/wildlifehabitats/nonnatives/python/humane-killing-methods/) — checked 2026-10-12. Humane onsite killing and required second step; no public live transport.

### Year-round python removal / Burmese python

Dates: 2026-07-01 to 2027-06-30

Bag: No bag limit.

Licenses: No license or removal permit required for non-native reptiles; vehicle/access permits still apply where required.

Methods: Non-firearm removal is allowed year-round subject to access and humane-killing rules. Firearms may be used only during open brochure hunting seasons and only as allowed by that season. Follow the linked FWC humane-killing guidance.

- Entry/exit is limited to the L-5 and Miami Canal levees. Hunting on roads, ramps, parking/camping areas, levees or adjacent powerline pads, and gun hunting on/from/across levees, is prohibited.
- Motorized use, scouting periods, flags and access routes are restricted. During general gun-vehicle season walk-hunting is closed and only vehicles authorized by its permits may operate; consult the map and permit conditions.
- Dogs may hunt deer/hog only during general gun-vehicle season; deer-dog hunting needs a valid WMA deer-dog permit, and dogs pursuing deer/hog need remote tracking and correction devices.
- When weekend check stations are staffed, check deer at the L-5 levee station before quartering, dismembering or removing them. General gun-vehicle deer must be immediately tagged with the FWC antlered deer tag.
- EO23-16 prohibits traps and modified/free-bolt captive-bolt stunners; all other area access and equipment restrictions still apply.
- No live python may be removed from the area. Florida anti-cruelty law and FWC humane-killing guidance apply; the required second step prevents recovery after immediate loss of consciousness.
- A year-round python removal opportunity does not open deer/hog/turkey seasons or authorize firearm discharge outside lawful hunting seasons. Follow each season's allowed firearm methods and property closures.
- Python shooting hours are half an hour before sunrise until half an hour after sunset. Report sightings/take through FWC's non-native wildlife reporting service.
- Centerfire rifle take is prohibited March 8-April 11, 2027; the seasonal firearm restriction still applies at all other times. Dogs may only search for reptiles during general gun-vehicle season.

Conditions for the whole scope:

- Hunting over bait, taking swimming deer or spotted fawns, and hunting in posted closed areas are prohibited.
- Ordinary shooting hours are half an hour before sunrise through half an hour after sunset; turkey has separate hours.
- Night gun hunting, fully automatic firearms and centerfire semiautomatic rifles with magazines capable of more than 5 rounds are prohibited.
- Deer hunters and companions need 500 square inches of fluorescent orange above the waist, except bow-and-arrow hunting during archery season.
- Brochure license/permit exemptions include children under 16, Florida residents 65+, residents with a qualifying disabled-person certificate, and qualifying resident military personnel home on leave. They do not override quota permits marked no exemptions or required deer tags. Hunters born on/after June 1, 1975 need hunter-safety certification or the lawful supervised mentoring exception. Youth require adult supervision; mentoring license holders require a licensed supervisor aged 21+. Consult the complete brochure.
- The official brochure includes PDF BROCHURE and PDF MAP ONLY controls. Follow its current maps, access restrictions and FWC closure notices.

## Burmese python: private land, 2026

Key: `python-private-2026`. proposed revision of existing approved draft.

Scope: Private-land statewide exception

Review coverage: 2026-01-01 through 2026-12-31.

- [FWC Removing Pythons in Florida](https://myfwc.com/wildlifehabitats/nonnatives/python/removing/) — checked 2026-10-12. Current 32-area list, year-round removal, no license/permit and no bag limit checked.
- [FWC Burmese Python regulatory status](https://myfwc.com/wildlifehabitats/profiles/reptiles/snakes/burmese-python/) — checked 2026-10-12. Anti-cruelty protection and private-property permission checked.
- [FWC humane killing guidance](https://myfwc.com/wildlifehabitats/nonnatives/python/humane-killing-methods/) — checked 2026-10-12. Humane onsite removal and prohibition on public live transport checked.
- [FWC 2026 python removal opportunities](https://myfwc.com/news/all-news/python-challenge-0826/) — checked 2026-10-12. Explicit private-land no hunting-license/no-permit statement checked.
- [FWC current area notices](https://myfwc.com/recreation/notices/) — checked 2026-10-12. Current closure directory checked; notices can change after this data check.

### Year-round python removal / Burmese python

Dates: 2026-01-01 to 2026-12-31

Bag: No bag limit.

Licenses: No hunting license or removal permit required within the stated scope.

Methods: FWC describes captive-bolt equipment or a lawfully used firearm/PCP air gun for immediate loss of consciousness, followed by pithing as the required second step to prevent recovery. Follow FWC/AVMA training and all property-specific firearm rules.

- Florida anti-cruelty law applies. Humanely kill at the capture location; members of the public may not transport live pythons.
- Obtain appropriate humane-removal training before attempting to handle or euthanize a large constrictor. The linked FWC guidance explains both required steps; the first step alone is insufficient.
- Follow Executive Order 23-16 and specific area access, closures and firearm rules. The annual area list does not override those rules.

Conditions for the whole scope:

- Check the linked FWC area notices for temporary closures; this local dataset does not poll live closures.

## Burmese python: 15 FWC-listed areas / Wildlife Management Area (WMA), 2026

Key: `python-public-2-2026`. proposed revision of existing approved draft.

Scope: managed_area: Allapattah Flats WMA, Big Cypress WMA, Dinner Island Ranch WMA, Everglades and Francis S. Taylor WMA, Holey Land WMA, J. W. Corbett WMA, Picayune Strand WMA, Rotenberger WMA, Spirit-of-the-Wild WMA, Okaloacoochee Slough WMA, Everglades Headwaters WMA, Kissimmee Bend Unit, Fred C. Babcock / Cecil M. Webb WMA, Fred C. Babcock/Cecil M. Webb WMA Yucca Pens Unit, Orange Hammock WMA

Review coverage: 2026-01-01 through 2026-12-31.

- [FWC Removing Pythons in Florida](https://myfwc.com/wildlifehabitats/nonnatives/python/removing/) — checked 2026-10-12. Current 32-area list, year-round removal, no license/permit and no bag limit checked.
- [FWC Burmese Python regulatory status](https://myfwc.com/wildlifehabitats/profiles/reptiles/snakes/burmese-python/) — checked 2026-10-12. Anti-cruelty protection and private-property permission checked.
- [FWC humane killing guidance](https://myfwc.com/wildlifehabitats/nonnatives/python/humane-killing-methods/) — checked 2026-10-12. Humane onsite removal and prohibition on public live transport checked.
- [FWC 2026 python removal opportunities](https://myfwc.com/news/all-news/python-challenge-0826/) — checked 2026-10-12. Explicit private-land no hunting-license/no-permit statement checked.
- [FWC current area notices](https://myfwc.com/recreation/notices/) — checked 2026-10-12. Current closure directory checked; notices can change after this data check.
- [FWC Executive Order 23-16](https://myfwc.com/media/31857/eo-23-16.pdf) — checked 2026-10-12. Checked year-round scope, traps/free-bolt prohibition and east/west US27 Fisheating Creek exceptions on page 2.

### Year-round python removal / Burmese python

Dates: 2026-01-01 to 2026-12-31

Bag: No bag limit.

Licenses: No hunting license or removal permit required within the stated scope.

Methods: FWC describes captive-bolt equipment or a lawfully used firearm/PCP air gun for immediate loss of consciousness, followed by pithing as the required second step to prevent recovery. Follow FWC/AVMA training and all property-specific firearm rules.

- Florida anti-cruelty law applies. Humanely kill at the capture location; members of the public may not transport live pythons.
- Obtain appropriate humane-removal training before attempting to handle or euthanize a large constrictor. The linked FWC guidance explains both required steps; the first step alone is insufficient.
- Follow Executive Order 23-16 and specific area access, closures and firearm rules. The annual area list does not override those rules.

Conditions for the whole scope:

- Coverage is restricted to FWC's current 32-area list (the WMA land-type option covers its WMA entries); other public lands are not covered.
- Check the linked FWC area notices for temporary closures; this local dataset does not poll live closures.
- Fisheating Creek uses separate east/west US27 reviewed scopes because EO23-16 imposes special season and permit conditions there.
- EO23-16 prohibits traps and modified/free-bolt captive-bolt stunners. Firearms require authorization under the specific area rules; closed-to-public-access portions remain closed.

## Burmese python: 32 FWC-listed areas / Commission-Managed Land, 2026

Key: `python-public-3-2026`. proposed revision of existing approved draft.

Scope: managed_area: A I -FEB PSGHA, Allapattah Flats WMA, Allapattah Flats PSGHA, Big Cypress WMA, C-23/24 Reservoir PSGHA, CREW WEA, Dinner Island Ranch WMA, DuPuis Dove Field PSGHA, Everglades and Francis S. Taylor WMA, Frog Pond North PSGHA, Holey Land WMA, J. W. Corbett WMA, John C. and Mariana Jones/Hungryland WEA, John G. and Susan H. DuPuis, Jr. WEA, Picayune Strand WMA, Rocky Glades PSGHA, Rotenberger WMA, Southern Glades WEA, Spirit-of-the-Wild WMA, Stormwater Treatment Area 1 West PSGHA, Stormwater Treatment Area 2 PSGHA, Stormwater Treatment Area 3/4 PSGHA, Stormwater Treatment Area 5/6 PSGHA, Okaloacoochee Slough WMA, Everglades Headwaters WMA, Kissimmee Bend Unit, Fred C. Babcock / Cecil M. Webb WMA, Fred C. Babcock/Cecil M. Webb WMA Yucca Pens Unit, Orange Hammock WMA, Myakka State Forest PSGHA, Hungryland Small Game Area (within John C. and Mariana Jones/Hungryland WEA), Everglades Headwaters National Wildlife Refuge, Okeechobee Unit

Review coverage: 2026-01-01 through 2026-12-31.

- [FWC Removing Pythons in Florida](https://myfwc.com/wildlifehabitats/nonnatives/python/removing/) — checked 2026-10-12. Current 32-area list, year-round removal, no license/permit and no bag limit checked.
- [FWC Burmese Python regulatory status](https://myfwc.com/wildlifehabitats/profiles/reptiles/snakes/burmese-python/) — checked 2026-10-12. Anti-cruelty protection and private-property permission checked.
- [FWC humane killing guidance](https://myfwc.com/wildlifehabitats/nonnatives/python/humane-killing-methods/) — checked 2026-10-12. Humane onsite removal and prohibition on public live transport checked.
- [FWC 2026 python removal opportunities](https://myfwc.com/news/all-news/python-challenge-0826/) — checked 2026-10-12. Explicit private-land no hunting-license/no-permit statement checked.
- [FWC current area notices](https://myfwc.com/recreation/notices/) — checked 2026-10-12. Current closure directory checked; notices can change after this data check.
- [FWC Executive Order 23-16](https://myfwc.com/media/31857/eo-23-16.pdf) — checked 2026-10-12. Checked year-round scope, traps/free-bolt prohibition and east/west US27 Fisheating Creek exceptions on page 2.

### Year-round python removal / Burmese python

Dates: 2026-01-01 to 2026-12-31

Bag: No bag limit.

Licenses: No hunting license or removal permit required within the stated scope.

Methods: FWC describes captive-bolt equipment or a lawfully used firearm/PCP air gun for immediate loss of consciousness, followed by pithing as the required second step to prevent recovery. Follow FWC/AVMA training and all property-specific firearm rules.

- Florida anti-cruelty law applies. Humanely kill at the capture location; members of the public may not transport live pythons.
- Obtain appropriate humane-removal training before attempting to handle or euthanize a large constrictor. The linked FWC guidance explains both required steps; the first step alone is insufficient.
- Follow Executive Order 23-16 and specific area access, closures and firearm rules. The annual area list does not override those rules.

Conditions for the whole scope:

- Coverage is restricted to FWC's current 32-area list (the WMA land-type option covers its WMA entries); other public lands are not covered.
- Check the linked FWC area notices for temporary closures; this local dataset does not poll live closures.
- Fisheating Creek uses separate east/west US27 reviewed scopes because EO23-16 imposes special season and permit conditions there.
- EO23-16 prohibits traps and modified/free-bolt captive-bolt stunners. Firearms require authorization under the specific area rules; closed-to-public-access portions remain closed.

## Burmese Python: Rotenberger WMA / Wildlife Management Area (WMA), 2026-2027 expansion

Key: `python-rotenberger-2-2026-2027-expanded`. new draft.

Scope: managed_area: Rotenberger WMA

Review coverage: 2026-07-01 through 2027-06-30.

- [FWC Rotenberger WMA 2026-2027 regulations and map](https://app.myfwc.com/hgm/hgmsearch/wmad?brochureTitle=Rotenberger) — checked 2026-10-12. Interactive brochure checked: area dates, legal species, bag limits, methods, permits, access and exceptions; PDF map available on the same page.
- [FWC hunting licenses and permits](https://myfwc.com/license/recreational/hunting/) — checked 2026-10-12. General license, management-area and season permits; brochure exemptions and area-specific quota restrictions retained.
- [FWC Executive Order 23-16](https://myfwc.com/media/31857/eo-23-16.pdf) — checked 2026-10-12. Page 2: traps and modified/free-bolt captive-bolt stunners prohibited; firearms need specific area authorization.
- [FWC python removal](https://myfwc.com/wildlifehabitats/nonnatives/python/removing/) — checked 2026-10-12. Area-specific removal is subject to the brochure and current FWC orders.
- [FWC humane killing methods](https://myfwc.com/wildlifehabitats/nonnatives/python/humane-killing-methods/) — checked 2026-10-12. Humane onsite killing and required second step; no public live transport.

### Year-round python removal / Burmese python

Dates: 2026-07-01 to 2027-06-30

Bag: No bag limit.

Licenses: No license or removal permit required for non-native reptiles; vehicle/access permits still apply where required.

Methods: Non-firearm removal is allowed year-round subject to access and humane-killing rules. Firearms may be used only during open brochure hunting seasons and only as allowed by that season. Follow the linked FWC humane-killing guidance.

- Entry/exit is limited to the L-4, Powerline, Miami Canal and Manley Ditch levees. Hunting on roads, ramps, parking/camping areas, levees or adjacent powerline pads, and gun hunting on/from/across levees, is prohibited.
- Vehicle, scouting-period and flag requirements apply; airboats are prohibited during archery, muzzleloading and general gun-walk seasons. Do not infer a general gun-vehicle hunt from access text: the 2026-2027 brochure lists none.
- Dogs may not hunt deer or wild hog. Leashed dogs may trail wounded game, subject to the brochure's restrictions.
- When weekend check stations are staffed, check deer at the southeast Holey Land station before quartering, dismembering or removing them.
- EO23-16 prohibits traps and modified/free-bolt captive-bolt stunners; all other area access and equipment restrictions still apply.
- No live python may be removed from the area. Florida anti-cruelty law and FWC humane-killing guidance apply; the required second step prevents recovery after immediate loss of consciousness.
- A year-round python removal opportunity does not open deer/hog/turkey seasons or authorize firearm discharge outside lawful hunting seasons. Follow each season's allowed firearm methods and property closures.
- Python shooting hours are half an hour before sunrise until half an hour after sunset. Report sightings/take through FWC's non-native wildlife reporting service.
- Centerfire rifle take is prohibited beginning March 8, 2027 after small-game season; firearms remain limited to lawful open hunting seasons. Dogs may not take or search for reptiles.

Conditions for the whole scope:

- Hunting over bait, taking swimming deer or spotted fawns, and hunting in posted closed areas are prohibited.
- Ordinary shooting hours are half an hour before sunrise through half an hour after sunset; turkey has separate hours.
- Night gun hunting, fully automatic firearms and centerfire semiautomatic rifles with magazines capable of more than 5 rounds are prohibited.
- Deer hunters and companions need 500 square inches of fluorescent orange above the waist, except bow-and-arrow hunting during archery season.
- Brochure license/permit exemptions include children under 16, Florida residents 65+, residents with a qualifying disabled-person certificate, and qualifying resident military personnel home on leave. They do not override quota permits marked no exemptions or required deer tags. Hunters born on/after June 1, 1975 need hunter-safety certification or the lawful supervised mentoring exception. Youth require adult supervision; mentoring license holders require a licensed supervisor aged 21+. Consult the complete brochure.
- The official brochure includes PDF BROCHURE and PDF MAP ONLY controls. Follow its current maps, access restrictions and FWC closure notices.

## Burmese Python: Rotenberger WMA / Commission-Managed Land, 2026-2027 expansion

Key: `python-rotenberger-3-2026-2027-expanded`. new draft.

Scope: managed_area: Rotenberger WMA

Review coverage: 2026-07-01 through 2027-06-30.

- [FWC Rotenberger WMA 2026-2027 regulations and map](https://app.myfwc.com/hgm/hgmsearch/wmad?brochureTitle=Rotenberger) — checked 2026-10-12. Interactive brochure checked: area dates, legal species, bag limits, methods, permits, access and exceptions; PDF map available on the same page.
- [FWC hunting licenses and permits](https://myfwc.com/license/recreational/hunting/) — checked 2026-10-12. General license, management-area and season permits; brochure exemptions and area-specific quota restrictions retained.
- [FWC Executive Order 23-16](https://myfwc.com/media/31857/eo-23-16.pdf) — checked 2026-10-12. Page 2: traps and modified/free-bolt captive-bolt stunners prohibited; firearms need specific area authorization.
- [FWC python removal](https://myfwc.com/wildlifehabitats/nonnatives/python/removing/) — checked 2026-10-12. Area-specific removal is subject to the brochure and current FWC orders.
- [FWC humane killing methods](https://myfwc.com/wildlifehabitats/nonnatives/python/humane-killing-methods/) — checked 2026-10-12. Humane onsite killing and required second step; no public live transport.

### Year-round python removal / Burmese python

Dates: 2026-07-01 to 2027-06-30

Bag: No bag limit.

Licenses: No license or removal permit required for non-native reptiles; vehicle/access permits still apply where required.

Methods: Non-firearm removal is allowed year-round subject to access and humane-killing rules. Firearms may be used only during open brochure hunting seasons and only as allowed by that season. Follow the linked FWC humane-killing guidance.

- Entry/exit is limited to the L-4, Powerline, Miami Canal and Manley Ditch levees. Hunting on roads, ramps, parking/camping areas, levees or adjacent powerline pads, and gun hunting on/from/across levees, is prohibited.
- Vehicle, scouting-period and flag requirements apply; airboats are prohibited during archery, muzzleloading and general gun-walk seasons. Do not infer a general gun-vehicle hunt from access text: the 2026-2027 brochure lists none.
- Dogs may not hunt deer or wild hog. Leashed dogs may trail wounded game, subject to the brochure's restrictions.
- When weekend check stations are staffed, check deer at the southeast Holey Land station before quartering, dismembering or removing them.
- EO23-16 prohibits traps and modified/free-bolt captive-bolt stunners; all other area access and equipment restrictions still apply.
- No live python may be removed from the area. Florida anti-cruelty law and FWC humane-killing guidance apply; the required second step prevents recovery after immediate loss of consciousness.
- A year-round python removal opportunity does not open deer/hog/turkey seasons or authorize firearm discharge outside lawful hunting seasons. Follow each season's allowed firearm methods and property closures.
- Python shooting hours are half an hour before sunrise until half an hour after sunset. Report sightings/take through FWC's non-native wildlife reporting service.
- Centerfire rifle take is prohibited beginning March 8, 2027 after small-game season; firearms remain limited to lawful open hunting seasons. Dogs may not take or search for reptiles.

Conditions for the whole scope:

- Hunting over bait, taking swimming deer or spotted fawns, and hunting in posted closed areas are prohibited.
- Ordinary shooting hours are half an hour before sunrise through half an hour after sunset; turkey has separate hours.
- Night gun hunting, fully automatic firearms and centerfire semiautomatic rifles with magazines capable of more than 5 rounds are prohibited.
- Deer hunters and companions need 500 square inches of fluorescent orange above the waist, except bow-and-arrow hunting during archery season.
- Brochure license/permit exemptions include children under 16, Florida residents 65+, residents with a qualifying disabled-person certificate, and qualifying resident military personnel home on leave. They do not override quota permits marked no exemptions or required deer tags. Hunters born on/after June 1, 1975 need hunter-safety certification or the lawful supervised mentoring exception. Youth require adult supervision; mentoring license holders require a licensed supervisor aged 21+. Consult the complete brochure.
- The official brochure includes PDF BROCHURE and PDF MAP ONLY controls. Follow its current maps, access restrictions and FWC closure notices.

## Wild Turkey: J. W. Corbett WMA / Wildlife Management Area (WMA), 2026-2027 expansion

Key: `turkey-corbett-2-2026-2027-expanded`. new draft.

Scope: managed_area: J. W. Corbett WMA

Review coverage: 2026-07-01 through 2027-06-30.

- [FWC J. W. Corbett WMA 2026-2027 regulations and map](https://app.myfwc.com/hgm/hgmsearch/wmad?brochureTitle=J.W.+Corbett) — checked 2026-10-12. Interactive brochure checked: area dates, legal species, bag limits, methods, permits, access and exceptions; PDF map available on the same page.
- [FWC hunting licenses and permits](https://myfwc.com/license/recreational/hunting/) — checked 2026-10-12. General license, management-area and season permits; brochure exemptions and area-specific quota restrictions retained.
- [FWC legal resident-game equipment](https://myfwc.com/hunting/regulations/taking-game/) — checked 2026-10-12. Checked broadhead minimum width, species-specific PCP minimums and deer muzzleloader design requirements; area season-method restrictions remain controlling.

### Youth turkey / Gobbler or bearded turkey

Dates: 2027-02-26 to 2027-03-01

Bag: Area daily limit 1 turkey; statewide spring season limit 2, daily 2 and possession 2 also apply. Youth harvest counts toward the spring limit.

Licenses: Hunting license, management area permit and turkey permit unless exempt; annual hunting license for nonresidents. No quota permit required. Hunters under 16 are exempt; participating adults need required licenses/permits unless exempt.

Methods: Bows, crossbows, PCP airguns propelling a bolt or arrow, or centerfire/muzzleloading shotguns with No. 2 or smaller shot. Bruce Bowman remains bows only except qualifying disability permits. Rifles, pistols and PCP bullets are not authorized for this spring turkey hunt.

- Bruce Bowman archery still-hunt area permits bows only, with the brochure's disability crossbow/airbow/draw-lock exceptions. Closed-to-hunting trails, boardwalk, parking and adjacent areas remain closed.
- Centerfire rifles are prohibited south and east of Stumper's Grade; all rifles are prohibited in the Pratt-Whitney buffer and within a quarter mile of the railroad and Mecca Farms.
- Enter/exit at designated entrances; when staffed, report at a check station on entry and departure and check harvested wildlife. No night gun hunting for these species.
- Motorized travel is restricted to named roads and designated access routes. From July 31, 2026 an OHV Hunting Permit is required for allowed off-road hunting vehicle use; airboats, ATVs, tracked vehicles and unregistered motorcycles remain prohibited.
- The area closes August 16 at midnight through August 28 at 8 a.m., with the brochure's limited road, through-hiking and boardwalk exceptions.
- Gobbler or bearded turkey only. Hunting other animals during spring turkey season is prohibited; do not infer firearm permission for other species from the spring turkey dates.
- Turkey shooting hours are half an hour before sunrise until sunset. Hunting roosted turkey or over bait is prohibited.
- Turkey arrows and bolts require broadheads at least 7/8 inch wide. PCP airguns remain limited here to bolts or arrows and must meet the statewide .20-caliber minimum; PCP bullets remain prohibited by this area's spring methods.
- Log turkey before moving it and report to FWC within 24 hours of recovery, in addition to check-station requirements.
- Only Florida resident turkey hunters may hunt March 6-14, 2027; later spring dates also remain limited to Saturdays, Sundays and Wednesdays.
- No fall turkey season is listed for Corbett; do not apply private-land fall seasons to this area.
- Only youth under 16 may harvest, under direct physical supervision by an adult aged 18+. Properly licensed adults may assist in the youth's presence but may not harvest.

### Spring turkey / Gobbler or bearded turkey

Dates: 2027-03-06 to 2027-04-11 (Wednesday, Saturday, Sunday only)

Bag: Area daily limit 1 turkey; statewide spring season limit 2, daily 2 and possession 2 also apply. Youth harvest counts toward the spring limit.

Licenses: Hunting license, management area permit and turkey permit unless exempt; annual hunting license for nonresidents. No quota permit required.

Methods: Bows, crossbows, PCP airguns propelling a bolt or arrow, or centerfire/muzzleloading shotguns with No. 2 or smaller shot. Bruce Bowman remains bows only except qualifying disability permits. Rifles, pistols and PCP bullets are not authorized for this spring turkey hunt.

- Bruce Bowman archery still-hunt area permits bows only, with the brochure's disability crossbow/airbow/draw-lock exceptions. Closed-to-hunting trails, boardwalk, parking and adjacent areas remain closed.
- Centerfire rifles are prohibited south and east of Stumper's Grade; all rifles are prohibited in the Pratt-Whitney buffer and within a quarter mile of the railroad and Mecca Farms.
- Enter/exit at designated entrances; when staffed, report at a check station on entry and departure and check harvested wildlife. No night gun hunting for these species.
- Motorized travel is restricted to named roads and designated access routes. From July 31, 2026 an OHV Hunting Permit is required for allowed off-road hunting vehicle use; airboats, ATVs, tracked vehicles and unregistered motorcycles remain prohibited.
- The area closes August 16 at midnight through August 28 at 8 a.m., with the brochure's limited road, through-hiking and boardwalk exceptions.
- Gobbler or bearded turkey only. Hunting other animals during spring turkey season is prohibited; do not infer firearm permission for other species from the spring turkey dates.
- Turkey shooting hours are half an hour before sunrise until sunset. Hunting roosted turkey or over bait is prohibited.
- Turkey arrows and bolts require broadheads at least 7/8 inch wide. PCP airguns remain limited here to bolts or arrows and must meet the statewide .20-caliber minimum; PCP bullets remain prohibited by this area's spring methods.
- Log turkey before moving it and report to FWC within 24 hours of recovery, in addition to check-station requirements.
- Only Florida resident turkey hunters may hunt March 6-14, 2027; later spring dates also remain limited to Saturdays, Sundays and Wednesdays.
- No fall turkey season is listed for Corbett; do not apply private-land fall seasons to this area.

Conditions for the whole scope:

- Hunting over bait, taking swimming deer or spotted fawns, and hunting in posted closed areas are prohibited.
- Ordinary shooting hours are half an hour before sunrise through half an hour after sunset; turkey has separate hours.
- Night gun hunting, fully automatic firearms and centerfire semiautomatic rifles with magazines capable of more than 5 rounds are prohibited.
- Deer hunters and companions need 500 square inches of fluorescent orange above the waist, except bow-and-arrow hunting during archery season.
- Brochure license/permit exemptions include children under 16, Florida residents 65+, residents with a qualifying disabled-person certificate, and qualifying resident military personnel home on leave. They do not override quota permits marked no exemptions or required deer tags. Hunters born on/after June 1, 1975 need hunter-safety certification or the lawful supervised mentoring exception. Youth require adult supervision; mentoring license holders require a licensed supervisor aged 21+. Consult the complete brochure.
- The official brochure includes PDF BROCHURE and PDF MAP ONLY controls. Follow its current maps, access restrictions and FWC closure notices.

## Wild Turkey: J. W. Corbett WMA / Commission-Managed Land, 2026-2027 expansion

Key: `turkey-corbett-3-2026-2027-expanded`. new draft.

Scope: managed_area: J. W. Corbett WMA

Review coverage: 2026-07-01 through 2027-06-30.

- [FWC J. W. Corbett WMA 2026-2027 regulations and map](https://app.myfwc.com/hgm/hgmsearch/wmad?brochureTitle=J.W.+Corbett) — checked 2026-10-12. Interactive brochure checked: area dates, legal species, bag limits, methods, permits, access and exceptions; PDF map available on the same page.
- [FWC hunting licenses and permits](https://myfwc.com/license/recreational/hunting/) — checked 2026-10-12. General license, management-area and season permits; brochure exemptions and area-specific quota restrictions retained.
- [FWC legal resident-game equipment](https://myfwc.com/hunting/regulations/taking-game/) — checked 2026-10-12. Checked broadhead minimum width, species-specific PCP minimums and deer muzzleloader design requirements; area season-method restrictions remain controlling.

### Youth turkey / Gobbler or bearded turkey

Dates: 2027-02-26 to 2027-03-01

Bag: Area daily limit 1 turkey; statewide spring season limit 2, daily 2 and possession 2 also apply. Youth harvest counts toward the spring limit.

Licenses: Hunting license, management area permit and turkey permit unless exempt; annual hunting license for nonresidents. No quota permit required. Hunters under 16 are exempt; participating adults need required licenses/permits unless exempt.

Methods: Bows, crossbows, PCP airguns propelling a bolt or arrow, or centerfire/muzzleloading shotguns with No. 2 or smaller shot. Bruce Bowman remains bows only except qualifying disability permits. Rifles, pistols and PCP bullets are not authorized for this spring turkey hunt.

- Bruce Bowman archery still-hunt area permits bows only, with the brochure's disability crossbow/airbow/draw-lock exceptions. Closed-to-hunting trails, boardwalk, parking and adjacent areas remain closed.
- Centerfire rifles are prohibited south and east of Stumper's Grade; all rifles are prohibited in the Pratt-Whitney buffer and within a quarter mile of the railroad and Mecca Farms.
- Enter/exit at designated entrances; when staffed, report at a check station on entry and departure and check harvested wildlife. No night gun hunting for these species.
- Motorized travel is restricted to named roads and designated access routes. From July 31, 2026 an OHV Hunting Permit is required for allowed off-road hunting vehicle use; airboats, ATVs, tracked vehicles and unregistered motorcycles remain prohibited.
- The area closes August 16 at midnight through August 28 at 8 a.m., with the brochure's limited road, through-hiking and boardwalk exceptions.
- Gobbler or bearded turkey only. Hunting other animals during spring turkey season is prohibited; do not infer firearm permission for other species from the spring turkey dates.
- Turkey shooting hours are half an hour before sunrise until sunset. Hunting roosted turkey or over bait is prohibited.
- Turkey arrows and bolts require broadheads at least 7/8 inch wide. PCP airguns remain limited here to bolts or arrows and must meet the statewide .20-caliber minimum; PCP bullets remain prohibited by this area's spring methods.
- Log turkey before moving it and report to FWC within 24 hours of recovery, in addition to check-station requirements.
- Only Florida resident turkey hunters may hunt March 6-14, 2027; later spring dates also remain limited to Saturdays, Sundays and Wednesdays.
- No fall turkey season is listed for Corbett; do not apply private-land fall seasons to this area.
- Only youth under 16 may harvest, under direct physical supervision by an adult aged 18+. Properly licensed adults may assist in the youth's presence but may not harvest.

### Spring turkey / Gobbler or bearded turkey

Dates: 2027-03-06 to 2027-04-11 (Wednesday, Saturday, Sunday only)

Bag: Area daily limit 1 turkey; statewide spring season limit 2, daily 2 and possession 2 also apply. Youth harvest counts toward the spring limit.

Licenses: Hunting license, management area permit and turkey permit unless exempt; annual hunting license for nonresidents. No quota permit required.

Methods: Bows, crossbows, PCP airguns propelling a bolt or arrow, or centerfire/muzzleloading shotguns with No. 2 or smaller shot. Bruce Bowman remains bows only except qualifying disability permits. Rifles, pistols and PCP bullets are not authorized for this spring turkey hunt.

- Bruce Bowman archery still-hunt area permits bows only, with the brochure's disability crossbow/airbow/draw-lock exceptions. Closed-to-hunting trails, boardwalk, parking and adjacent areas remain closed.
- Centerfire rifles are prohibited south and east of Stumper's Grade; all rifles are prohibited in the Pratt-Whitney buffer and within a quarter mile of the railroad and Mecca Farms.
- Enter/exit at designated entrances; when staffed, report at a check station on entry and departure and check harvested wildlife. No night gun hunting for these species.
- Motorized travel is restricted to named roads and designated access routes. From July 31, 2026 an OHV Hunting Permit is required for allowed off-road hunting vehicle use; airboats, ATVs, tracked vehicles and unregistered motorcycles remain prohibited.
- The area closes August 16 at midnight through August 28 at 8 a.m., with the brochure's limited road, through-hiking and boardwalk exceptions.
- Gobbler or bearded turkey only. Hunting other animals during spring turkey season is prohibited; do not infer firearm permission for other species from the spring turkey dates.
- Turkey shooting hours are half an hour before sunrise until sunset. Hunting roosted turkey or over bait is prohibited.
- Turkey arrows and bolts require broadheads at least 7/8 inch wide. PCP airguns remain limited here to bolts or arrows and must meet the statewide .20-caliber minimum; PCP bullets remain prohibited by this area's spring methods.
- Log turkey before moving it and report to FWC within 24 hours of recovery, in addition to check-station requirements.
- Only Florida resident turkey hunters may hunt March 6-14, 2027; later spring dates also remain limited to Saturdays, Sundays and Wednesdays.
- No fall turkey season is listed for Corbett; do not apply private-land fall seasons to this area.

Conditions for the whole scope:

- Hunting over bait, taking swimming deer or spotted fawns, and hunting in posted closed areas are prohibited.
- Ordinary shooting hours are half an hour before sunrise through half an hour after sunset; turkey has separate hours.
- Night gun hunting, fully automatic firearms and centerfire semiautomatic rifles with magazines capable of more than 5 rounds are prohibited.
- Deer hunters and companions need 500 square inches of fluorescent orange above the waist, except bow-and-arrow hunting during archery season.
- Brochure license/permit exemptions include children under 16, Florida residents 65+, residents with a qualifying disabled-person certificate, and qualifying resident military personnel home on leave. They do not override quota permits marked no exemptions or required deer tags. Hunters born on/after June 1, 1975 need hunter-safety certification or the lawful supervised mentoring exception. Youth require adult supervision; mentoring license holders require a licensed supervisor aged 21+. Consult the complete brochure.
- The official brochure includes PDF BROCHURE and PDF MAP ONLY controls. Follow its current maps, access restrictions and FWC closure notices.

## Wild Turkey: Dinner Island Ranch / Wildlife Management Area (WMA), 2026-2027

Key: `turkey-dinner-island-2-2026-2027`. new draft.

Scope: managed_area: Dinner Island Ranch WMA

Review coverage: 2026-07-01 through 2027-06-30.

- [FWC Dinner Island Ranch 2026-2027 area brochure](https://app.myfwc.com/hgm/hgmsearch/wmad?brochureTitle=Dinner+Island+Ranch) — checked 2026-10-12. Read complete interactive brochure: season dates, antlered-only deer, quota/shared bags, turkey restrictions, hog methods, access and check-station waiver.
- [FWC Dinner Island Ranch 2026-2027 hunt calendar](https://app.myfwc.com/hsc/wmahuntcalendar/?areaName=dinner+island+ranch) — checked 2026-10-12. Corroborated every archery, muzzleloading, family, general gun, small-game and youth/spring turkey endpoint; Caracara Unit excluded.
- [FWC hunting licenses and permits](https://myfwc.com/license/recreational/hunting/) — checked 2026-10-12. Species/season permits and individual exemptions are separate from no-exemption area quota permits.
- [FWC taking game methods](https://myfwc.com/hunting/regulations/taking-game/) — checked 2026-10-12. Deer muzzleloader minimum .30-caliber single bullet/20-gauge multiple balls and deer/turkey 7/8-inch broadheads checked; area-specific stricter methods retained.

### Dinner Island Ranch youth turkey / Gobbler or bearded turkey; youth only

Dates: 2027-02-26 to 2027-03-01

Bag: 1 gobbler or bearded turkey per youth or spring turkey quota permit, shared with any permitted guest. Statewide spring daily 2, possession 2 and season 2 limits also apply; youth-weekend harvest counts toward the spring season limit.

Licenses: Eligible youth under 16 do not need a hunting license or season permits. A youth turkey quota permit is required, with no quota exemptions. Supervising adults participating in the hunt need the applicable licenses/permits unless exempt, and may not harvest turkey.

Methods: Bows, crossbows, PCP airguns propelling a bolt or arrow, or shotguns using No. 2 or smaller shot. Rifles, pistols and PCP airguns propelling bullets are prohibited for turkey. No shooting a turkey on its roost; shooting hours are half an hour before sunrise through sunset.

- Only youth under 16 may harvest during this hunt, under direct physical supervision of an adult at least 18. An adult may assist in the youth's presence but may not harvest.
- Turkey arrows and bolts require broadheads at least 7/8 inch wide. The area's PCP bolt/arrow-only restriction still applies; statewide PCP bullet guidance does not authorize bullets here.
- Quota permits are nontransferable and require positive identification except for youth. Where a guest permit is allowed, one guest and the host must enter/exit together, share a street-legal vehicle and hunt with the host present. Deer and turkey limits are shared per quota permit.

### Dinner Island Ranch spring turkey / Gobbler or bearded turkey only

Dates: 2027-03-06 to 2027-03-08; 2027-03-13 to 2027-03-15; 2027-04-03 to 2027-04-05

Bag: 1 gobbler or bearded turkey per youth or spring turkey quota permit, shared with any permitted guest. Statewide spring daily 2, possession 2 and season 2 limits also apply; youth-weekend harvest counts toward the spring season limit.

Licenses: Hunting license, management area permit and turkey permit required unless exempt. A quota permit for this area and hunt is required; no quota exemptions.

Methods: Bows, crossbows, PCP airguns propelling a bolt or arrow, or shotguns using No. 2 or smaller shot. Rifles, pistols and PCP airguns propelling bullets are prohibited for turkey. No shooting a turkey on its roost; shooting hours are half an hour before sunrise through sunset.

- Turkey arrows and bolts require broadheads at least 7/8 inch wide. The area's PCP bolt/arrow-only restriction still applies; statewide PCP bullet guidance does not authorize bullets here.
- Quota permits are nontransferable and require positive identification except for youth. Where a guest permit is allowed, one guest and the host must enter/exit together, share a street-legal vehicle and hunt with the host present. Deer and turkey limits are shared per quota permit.

Conditions for the whole scope:

- Dinner Island Ranch coverage excludes the separately regulated Caracara Unit. Enter and exit at the designated entrance; posted closed areas remain closed.
- The 2026-2027 Attention Hunters notice says there is no operating check station and waives all check-station duties. Deer and turkey must still be logged before moving and officially reported within 24 hours. HuntIt does not submit the FWC report.
- Vehicles may use named and numbered roads only, except valid Alternative Mobility Permit allowances. Vehicles are prohibited from 1.5 hours after sunset until 1.5 hours before sunrise, except camping-permit holders and guests accessing their designated campsite.
- Airboats, ATVs, swamp buggies, tracked vehicles and unregistered motorcycles are prohibited, except quota hunters and their guest permit holders may use ATVs and swamp buggies on named/numbered roads during their permitted archery, muzzleloading gun, family or general gun hunt. This exception does not authorize off-road travel.
- Camping requires an FWC permit and is limited to designated campgrounds. Horses are prohibited during archery, muzzleloading gun, family, general gun and spring turkey seasons; otherwise use designated roads.
- On posted dove fields, hunting during dove season is limited to Saturdays; otherwise only hunting allowed by the applicable area season is authorized. Check the brochure map and current closures before selecting a hunting site.
- No hunting over bait, night gun hunting, fully automatic firearms or centerfire semiautomatic rifles with magazines holding more than 5 rounds. The brochure's ammunition, equipment and closed-area restrictions apply.
- Ordinary shooting hours are half an hour before sunrise through half an hour after sunset. Turkey shooting ends at sunset.
- Dogs may not hunt deer, wild hog or furbearers; leashed dogs may trail wounded game under the brochure's conditions. No dogs may pursue non-native reptiles.
- License/season-permit exemptions do not waive a quota permit marked no exemptions. Check hunter-safety requirements and individual exemptions in the full brochure.
- Nonresident hunters taking native game need the applicable annual hunting license unless exempt. A hunting license is not required when hunting wild hog or removing python within the stated exception.
- Turkey hunting is authorized only during the listed youth/spring hunts; no fall turkey season is authorized here.
- Log turkey before moving and officially report to FWC within 24 hours or before an earlier processing, transfer or out-of-state deadline.

## Wild Turkey: Dinner Island Ranch / Commission-Managed Land, 2026-2027

Key: `turkey-dinner-island-3-2026-2027`. new draft.

Scope: managed_area: Dinner Island Ranch WMA

Review coverage: 2026-07-01 through 2027-06-30.

- [FWC Dinner Island Ranch 2026-2027 area brochure](https://app.myfwc.com/hgm/hgmsearch/wmad?brochureTitle=Dinner+Island+Ranch) — checked 2026-10-12. Read complete interactive brochure: season dates, antlered-only deer, quota/shared bags, turkey restrictions, hog methods, access and check-station waiver.
- [FWC Dinner Island Ranch 2026-2027 hunt calendar](https://app.myfwc.com/hsc/wmahuntcalendar/?areaName=dinner+island+ranch) — checked 2026-10-12. Corroborated every archery, muzzleloading, family, general gun, small-game and youth/spring turkey endpoint; Caracara Unit excluded.
- [FWC hunting licenses and permits](https://myfwc.com/license/recreational/hunting/) — checked 2026-10-12. Species/season permits and individual exemptions are separate from no-exemption area quota permits.
- [FWC taking game methods](https://myfwc.com/hunting/regulations/taking-game/) — checked 2026-10-12. Deer muzzleloader minimum .30-caliber single bullet/20-gauge multiple balls and deer/turkey 7/8-inch broadheads checked; area-specific stricter methods retained.

### Dinner Island Ranch youth turkey / Gobbler or bearded turkey; youth only

Dates: 2027-02-26 to 2027-03-01

Bag: 1 gobbler or bearded turkey per youth or spring turkey quota permit, shared with any permitted guest. Statewide spring daily 2, possession 2 and season 2 limits also apply; youth-weekend harvest counts toward the spring season limit.

Licenses: Eligible youth under 16 do not need a hunting license or season permits. A youth turkey quota permit is required, with no quota exemptions. Supervising adults participating in the hunt need the applicable licenses/permits unless exempt, and may not harvest turkey.

Methods: Bows, crossbows, PCP airguns propelling a bolt or arrow, or shotguns using No. 2 or smaller shot. Rifles, pistols and PCP airguns propelling bullets are prohibited for turkey. No shooting a turkey on its roost; shooting hours are half an hour before sunrise through sunset.

- Only youth under 16 may harvest during this hunt, under direct physical supervision of an adult at least 18. An adult may assist in the youth's presence but may not harvest.
- Turkey arrows and bolts require broadheads at least 7/8 inch wide. The area's PCP bolt/arrow-only restriction still applies; statewide PCP bullet guidance does not authorize bullets here.
- Quota permits are nontransferable and require positive identification except for youth. Where a guest permit is allowed, one guest and the host must enter/exit together, share a street-legal vehicle and hunt with the host present. Deer and turkey limits are shared per quota permit.

### Dinner Island Ranch spring turkey / Gobbler or bearded turkey only

Dates: 2027-03-06 to 2027-03-08; 2027-03-13 to 2027-03-15; 2027-04-03 to 2027-04-05

Bag: 1 gobbler or bearded turkey per youth or spring turkey quota permit, shared with any permitted guest. Statewide spring daily 2, possession 2 and season 2 limits also apply; youth-weekend harvest counts toward the spring season limit.

Licenses: Hunting license, management area permit and turkey permit required unless exempt. A quota permit for this area and hunt is required; no quota exemptions.

Methods: Bows, crossbows, PCP airguns propelling a bolt or arrow, or shotguns using No. 2 or smaller shot. Rifles, pistols and PCP airguns propelling bullets are prohibited for turkey. No shooting a turkey on its roost; shooting hours are half an hour before sunrise through sunset.

- Turkey arrows and bolts require broadheads at least 7/8 inch wide. The area's PCP bolt/arrow-only restriction still applies; statewide PCP bullet guidance does not authorize bullets here.
- Quota permits are nontransferable and require positive identification except for youth. Where a guest permit is allowed, one guest and the host must enter/exit together, share a street-legal vehicle and hunt with the host present. Deer and turkey limits are shared per quota permit.

Conditions for the whole scope:

- Dinner Island Ranch coverage excludes the separately regulated Caracara Unit. Enter and exit at the designated entrance; posted closed areas remain closed.
- The 2026-2027 Attention Hunters notice says there is no operating check station and waives all check-station duties. Deer and turkey must still be logged before moving and officially reported within 24 hours. HuntIt does not submit the FWC report.
- Vehicles may use named and numbered roads only, except valid Alternative Mobility Permit allowances. Vehicles are prohibited from 1.5 hours after sunset until 1.5 hours before sunrise, except camping-permit holders and guests accessing their designated campsite.
- Airboats, ATVs, swamp buggies, tracked vehicles and unregistered motorcycles are prohibited, except quota hunters and their guest permit holders may use ATVs and swamp buggies on named/numbered roads during their permitted archery, muzzleloading gun, family or general gun hunt. This exception does not authorize off-road travel.
- Camping requires an FWC permit and is limited to designated campgrounds. Horses are prohibited during archery, muzzleloading gun, family, general gun and spring turkey seasons; otherwise use designated roads.
- On posted dove fields, hunting during dove season is limited to Saturdays; otherwise only hunting allowed by the applicable area season is authorized. Check the brochure map and current closures before selecting a hunting site.
- No hunting over bait, night gun hunting, fully automatic firearms or centerfire semiautomatic rifles with magazines holding more than 5 rounds. The brochure's ammunition, equipment and closed-area restrictions apply.
- Ordinary shooting hours are half an hour before sunrise through half an hour after sunset. Turkey shooting ends at sunset.
- Dogs may not hunt deer, wild hog or furbearers; leashed dogs may trail wounded game under the brochure's conditions. No dogs may pursue non-native reptiles.
- License/season-permit exemptions do not waive a quota permit marked no exemptions. Check hunter-safety requirements and individual exemptions in the full brochure.
- Nonresident hunters taking native game need the applicable annual hunting license unless exempt. A hunting license is not required when hunting wild hog or removing python within the stated exception.
- Turkey hunting is authorized only during the listed youth/spring hunts; no fall turkey season is authorized here.
- Log turkey before moving and officially report to FWC within 24 hours or before an earlier processing, transfer or out-of-state deadline.

## Wild Turkey: Holey Land WMA / Wildlife Management Area (WMA), 2026-2027 expansion

Key: `turkey-holey-land-2-2026-2027-expanded`. new draft.

Scope: managed_area: Holey Land WMA

Review coverage: 2026-07-01 through 2027-06-30.

- [FWC Holey Land WMA 2026-2027 regulations and map](https://app.myfwc.com/hgm/hgmsearch/wmad?brochureTitle=Holey+Land) — checked 2026-10-12. Interactive brochure checked: area dates, legal species, bag limits, methods, permits, access and exceptions; PDF map available on the same page.
- [FWC hunting licenses and permits](https://myfwc.com/license/recreational/hunting/) — checked 2026-10-12. General license, management-area and season permits; brochure exemptions and area-specific quota restrictions retained.

### Turkey take prohibited / Turkey take prohibited

Dates: 2026-07-01 to 2027-06-30

Bag: No turkey may be taken.

Licenses: No license or permit authorizes turkey take in this area.

Methods: Turkey hunting/take is prohibited by the area brochure.

**Explicit prohibition. Search must remain closed throughout these dates.**

- The area brochure expressly prohibits turkey. Private-land turkey dates and permits do not override this prohibition.

Conditions for the whole scope:

- Hunting over bait, taking swimming deer or spotted fawns, and hunting in posted closed areas are prohibited.
- Ordinary shooting hours are half an hour before sunrise through half an hour after sunset; turkey has separate hours.
- Night gun hunting, fully automatic firearms and centerfire semiautomatic rifles with magazines capable of more than 5 rounds are prohibited.
- Deer hunters and companions need 500 square inches of fluorescent orange above the waist, except bow-and-arrow hunting during archery season.
- Brochure license/permit exemptions include children under 16, Florida residents 65+, residents with a qualifying disabled-person certificate, and qualifying resident military personnel home on leave. They do not override quota permits marked no exemptions or required deer tags. Hunters born on/after June 1, 1975 need hunter-safety certification or the lawful supervised mentoring exception. Youth require adult supervision; mentoring license holders require a licensed supervisor aged 21+. Consult the complete brochure.
- The official brochure includes PDF BROCHURE and PDF MAP ONLY controls. Follow its current maps, access restrictions and FWC closure notices.

## Wild Turkey: Holey Land WMA / Commission-Managed Land, 2026-2027 expansion

Key: `turkey-holey-land-3-2026-2027-expanded`. new draft.

Scope: managed_area: Holey Land WMA

Review coverage: 2026-07-01 through 2027-06-30.

- [FWC Holey Land WMA 2026-2027 regulations and map](https://app.myfwc.com/hgm/hgmsearch/wmad?brochureTitle=Holey+Land) — checked 2026-10-12. Interactive brochure checked: area dates, legal species, bag limits, methods, permits, access and exceptions; PDF map available on the same page.
- [FWC hunting licenses and permits](https://myfwc.com/license/recreational/hunting/) — checked 2026-10-12. General license, management-area and season permits; brochure exemptions and area-specific quota restrictions retained.

### Turkey take prohibited / Turkey take prohibited

Dates: 2026-07-01 to 2027-06-30

Bag: No turkey may be taken.

Licenses: No license or permit authorizes turkey take in this area.

Methods: Turkey hunting/take is prohibited by the area brochure.

**Explicit prohibition. Search must remain closed throughout these dates.**

- The area brochure expressly prohibits turkey. Private-land turkey dates and permits do not override this prohibition.

Conditions for the whole scope:

- Hunting over bait, taking swimming deer or spotted fawns, and hunting in posted closed areas are prohibited.
- Ordinary shooting hours are half an hour before sunrise through half an hour after sunset; turkey has separate hours.
- Night gun hunting, fully automatic firearms and centerfire semiautomatic rifles with magazines capable of more than 5 rounds are prohibited.
- Deer hunters and companions need 500 square inches of fluorescent orange above the waist, except bow-and-arrow hunting during archery season.
- Brochure license/permit exemptions include children under 16, Florida residents 65+, residents with a qualifying disabled-person certificate, and qualifying resident military personnel home on leave. They do not override quota permits marked no exemptions or required deer tags. Hunters born on/after June 1, 1975 need hunter-safety certification or the lawful supervised mentoring exception. Youth require adult supervision; mentoring license holders require a licensed supervisor aged 21+. Consult the complete brochure.
- The official brochure includes PDF BROCHURE and PDF MAP ONLY controls. Follow its current maps, access restrictions and FWC closure notices.

## Wild turkey: private land, fall a, 2026–2027

Key: `turkey-private-fall-a-2026-2027`. new draft.

Scope: zone: A

Review coverage: 2026-07-01 through 2027-01-31.

- [FWC 2026–2027 turkey seasons and limits](https://myfwc.com/hunting/season-dates/) — checked 2026-10-12. Checked zone fall dates, SR70 spring dates, lawful categories, methods and combined season limits; WMA schedules excluded.
- [FWC hunting licenses and permits](https://myfwc.com/license/recreational/hunting/) — checked 2026-10-12. Checked hunting license, Turkey Permit and season-specific permits.
- [FWC license exemptions](https://myfwc.com/license/recreational/do-i-need-one/) — checked 2026-10-12. Checked age, residency and conditional exemptions; access and hunting restrictions remain separate.
- [FWC general hunting information](https://myfwc.com/hunting/regulations/general-information/) — checked 2026-10-12. Checked private-land permission, fall/spring shooting hours, carcass evidence and transfer labeling.
- [FWC legal and prohibited methods](https://myfwc.com/hunting/regulations/taking-game/) — checked 2026-10-12. Checked equipment thresholds, dogs/roost/feed restrictions and closed locations.
- [FWC deer and wild turkey harvest reporting](https://myfwc.com/hunting/deer/harvest-report/) — checked 2026-10-12. Checked log-before-move duty, earliest reporting deadline and confirmation number.
- [FWC 2027 youth turkey hunts](https://myfwc.com/hunting/get-started/youth-turkey-hunting/) — checked 2026-10-12. Checked all four days of each regional youth hunt, age/supervision, adult participation and youth season-limit counting.
- [FWC wild turkey species profile](https://myfwc.com/wildlifehabitats/profiles/birds/game-birds/wild-turkeys/) — checked 2026-10-12. Checked Florida subspecies, appearance, habitat, flocking, feeding and tree roosts.
- [FWC how to hunt wild turkeys](https://myfwc.com/hunting/turkey/get-started/) — checked 2026-10-12. Checked scouting and patience guidance; links provide safe calling and shooting instruction.

### Turkey archery season / Gobblers and bearded turkeys only

Dates: 2026-08-01 to 2026-08-30

Bag: Daily limit 2; possession and season limit 2 for all fall seasons combined.

Licenses: Hunting license and Turkey Permit required unless individually exempt. Archery season permit required unless exempt.

Methods: Bows only.

- Shooting hours on private land: one-half hour before sunrise to one-half hour after sunset during fall hunts.
- Turkey arrows/bolts need broadheads at least 7/8 inch wide. Turkey PCP equipment must meet FWC's minimum .20-caliber projectile requirement. Non-PCP air guns are prohibited for turkey. Centerfire semiautomatic rifle magazines cannot exceed five rounds; fully automatic firearms are prohibited.
- Do not hunt turkeys with dogs, shoot a roosted turkey or hunt within 100 yards of a feeding station while feed is present. Live decoys, recorded game calls, artificial lights, traps and other prohibited methods are not authorized. Road rights-of-way, occupied premises, local discharge restrictions and private-property boundaries still apply.
- Log every turkey before moving it. Report to FWC within 24 hours or before final processing, transfer to a processor/taxidermist or leaving Florida, whichever is first; retain the confirmation number. HuntIt's personal harvest record does not submit an FWC report.
- Retain the head and beard, when applicable, and required hunter identification as evidence of legal harvest. After official reporting, transferred carcasses/parts require the hunter's name, address and harvest confirmation number; retain traceability and sex identification under FWC's processing/transport rules.

### Turkey crossbow season / Gobblers and bearded turkeys only

Dates: 2026-08-01 to 2026-09-04

Bag: Daily limit 2; possession and season limit 2 for all fall seasons combined.

Licenses: Hunting license and Turkey Permit required unless individually exempt. Crossbow season permit required unless exempt.

Methods: Crossbows, bows and airbows.

- Shooting hours on private land: one-half hour before sunrise to one-half hour after sunset during fall hunts.
- Turkey arrows/bolts need broadheads at least 7/8 inch wide. Turkey PCP equipment must meet FWC's minimum .20-caliber projectile requirement. Non-PCP air guns are prohibited for turkey. Centerfire semiautomatic rifle magazines cannot exceed five rounds; fully automatic firearms are prohibited.
- Do not hunt turkeys with dogs, shoot a roosted turkey or hunt within 100 yards of a feeding station while feed is present. Live decoys, recorded game calls, artificial lights, traps and other prohibited methods are not authorized. Road rights-of-way, occupied premises, local discharge restrictions and private-property boundaries still apply.
- Log every turkey before moving it. Report to FWC within 24 hours or before final processing, transfer to a processor/taxidermist or leaving Florida, whichever is first; retain the confirmation number. HuntIt's personal harvest record does not submit an FWC report.
- Retain the head and beard, when applicable, and required hunter identification as evidence of legal harvest. After official reporting, transferred carcasses/parts require the hunter's name, address and harvest confirmation number; retain traceability and sex identification under FWC's processing/transport rules.

### Turkey muzzleloading gun season / Gobblers and bearded turkeys only

Dates: 2026-09-05 to 2026-09-18

Bag: Daily limit 2; possession and season limit 2 for all fall seasons combined.

Licenses: Hunting license and Turkey Permit required unless individually exempt. Muzzleloading gun season permit required unless exempt.

Methods: Muzzleloaders, crossbows, bows and airbows. Muzzleloading projectiles must load through the muzzle; ignition must use wheel lock, flintlock, percussion cap or centerfire primer (including 209). Powder may load at the breech.

- Shooting hours on private land: one-half hour before sunrise to one-half hour after sunset during fall hunts.
- Turkey arrows/bolts need broadheads at least 7/8 inch wide. Turkey PCP equipment must meet FWC's minimum .20-caliber projectile requirement. Non-PCP air guns are prohibited for turkey. Centerfire semiautomatic rifle magazines cannot exceed five rounds; fully automatic firearms are prohibited.
- Do not hunt turkeys with dogs, shoot a roosted turkey or hunt within 100 yards of a feeding station while feed is present. Live decoys, recorded game calls, artificial lights, traps and other prohibited methods are not authorized. Road rights-of-way, occupied premises, local discharge restrictions and private-property boundaries still apply.
- Log every turkey before moving it. Report to FWC within 24 hours or before final processing, transfer to a processor/taxidermist or leaving Florida, whichever is first; retain the confirmation number. HuntIt's personal harvest record does not submit an FWC report.
- Retain the head and beard, when applicable, and required hunter identification as evidence of legal harvest. After official reporting, transferred carcasses/parts require the hunter's name, address and harvest confirmation number; retain traceability and sex identification under FWC's processing/transport rules.

### Fall turkey season / Gobblers and bearded turkeys only

Dates: 2026-10-05 to 2026-10-18; 2026-11-21 to 2027-01-03

Bag: Daily limit 2; possession and season limit 2 for all fall seasons combined.

Licenses: Hunting license and Turkey Permit required unless individually exempt.

Methods: Shotguns, rifles, handguns, muzzleloaders, crossbows, bows and lawful pre-charged pneumatic (PCP) air guns.

- Shooting hours on private land: one-half hour before sunrise to one-half hour after sunset during fall hunts.
- Turkey arrows/bolts need broadheads at least 7/8 inch wide. Turkey PCP equipment must meet FWC's minimum .20-caliber projectile requirement. Non-PCP air guns are prohibited for turkey. Centerfire semiautomatic rifle magazines cannot exceed five rounds; fully automatic firearms are prohibited.
- Do not hunt turkeys with dogs, shoot a roosted turkey or hunt within 100 yards of a feeding station while feed is present. Live decoys, recorded game calls, artificial lights, traps and other prohibited methods are not authorized. Road rights-of-way, occupied premises, local discharge restrictions and private-property boundaries still apply.
- Log every turkey before moving it. Report to FWC within 24 hours or before final processing, transfer to a processor/taxidermist or leaving Florida, whichever is first; retain the confirmation number. HuntIt's personal harvest record does not submit an FWC report.
- Retain the head and beard, when applicable, and required hunter identification as evidence of legal harvest. After official reporting, transferred carcasses/parts require the hunter's name, address and harvest confirmation number; retain traceability and sex identification under FWC's processing/transport rules.

Conditions for the whole scope:

- Private lands outside the WMA system only; obtain landowner permission. WMA dates, quotas and shooting hours require the specific area brochure.
- License/permit exemptions require the relevant proof and conditions: youth under 16; Florida residents age 65+; qualifying homestead hunting in the county of residence; Florida residents holding the qualifying disability license; qualifying resident military members home on leave for at most 30 days with orders; authorized military/disabled-veteran events; and qualifying licensed-preserve patrons. Check the official exemption page. An exemption does not change season dates, bag limits, access permission or harvest reporting.
- The date bounds describe this edition's reviewed coverage; future seasons require new source review.

Proposed completion of blank species fields:

- scientific_name: Meleagris gallopavo
- description: Florida supports eastern and Osceola wild turkey subspecies. These large birds have long legs and broad tails; males commonly have a breast beard.
- habitat: Open woodland, forest edges and clearings across suitable Florida habitat; Osceola turkeys occur in peninsular Florida.
- behavior: Turkeys forage mainly on the ground, form flocks and roost in trees at night. They are wary and can fly rapidly over short distances.
- hunting_strategy: Scout the hunting area beforehand, learn where turkeys travel and remain patient. Follow FWC's safe-hunting and calling guidance and positively identify the legal bird and a safe shooting direction.

## Wild turkey: private land, fall b, 2026–2027

Key: `turkey-private-fall-b-2026-2027`. new draft.

Scope: zone: B

Review coverage: 2026-07-01 through 2027-01-31.

- [FWC 2026–2027 turkey seasons and limits](https://myfwc.com/hunting/season-dates/) — checked 2026-10-12. Checked zone fall dates, SR70 spring dates, lawful categories, methods and combined season limits; WMA schedules excluded.
- [FWC hunting licenses and permits](https://myfwc.com/license/recreational/hunting/) — checked 2026-10-12. Checked hunting license, Turkey Permit and season-specific permits.
- [FWC license exemptions](https://myfwc.com/license/recreational/do-i-need-one/) — checked 2026-10-12. Checked age, residency and conditional exemptions; access and hunting restrictions remain separate.
- [FWC general hunting information](https://myfwc.com/hunting/regulations/general-information/) — checked 2026-10-12. Checked private-land permission, fall/spring shooting hours, carcass evidence and transfer labeling.
- [FWC legal and prohibited methods](https://myfwc.com/hunting/regulations/taking-game/) — checked 2026-10-12. Checked equipment thresholds, dogs/roost/feed restrictions and closed locations.
- [FWC deer and wild turkey harvest reporting](https://myfwc.com/hunting/deer/harvest-report/) — checked 2026-10-12. Checked log-before-move duty, earliest reporting deadline and confirmation number.
- [FWC 2027 youth turkey hunts](https://myfwc.com/hunting/get-started/youth-turkey-hunting/) — checked 2026-10-12. Checked all four days of each regional youth hunt, age/supervision, adult participation and youth season-limit counting.
- [FWC wild turkey species profile](https://myfwc.com/wildlifehabitats/profiles/birds/game-birds/wild-turkeys/) — checked 2026-10-12. Checked Florida subspecies, appearance, habitat, flocking, feeding and tree roosts.
- [FWC how to hunt wild turkeys](https://myfwc.com/hunting/turkey/get-started/) — checked 2026-10-12. Checked scouting and patience guidance; links provide safe calling and shooting instruction.

### Turkey archery season / Gobblers and bearded turkeys only

Dates: 2026-10-17 to 2026-11-15

Bag: Daily limit 2; possession and season limit 2 for all fall seasons combined.

Licenses: Hunting license and Turkey Permit required unless individually exempt. Archery season permit required unless exempt.

Methods: Bows only.

- Shooting hours on private land: one-half hour before sunrise to one-half hour after sunset during fall hunts.
- Turkey arrows/bolts need broadheads at least 7/8 inch wide. Turkey PCP equipment must meet FWC's minimum .20-caliber projectile requirement. Non-PCP air guns are prohibited for turkey. Centerfire semiautomatic rifle magazines cannot exceed five rounds; fully automatic firearms are prohibited.
- Do not hunt turkeys with dogs, shoot a roosted turkey or hunt within 100 yards of a feeding station while feed is present. Live decoys, recorded game calls, artificial lights, traps and other prohibited methods are not authorized. Road rights-of-way, occupied premises, local discharge restrictions and private-property boundaries still apply.
- Log every turkey before moving it. Report to FWC within 24 hours or before final processing, transfer to a processor/taxidermist or leaving Florida, whichever is first; retain the confirmation number. HuntIt's personal harvest record does not submit an FWC report.
- Retain the head and beard, when applicable, and required hunter identification as evidence of legal harvest. After official reporting, transferred carcasses/parts require the hunter's name, address and harvest confirmation number; retain traceability and sex identification under FWC's processing/transport rules.

### Turkey crossbow season / Gobblers and bearded turkeys only

Dates: 2026-10-17 to 2026-11-20

Bag: Daily limit 2; possession and season limit 2 for all fall seasons combined.

Licenses: Hunting license and Turkey Permit required unless individually exempt. Crossbow season permit required unless exempt.

Methods: Crossbows, bows and airbows.

- Shooting hours on private land: one-half hour before sunrise to one-half hour after sunset during fall hunts.
- Turkey arrows/bolts need broadheads at least 7/8 inch wide. Turkey PCP equipment must meet FWC's minimum .20-caliber projectile requirement. Non-PCP air guns are prohibited for turkey. Centerfire semiautomatic rifle magazines cannot exceed five rounds; fully automatic firearms are prohibited.
- Do not hunt turkeys with dogs, shoot a roosted turkey or hunt within 100 yards of a feeding station while feed is present. Live decoys, recorded game calls, artificial lights, traps and other prohibited methods are not authorized. Road rights-of-way, occupied premises, local discharge restrictions and private-property boundaries still apply.
- Log every turkey before moving it. Report to FWC within 24 hours or before final processing, transfer to a processor/taxidermist or leaving Florida, whichever is first; retain the confirmation number. HuntIt's personal harvest record does not submit an FWC report.
- Retain the head and beard, when applicable, and required hunter identification as evidence of legal harvest. After official reporting, transferred carcasses/parts require the hunter's name, address and harvest confirmation number; retain traceability and sex identification under FWC's processing/transport rules.

### Turkey muzzleloading gun season / Gobblers and bearded turkeys only

Dates: 2026-11-21 to 2026-12-04

Bag: Daily limit 2; possession and season limit 2 for all fall seasons combined.

Licenses: Hunting license and Turkey Permit required unless individually exempt. Muzzleloading gun season permit required unless exempt.

Methods: Muzzleloaders, crossbows, bows and airbows. Muzzleloading projectiles must load through the muzzle; ignition must use wheel lock, flintlock, percussion cap or centerfire primer (including 209). Powder may load at the breech.

- Shooting hours on private land: one-half hour before sunrise to one-half hour after sunset during fall hunts.
- Turkey arrows/bolts need broadheads at least 7/8 inch wide. Turkey PCP equipment must meet FWC's minimum .20-caliber projectile requirement. Non-PCP air guns are prohibited for turkey. Centerfire semiautomatic rifle magazines cannot exceed five rounds; fully automatic firearms are prohibited.
- Do not hunt turkeys with dogs, shoot a roosted turkey or hunt within 100 yards of a feeding station while feed is present. Live decoys, recorded game calls, artificial lights, traps and other prohibited methods are not authorized. Road rights-of-way, occupied premises, local discharge restrictions and private-property boundaries still apply.
- Log every turkey before moving it. Report to FWC within 24 hours or before final processing, transfer to a processor/taxidermist or leaving Florida, whichever is first; retain the confirmation number. HuntIt's personal harvest record does not submit an FWC report.
- Retain the head and beard, when applicable, and required hunter identification as evidence of legal harvest. After official reporting, transferred carcasses/parts require the hunter's name, address and harvest confirmation number; retain traceability and sex identification under FWC's processing/transport rules.

### Fall turkey season / Gobblers and bearded turkeys only

Dates: 2026-12-05 to 2027-01-31

Bag: Daily limit 2; possession and season limit 2 for all fall seasons combined.

Licenses: Hunting license and Turkey Permit required unless individually exempt.

Methods: Shotguns, rifles, handguns, muzzleloaders, crossbows, bows and lawful pre-charged pneumatic (PCP) air guns.

- Shooting hours on private land: one-half hour before sunrise to one-half hour after sunset during fall hunts.
- Turkey arrows/bolts need broadheads at least 7/8 inch wide. Turkey PCP equipment must meet FWC's minimum .20-caliber projectile requirement. Non-PCP air guns are prohibited for turkey. Centerfire semiautomatic rifle magazines cannot exceed five rounds; fully automatic firearms are prohibited.
- Do not hunt turkeys with dogs, shoot a roosted turkey or hunt within 100 yards of a feeding station while feed is present. Live decoys, recorded game calls, artificial lights, traps and other prohibited methods are not authorized. Road rights-of-way, occupied premises, local discharge restrictions and private-property boundaries still apply.
- Log every turkey before moving it. Report to FWC within 24 hours or before final processing, transfer to a processor/taxidermist or leaving Florida, whichever is first; retain the confirmation number. HuntIt's personal harvest record does not submit an FWC report.
- Retain the head and beard, when applicable, and required hunter identification as evidence of legal harvest. After official reporting, transferred carcasses/parts require the hunter's name, address and harvest confirmation number; retain traceability and sex identification under FWC's processing/transport rules.

Conditions for the whole scope:

- Private lands outside the WMA system only; obtain landowner permission. WMA dates, quotas and shooting hours require the specific area brochure.
- License/permit exemptions require the relevant proof and conditions: youth under 16; Florida residents age 65+; qualifying homestead hunting in the county of residence; Florida residents holding the qualifying disability license; qualifying resident military members home on leave for at most 30 days with orders; authorized military/disabled-veteran events; and qualifying licensed-preserve patrons. Check the official exemption page. An exemption does not change season dates, bag limits, access permission or harvest reporting.
- The date bounds describe this edition's reviewed coverage; future seasons require new source review.

Proposed completion of blank species fields:

- scientific_name: Meleagris gallopavo
- description: Florida supports eastern and Osceola wild turkey subspecies. These large birds have long legs and broad tails; males commonly have a breast beard.
- habitat: Open woodland, forest edges and clearings across suitable Florida habitat; Osceola turkeys occur in peninsular Florida.
- behavior: Turkeys forage mainly on the ground, form flocks and roost in trees at night. They are wary and can fly rapidly over short distances.
- hunting_strategy: Scout the hunting area beforehand, learn where turkeys travel and remain patient. Follow FWC's safe-hunting and calling guidance and positively identify the legal bird and a safe shooting direction.

## Wild turkey: private land, fall c, 2026–2027

Key: `turkey-private-fall-c-2026-2027`. new draft.

Scope: zone: C

Review coverage: 2026-07-01 through 2027-01-31.

- [FWC 2026–2027 turkey seasons and limits](https://myfwc.com/hunting/season-dates/) — checked 2026-10-12. Checked zone fall dates, SR70 spring dates, lawful categories, methods and combined season limits; WMA schedules excluded.
- [FWC hunting licenses and permits](https://myfwc.com/license/recreational/hunting/) — checked 2026-10-12. Checked hunting license, Turkey Permit and season-specific permits.
- [FWC license exemptions](https://myfwc.com/license/recreational/do-i-need-one/) — checked 2026-10-12. Checked age, residency and conditional exemptions; access and hunting restrictions remain separate.
- [FWC general hunting information](https://myfwc.com/hunting/regulations/general-information/) — checked 2026-10-12. Checked private-land permission, fall/spring shooting hours, carcass evidence and transfer labeling.
- [FWC legal and prohibited methods](https://myfwc.com/hunting/regulations/taking-game/) — checked 2026-10-12. Checked equipment thresholds, dogs/roost/feed restrictions and closed locations.
- [FWC deer and wild turkey harvest reporting](https://myfwc.com/hunting/deer/harvest-report/) — checked 2026-10-12. Checked log-before-move duty, earliest reporting deadline and confirmation number.
- [FWC 2027 youth turkey hunts](https://myfwc.com/hunting/get-started/youth-turkey-hunting/) — checked 2026-10-12. Checked all four days of each regional youth hunt, age/supervision, adult participation and youth season-limit counting.
- [FWC wild turkey species profile](https://myfwc.com/wildlifehabitats/profiles/birds/game-birds/wild-turkeys/) — checked 2026-10-12. Checked Florida subspecies, appearance, habitat, flocking, feeding and tree roosts.
- [FWC how to hunt wild turkeys](https://myfwc.com/hunting/turkey/get-started/) — checked 2026-10-12. Checked scouting and patience guidance; links provide safe calling and shooting instruction.

### Turkey archery season / Gobblers and bearded turkeys only

Dates: 2026-09-19 to 2026-10-18

Bag: Daily limit 2; possession and season limit 2 for all fall seasons combined.

Licenses: Hunting license and Turkey Permit required unless individually exempt. Archery season permit required unless exempt.

Methods: Bows only.

- Shooting hours on private land: one-half hour before sunrise to one-half hour after sunset during fall hunts.
- Turkey arrows/bolts need broadheads at least 7/8 inch wide. Turkey PCP equipment must meet FWC's minimum .20-caliber projectile requirement. Non-PCP air guns are prohibited for turkey. Centerfire semiautomatic rifle magazines cannot exceed five rounds; fully automatic firearms are prohibited.
- Do not hunt turkeys with dogs, shoot a roosted turkey or hunt within 100 yards of a feeding station while feed is present. Live decoys, recorded game calls, artificial lights, traps and other prohibited methods are not authorized. Road rights-of-way, occupied premises, local discharge restrictions and private-property boundaries still apply.
- Log every turkey before moving it. Report to FWC within 24 hours or before final processing, transfer to a processor/taxidermist or leaving Florida, whichever is first; retain the confirmation number. HuntIt's personal harvest record does not submit an FWC report.
- Retain the head and beard, when applicable, and required hunter identification as evidence of legal harvest. After official reporting, transferred carcasses/parts require the hunter's name, address and harvest confirmation number; retain traceability and sex identification under FWC's processing/transport rules.

### Turkey crossbow season / Gobblers and bearded turkeys only

Dates: 2026-09-19 to 2026-10-23

Bag: Daily limit 2; possession and season limit 2 for all fall seasons combined.

Licenses: Hunting license and Turkey Permit required unless individually exempt. Crossbow season permit required unless exempt.

Methods: Crossbows, bows and airbows.

- Shooting hours on private land: one-half hour before sunrise to one-half hour after sunset during fall hunts.
- Turkey arrows/bolts need broadheads at least 7/8 inch wide. Turkey PCP equipment must meet FWC's minimum .20-caliber projectile requirement. Non-PCP air guns are prohibited for turkey. Centerfire semiautomatic rifle magazines cannot exceed five rounds; fully automatic firearms are prohibited.
- Do not hunt turkeys with dogs, shoot a roosted turkey or hunt within 100 yards of a feeding station while feed is present. Live decoys, recorded game calls, artificial lights, traps and other prohibited methods are not authorized. Road rights-of-way, occupied premises, local discharge restrictions and private-property boundaries still apply.
- Log every turkey before moving it. Report to FWC within 24 hours or before final processing, transfer to a processor/taxidermist or leaving Florida, whichever is first; retain the confirmation number. HuntIt's personal harvest record does not submit an FWC report.
- Retain the head and beard, when applicable, and required hunter identification as evidence of legal harvest. After official reporting, transferred carcasses/parts require the hunter's name, address and harvest confirmation number; retain traceability and sex identification under FWC's processing/transport rules.

### Turkey muzzleloading gun season / Gobblers and bearded turkeys only

Dates: 2026-10-24 to 2026-11-06

Bag: Daily limit 2; possession and season limit 2 for all fall seasons combined.

Licenses: Hunting license and Turkey Permit required unless individually exempt. Muzzleloading gun season permit required unless exempt.

Methods: Muzzleloaders, crossbows, bows and airbows. Muzzleloading projectiles must load through the muzzle; ignition must use wheel lock, flintlock, percussion cap or centerfire primer (including 209). Powder may load at the breech.

- Shooting hours on private land: one-half hour before sunrise to one-half hour after sunset during fall hunts.
- Turkey arrows/bolts need broadheads at least 7/8 inch wide. Turkey PCP equipment must meet FWC's minimum .20-caliber projectile requirement. Non-PCP air guns are prohibited for turkey. Centerfire semiautomatic rifle magazines cannot exceed five rounds; fully automatic firearms are prohibited.
- Do not hunt turkeys with dogs, shoot a roosted turkey or hunt within 100 yards of a feeding station while feed is present. Live decoys, recorded game calls, artificial lights, traps and other prohibited methods are not authorized. Road rights-of-way, occupied premises, local discharge restrictions and private-property boundaries still apply.
- Log every turkey before moving it. Report to FWC within 24 hours or before final processing, transfer to a processor/taxidermist or leaving Florida, whichever is first; retain the confirmation number. HuntIt's personal harvest record does not submit an FWC report.
- Retain the head and beard, when applicable, and required hunter identification as evidence of legal harvest. After official reporting, transferred carcasses/parts require the hunter's name, address and harvest confirmation number; retain traceability and sex identification under FWC's processing/transport rules.

### Fall turkey season / Gobblers and bearded turkeys only

Dates: 2026-11-07 to 2027-01-03

Bag: Daily limit 2; possession and season limit 2 for all fall seasons combined.

Licenses: Hunting license and Turkey Permit required unless individually exempt.

Methods: Shotguns, rifles, handguns, muzzleloaders, crossbows, bows and lawful pre-charged pneumatic (PCP) air guns.

- Shooting hours on private land: one-half hour before sunrise to one-half hour after sunset during fall hunts.
- Turkey arrows/bolts need broadheads at least 7/8 inch wide. Turkey PCP equipment must meet FWC's minimum .20-caliber projectile requirement. Non-PCP air guns are prohibited for turkey. Centerfire semiautomatic rifle magazines cannot exceed five rounds; fully automatic firearms are prohibited.
- Do not hunt turkeys with dogs, shoot a roosted turkey or hunt within 100 yards of a feeding station while feed is present. Live decoys, recorded game calls, artificial lights, traps and other prohibited methods are not authorized. Road rights-of-way, occupied premises, local discharge restrictions and private-property boundaries still apply.
- Log every turkey before moving it. Report to FWC within 24 hours or before final processing, transfer to a processor/taxidermist or leaving Florida, whichever is first; retain the confirmation number. HuntIt's personal harvest record does not submit an FWC report.
- Retain the head and beard, when applicable, and required hunter identification as evidence of legal harvest. After official reporting, transferred carcasses/parts require the hunter's name, address and harvest confirmation number; retain traceability and sex identification under FWC's processing/transport rules.

Conditions for the whole scope:

- Private lands outside the WMA system only; obtain landowner permission. WMA dates, quotas and shooting hours require the specific area brochure.
- License/permit exemptions require the relevant proof and conditions: youth under 16; Florida residents age 65+; qualifying homestead hunting in the county of residence; Florida residents holding the qualifying disability license; qualifying resident military members home on leave for at most 30 days with orders; authorized military/disabled-veteran events; and qualifying licensed-preserve patrons. Check the official exemption page. An exemption does not change season dates, bag limits, access permission or harvest reporting.
- The date bounds describe this edition's reviewed coverage; future seasons require new source review.

Proposed completion of blank species fields:

- scientific_name: Meleagris gallopavo
- description: Florida supports eastern and Osceola wild turkey subspecies. These large birds have long legs and broad tails; males commonly have a breast beard.
- habitat: Open woodland, forest edges and clearings across suitable Florida habitat; Osceola turkeys occur in peninsular Florida.
- behavior: Turkeys forage mainly on the ground, form flocks and roost in trees at night. They are wary and can fly rapidly over short distances.
- hunting_strategy: Scout the hunting area beforehand, learn where turkeys travel and remain patient. Follow FWC's safe-hunting and calling guidance and positively identify the legal bird and a safe shooting direction.

## Wild turkey: private land, fall d, 2026–2027

Key: `turkey-private-fall-d-2026-2027`. new draft.

Scope: zone: D

Review coverage: 2026-07-01 through 2027-01-31.

- [FWC 2026–2027 turkey seasons and limits](https://myfwc.com/hunting/season-dates/) — checked 2026-10-12. Checked zone fall dates, SR70 spring dates, lawful categories, methods and combined season limits; WMA schedules excluded.
- [FWC hunting licenses and permits](https://myfwc.com/license/recreational/hunting/) — checked 2026-10-12. Checked hunting license, Turkey Permit and season-specific permits.
- [FWC license exemptions](https://myfwc.com/license/recreational/do-i-need-one/) — checked 2026-10-12. Checked age, residency and conditional exemptions; access and hunting restrictions remain separate.
- [FWC general hunting information](https://myfwc.com/hunting/regulations/general-information/) — checked 2026-10-12. Checked private-land permission, fall/spring shooting hours, carcass evidence and transfer labeling.
- [FWC legal and prohibited methods](https://myfwc.com/hunting/regulations/taking-game/) — checked 2026-10-12. Checked equipment thresholds, dogs/roost/feed restrictions and closed locations.
- [FWC deer and wild turkey harvest reporting](https://myfwc.com/hunting/deer/harvest-report/) — checked 2026-10-12. Checked log-before-move duty, earliest reporting deadline and confirmation number.
- [FWC 2027 youth turkey hunts](https://myfwc.com/hunting/get-started/youth-turkey-hunting/) — checked 2026-10-12. Checked all four days of each regional youth hunt, age/supervision, adult participation and youth season-limit counting.
- [FWC wild turkey species profile](https://myfwc.com/wildlifehabitats/profiles/birds/game-birds/wild-turkeys/) — checked 2026-10-12. Checked Florida subspecies, appearance, habitat, flocking, feeding and tree roosts.
- [FWC how to hunt wild turkeys](https://myfwc.com/hunting/turkey/get-started/) — checked 2026-10-12. Checked scouting and patience guidance; links provide safe calling and shooting instruction.

### Turkey archery season / Gobblers and bearded turkeys only

Dates: 2026-10-24 to 2026-11-25

Bag: Daily limit 2; possession and season limit 2 for all fall seasons combined.

Licenses: Hunting license and Turkey Permit required unless individually exempt. Archery season permit required unless exempt.

Methods: Bows only.

- Shooting hours on private land: one-half hour before sunrise to one-half hour after sunset during fall hunts.
- Turkey arrows/bolts need broadheads at least 7/8 inch wide. Turkey PCP equipment must meet FWC's minimum .20-caliber projectile requirement. Non-PCP air guns are prohibited for turkey. Centerfire semiautomatic rifle magazines cannot exceed five rounds; fully automatic firearms are prohibited.
- Do not hunt turkeys with dogs, shoot a roosted turkey or hunt within 100 yards of a feeding station while feed is present. Live decoys, recorded game calls, artificial lights, traps and other prohibited methods are not authorized. Road rights-of-way, occupied premises, local discharge restrictions and private-property boundaries still apply.
- Log every turkey before moving it. Report to FWC within 24 hours or before final processing, transfer to a processor/taxidermist or leaving Florida, whichever is first; retain the confirmation number. HuntIt's personal harvest record does not submit an FWC report.
- Retain the head and beard, when applicable, and required hunter identification as evidence of legal harvest. After official reporting, transferred carcasses/parts require the hunter's name, address and harvest confirmation number; retain traceability and sex identification under FWC's processing/transport rules.

### Turkey crossbow season / Gobblers and bearded turkeys only

Dates: 2026-10-24 to 2026-11-25; 2026-11-30 to 2026-12-04

Bag: Daily limit 2; possession and season limit 2 for all fall seasons combined.

Licenses: Hunting license and Turkey Permit required unless individually exempt. Crossbow season permit required unless exempt.

Methods: Crossbows, bows and airbows.

- Shooting hours on private land: one-half hour before sunrise to one-half hour after sunset during fall hunts.
- Turkey arrows/bolts need broadheads at least 7/8 inch wide. Turkey PCP equipment must meet FWC's minimum .20-caliber projectile requirement. Non-PCP air guns are prohibited for turkey. Centerfire semiautomatic rifle magazines cannot exceed five rounds; fully automatic firearms are prohibited.
- Do not hunt turkeys with dogs, shoot a roosted turkey or hunt within 100 yards of a feeding station while feed is present. Live decoys, recorded game calls, artificial lights, traps and other prohibited methods are not authorized. Road rights-of-way, occupied premises, local discharge restrictions and private-property boundaries still apply.
- Log every turkey before moving it. Report to FWC within 24 hours or before final processing, transfer to a processor/taxidermist or leaving Florida, whichever is first; retain the confirmation number. HuntIt's personal harvest record does not submit an FWC report.
- Retain the head and beard, when applicable, and required hunter identification as evidence of legal harvest. After official reporting, transferred carcasses/parts require the hunter's name, address and harvest confirmation number; retain traceability and sex identification under FWC's processing/transport rules.

### Turkey muzzleloading gun season / Gobblers and bearded turkeys only

Dates: 2026-12-05 to 2026-12-11

Bag: Daily limit 2; possession and season limit 2 for all fall seasons combined.

Licenses: Hunting license and Turkey Permit required unless individually exempt. Muzzleloading gun season permit required unless exempt.

Methods: Muzzleloaders, crossbows, bows and airbows. Muzzleloading projectiles must load through the muzzle; ignition must use wheel lock, flintlock, percussion cap or centerfire primer (including 209). Powder may load at the breech.

- Shooting hours on private land: one-half hour before sunrise to one-half hour after sunset during fall hunts.
- Turkey arrows/bolts need broadheads at least 7/8 inch wide. Turkey PCP equipment must meet FWC's minimum .20-caliber projectile requirement. Non-PCP air guns are prohibited for turkey. Centerfire semiautomatic rifle magazines cannot exceed five rounds; fully automatic firearms are prohibited.
- Do not hunt turkeys with dogs, shoot a roosted turkey or hunt within 100 yards of a feeding station while feed is present. Live decoys, recorded game calls, artificial lights, traps and other prohibited methods are not authorized. Road rights-of-way, occupied premises, local discharge restrictions and private-property boundaries still apply.
- Log every turkey before moving it. Report to FWC within 24 hours or before final processing, transfer to a processor/taxidermist or leaving Florida, whichever is first; retain the confirmation number. HuntIt's personal harvest record does not submit an FWC report.
- Retain the head and beard, when applicable, and required hunter identification as evidence of legal harvest. After official reporting, transferred carcasses/parts require the hunter's name, address and harvest confirmation number; retain traceability and sex identification under FWC's processing/transport rules.

### Fall turkey season / Gobblers and bearded turkeys only

Dates: 2026-11-26 to 2026-11-29; 2026-12-12 to 2027-01-17

Bag: Daily limit 2; possession and season limit 2 for all fall seasons combined.

Licenses: Hunting license and Turkey Permit required unless individually exempt.

Methods: Shotguns, rifles, handguns, muzzleloaders, crossbows, bows and lawful pre-charged pneumatic (PCP) air guns.

- Shooting hours on private land: one-half hour before sunrise to one-half hour after sunset during fall hunts.
- Turkey arrows/bolts need broadheads at least 7/8 inch wide. Turkey PCP equipment must meet FWC's minimum .20-caliber projectile requirement. Non-PCP air guns are prohibited for turkey. Centerfire semiautomatic rifle magazines cannot exceed five rounds; fully automatic firearms are prohibited.
- Do not hunt turkeys with dogs, shoot a roosted turkey or hunt within 100 yards of a feeding station while feed is present. Live decoys, recorded game calls, artificial lights, traps and other prohibited methods are not authorized. Road rights-of-way, occupied premises, local discharge restrictions and private-property boundaries still apply.
- Log every turkey before moving it. Report to FWC within 24 hours or before final processing, transfer to a processor/taxidermist or leaving Florida, whichever is first; retain the confirmation number. HuntIt's personal harvest record does not submit an FWC report.
- Retain the head and beard, when applicable, and required hunter identification as evidence of legal harvest. After official reporting, transferred carcasses/parts require the hunter's name, address and harvest confirmation number; retain traceability and sex identification under FWC's processing/transport rules.

Conditions for the whole scope:

- Private lands outside the WMA system only; obtain landowner permission. WMA dates, quotas and shooting hours require the specific area brochure.
- License/permit exemptions require the relevant proof and conditions: youth under 16; Florida residents age 65+; qualifying homestead hunting in the county of residence; Florida residents holding the qualifying disability license; qualifying resident military members home on leave for at most 30 days with orders; authorized military/disabled-veteran events; and qualifying licensed-preserve patrons. Check the official exemption page. An exemption does not change season dates, bag limits, access permission or harvest reporting.
- The date bounds describe this edition's reviewed coverage; future seasons require new source review.

Proposed completion of blank species fields:

- scientific_name: Meleagris gallopavo
- description: Florida supports eastern and Osceola wild turkey subspecies. These large birds have long legs and broad tails; males commonly have a breast beard.
- habitat: Open woodland, forest edges and clearings across suitable Florida habitat; Osceola turkeys occur in peninsular Florida.
- behavior: Turkeys forage mainly on the ground, form flocks and roost in trees at night. They are wary and can fly rapidly over short distances.
- hunting_strategy: Scout the hunting area beforehand, learn where turkeys travel and remain patient. Follow FWC's safe-hunting and calling guidance and positively identify the legal bird and a safe shooting direction.

## Wild turkey: private land, spring north_sr70, 2026–2027

Key: `turkey-private-spring-north_sr70-2026-2027`. new draft.

Scope: regulatory_area: North of State Road 70

Review coverage: 2027-02-01 through 2027-06-30.

- [FWC 2026–2027 turkey seasons and limits](https://myfwc.com/hunting/season-dates/) — checked 2026-10-12. Checked zone fall dates, SR70 spring dates, lawful categories, methods and combined season limits; WMA schedules excluded.
- [FWC hunting licenses and permits](https://myfwc.com/license/recreational/hunting/) — checked 2026-10-12. Checked hunting license, Turkey Permit and season-specific permits.
- [FWC license exemptions](https://myfwc.com/license/recreational/do-i-need-one/) — checked 2026-10-12. Checked age, residency and conditional exemptions; access and hunting restrictions remain separate.
- [FWC general hunting information](https://myfwc.com/hunting/regulations/general-information/) — checked 2026-10-12. Checked private-land permission, fall/spring shooting hours, carcass evidence and transfer labeling.
- [FWC legal and prohibited methods](https://myfwc.com/hunting/regulations/taking-game/) — checked 2026-10-12. Checked equipment thresholds, dogs/roost/feed restrictions and closed locations.
- [FWC deer and wild turkey harvest reporting](https://myfwc.com/hunting/deer/harvest-report/) — checked 2026-10-12. Checked log-before-move duty, earliest reporting deadline and confirmation number.
- [FWC 2027 youth turkey hunts](https://myfwc.com/hunting/get-started/youth-turkey-hunting/) — checked 2026-10-12. Checked all four days of each regional youth hunt, age/supervision, adult participation and youth season-limit counting.
- [FWC wild turkey species profile](https://myfwc.com/wildlifehabitats/profiles/birds/game-birds/wild-turkeys/) — checked 2026-10-12. Checked Florida subspecies, appearance, habitat, flocking, feeding and tree roosts.
- [FWC how to hunt wild turkeys](https://myfwc.com/hunting/turkey/get-started/) — checked 2026-10-12. Checked scouting and patience guidance; links provide safe calling and shooting instruction.

### Spring turkey season / Gobblers and bearded turkeys only

Dates: 2027-03-20 to 2027-04-25

Bag: Daily limit 2; possession and season limit 2 for all spring seasons combined.

Licenses: Hunting license and Turkey Permit required unless individually exempt.

Methods: Shotguns, rifles, handguns, muzzleloaders, crossbows, bows and lawful pre-charged pneumatic (PCP) air guns.

- Shooting hours on private land: one-half hour before sunrise to sunset during spring (including youth) hunts.
- Turkey arrows/bolts need broadheads at least 7/8 inch wide. Turkey PCP equipment must meet FWC's minimum .20-caliber projectile requirement. Non-PCP air guns are prohibited for turkey. Centerfire semiautomatic rifle magazines cannot exceed five rounds; fully automatic firearms are prohibited.
- Do not hunt turkeys with dogs, shoot a roosted turkey or hunt within 100 yards of a feeding station while feed is present. Live decoys, recorded game calls, artificial lights, traps and other prohibited methods are not authorized. Road rights-of-way, occupied premises, local discharge restrictions and private-property boundaries still apply.
- Log every turkey before moving it. Report to FWC within 24 hours or before final processing, transfer to a processor/taxidermist or leaving Florida, whichever is first; retain the confirmation number. HuntIt's personal harvest record does not submit an FWC report.
- Retain the head and beard, when applicable, and required hunter identification as evidence of legal harvest. After official reporting, transferred carcasses/parts require the hunter's name, address and harvest confirmation number; retain traceability and sex identification under FWC's processing/transport rules.

### Youth spring turkey hunt / Gobblers and bearded turkeys only

Dates: 2027-03-12 to 2027-03-15

Bag: Daily limit 2; possession and season limit 2 for all spring seasons combined. Youth-hunt harvest counts toward the same spring limit of 2.

Licenses: No hunting license or permit required for youth 15 and under or a supervising adult who only supervises. Adults who call or otherwise participate need a hunting license and Turkey Permit; they may not shoot or shoot at turkey.

Methods: Shotguns, rifles, handguns, muzzleloaders, crossbows, bows and lawful pre-charged pneumatic (PCP) air guns.

- Shooting hours on private land: one-half hour before sunrise to sunset during spring (including youth) hunts.
- Turkey arrows/bolts need broadheads at least 7/8 inch wide. Turkey PCP equipment must meet FWC's minimum .20-caliber projectile requirement. Non-PCP air guns are prohibited for turkey. Centerfire semiautomatic rifle magazines cannot exceed five rounds; fully automatic firearms are prohibited.
- Do not hunt turkeys with dogs, shoot a roosted turkey or hunt within 100 yards of a feeding station while feed is present. Live decoys, recorded game calls, artificial lights, traps and other prohibited methods are not authorized. Road rights-of-way, occupied premises, local discharge restrictions and private-property boundaries still apply.
- Log every turkey before moving it. Report to FWC within 24 hours or before final processing, transfer to a processor/taxidermist or leaving Florida, whichever is first; retain the confirmation number. HuntIt's personal harvest record does not submit an FWC report.
- Retain the head and beard, when applicable, and required hunter identification as evidence of legal harvest. After official reporting, transferred carcasses/parts require the hunter's name, address and harvest confirmation number; retain traceability and sex identification under FWC's processing/transport rules.
- Only youth 15 and younger may harvest during this hunt, supervised by an adult age 18 or older.

Conditions for the whole scope:

- Private lands outside the WMA system only; obtain landowner permission. WMA dates, quotas and shooting hours require the specific area brochure.
- License/permit exemptions require the relevant proof and conditions: youth under 16; Florida residents age 65+; qualifying homestead hunting in the county of residence; Florida residents holding the qualifying disability license; qualifying resident military members home on leave for at most 30 days with orders; authorized military/disabled-veteran events; and qualifying licensed-preserve patrons. Check the official exemption page. An exemption does not change season dates, bag limits, access permission or harvest reporting.
- The date bounds describe this edition's reviewed coverage; future seasons require new source review.

Proposed completion of blank species fields:

- scientific_name: Meleagris gallopavo
- description: Florida supports eastern and Osceola wild turkey subspecies. These large birds have long legs and broad tails; males commonly have a breast beard.
- habitat: Open woodland, forest edges and clearings across suitable Florida habitat; Osceola turkeys occur in peninsular Florida.
- behavior: Turkeys forage mainly on the ground, form flocks and roost in trees at night. They are wary and can fly rapidly over short distances.
- hunting_strategy: Scout the hunting area beforehand, learn where turkeys travel and remain patient. Follow FWC's safe-hunting and calling guidance and positively identify the legal bird and a safe shooting direction.

## Wild turkey: private land, spring south_sr70, 2026–2027

Key: `turkey-private-spring-south_sr70-2026-2027`. new draft.

Scope: regulatory_area: South of State Road 70

Review coverage: 2027-02-01 through 2027-06-30.

- [FWC 2026–2027 turkey seasons and limits](https://myfwc.com/hunting/season-dates/) — checked 2026-10-12. Checked zone fall dates, SR70 spring dates, lawful categories, methods and combined season limits; WMA schedules excluded.
- [FWC hunting licenses and permits](https://myfwc.com/license/recreational/hunting/) — checked 2026-10-12. Checked hunting license, Turkey Permit and season-specific permits.
- [FWC license exemptions](https://myfwc.com/license/recreational/do-i-need-one/) — checked 2026-10-12. Checked age, residency and conditional exemptions; access and hunting restrictions remain separate.
- [FWC general hunting information](https://myfwc.com/hunting/regulations/general-information/) — checked 2026-10-12. Checked private-land permission, fall/spring shooting hours, carcass evidence and transfer labeling.
- [FWC legal and prohibited methods](https://myfwc.com/hunting/regulations/taking-game/) — checked 2026-10-12. Checked equipment thresholds, dogs/roost/feed restrictions and closed locations.
- [FWC deer and wild turkey harvest reporting](https://myfwc.com/hunting/deer/harvest-report/) — checked 2026-10-12. Checked log-before-move duty, earliest reporting deadline and confirmation number.
- [FWC 2027 youth turkey hunts](https://myfwc.com/hunting/get-started/youth-turkey-hunting/) — checked 2026-10-12. Checked all four days of each regional youth hunt, age/supervision, adult participation and youth season-limit counting.
- [FWC wild turkey species profile](https://myfwc.com/wildlifehabitats/profiles/birds/game-birds/wild-turkeys/) — checked 2026-10-12. Checked Florida subspecies, appearance, habitat, flocking, feeding and tree roosts.
- [FWC how to hunt wild turkeys](https://myfwc.com/hunting/turkey/get-started/) — checked 2026-10-12. Checked scouting and patience guidance; links provide safe calling and shooting instruction.

### Spring turkey season / Gobblers and bearded turkeys only

Dates: 2027-03-06 to 2027-04-11

Bag: Daily limit 2; possession and season limit 2 for all spring seasons combined.

Licenses: Hunting license and Turkey Permit required unless individually exempt.

Methods: Shotguns, rifles, handguns, muzzleloaders, crossbows, bows and lawful pre-charged pneumatic (PCP) air guns.

- Shooting hours on private land: one-half hour before sunrise to sunset during spring (including youth) hunts.
- Turkey arrows/bolts need broadheads at least 7/8 inch wide. Turkey PCP equipment must meet FWC's minimum .20-caliber projectile requirement. Non-PCP air guns are prohibited for turkey. Centerfire semiautomatic rifle magazines cannot exceed five rounds; fully automatic firearms are prohibited.
- Do not hunt turkeys with dogs, shoot a roosted turkey or hunt within 100 yards of a feeding station while feed is present. Live decoys, recorded game calls, artificial lights, traps and other prohibited methods are not authorized. Road rights-of-way, occupied premises, local discharge restrictions and private-property boundaries still apply.
- Log every turkey before moving it. Report to FWC within 24 hours or before final processing, transfer to a processor/taxidermist or leaving Florida, whichever is first; retain the confirmation number. HuntIt's personal harvest record does not submit an FWC report.
- Retain the head and beard, when applicable, and required hunter identification as evidence of legal harvest. After official reporting, transferred carcasses/parts require the hunter's name, address and harvest confirmation number; retain traceability and sex identification under FWC's processing/transport rules.

### Youth spring turkey hunt / Gobblers and bearded turkeys only

Dates: 2027-02-26 to 2027-03-01

Bag: Daily limit 2; possession and season limit 2 for all spring seasons combined. Youth-hunt harvest counts toward the same spring limit of 2.

Licenses: No hunting license or permit required for youth 15 and under or a supervising adult who only supervises. Adults who call or otherwise participate need a hunting license and Turkey Permit; they may not shoot or shoot at turkey.

Methods: Shotguns, rifles, handguns, muzzleloaders, crossbows, bows and lawful pre-charged pneumatic (PCP) air guns.

- Shooting hours on private land: one-half hour before sunrise to sunset during spring (including youth) hunts.
- Turkey arrows/bolts need broadheads at least 7/8 inch wide. Turkey PCP equipment must meet FWC's minimum .20-caliber projectile requirement. Non-PCP air guns are prohibited for turkey. Centerfire semiautomatic rifle magazines cannot exceed five rounds; fully automatic firearms are prohibited.
- Do not hunt turkeys with dogs, shoot a roosted turkey or hunt within 100 yards of a feeding station while feed is present. Live decoys, recorded game calls, artificial lights, traps and other prohibited methods are not authorized. Road rights-of-way, occupied premises, local discharge restrictions and private-property boundaries still apply.
- Log every turkey before moving it. Report to FWC within 24 hours or before final processing, transfer to a processor/taxidermist or leaving Florida, whichever is first; retain the confirmation number. HuntIt's personal harvest record does not submit an FWC report.
- Retain the head and beard, when applicable, and required hunter identification as evidence of legal harvest. After official reporting, transferred carcasses/parts require the hunter's name, address and harvest confirmation number; retain traceability and sex identification under FWC's processing/transport rules.
- Only youth 15 and younger may harvest during this hunt, supervised by an adult age 18 or older.

Conditions for the whole scope:

- Private lands outside the WMA system only; obtain landowner permission. WMA dates, quotas and shooting hours require the specific area brochure.
- License/permit exemptions require the relevant proof and conditions: youth under 16; Florida residents age 65+; qualifying homestead hunting in the county of residence; Florida residents holding the qualifying disability license; qualifying resident military members home on leave for at most 30 days with orders; authorized military/disabled-veteran events; and qualifying licensed-preserve patrons. Check the official exemption page. An exemption does not change season dates, bag limits, access permission or harvest reporting.
- The date bounds describe this edition's reviewed coverage; future seasons require new source review.

Proposed completion of blank species fields:

- scientific_name: Meleagris gallopavo
- description: Florida supports eastern and Osceola wild turkey subspecies. These large birds have long legs and broad tails; males commonly have a breast beard.
- habitat: Open woodland, forest edges and clearings across suitable Florida habitat; Osceola turkeys occur in peninsular Florida.
- behavior: Turkeys forage mainly on the ground, form flocks and roost in trees at night. They are wary and can fly rapidly over short distances.
- hunting_strategy: Scout the hunting area beforehand, learn where turkeys travel and remain patient. Follow FWC's safe-hunting and calling guidance and positively identify the legal bird and a safe shooting direction.

## Wild Turkey: Rotenberger WMA / Wildlife Management Area (WMA), 2026-2027 expansion

Key: `turkey-rotenberger-2-2026-2027-expanded`. new draft.

Scope: managed_area: Rotenberger WMA

Review coverage: 2026-07-01 through 2027-06-30.

- [FWC Rotenberger WMA 2026-2027 regulations and map](https://app.myfwc.com/hgm/hgmsearch/wmad?brochureTitle=Rotenberger) — checked 2026-10-12. Interactive brochure checked: area dates, legal species, bag limits, methods, permits, access and exceptions; PDF map available on the same page.
- [FWC hunting licenses and permits](https://myfwc.com/license/recreational/hunting/) — checked 2026-10-12. General license, management-area and season permits; brochure exemptions and area-specific quota restrictions retained.

### Turkey take prohibited / Turkey take prohibited

Dates: 2026-07-01 to 2027-06-30

Bag: No turkey may be taken.

Licenses: No license or permit authorizes turkey take in this area.

Methods: Turkey hunting/take is prohibited by the area brochure.

**Explicit prohibition. Search must remain closed throughout these dates.**

- The area brochure expressly prohibits turkey. Private-land turkey dates and permits do not override this prohibition.

Conditions for the whole scope:

- Hunting over bait, taking swimming deer or spotted fawns, and hunting in posted closed areas are prohibited.
- Ordinary shooting hours are half an hour before sunrise through half an hour after sunset; turkey has separate hours.
- Night gun hunting, fully automatic firearms and centerfire semiautomatic rifles with magazines capable of more than 5 rounds are prohibited.
- Deer hunters and companions need 500 square inches of fluorescent orange above the waist, except bow-and-arrow hunting during archery season.
- Brochure license/permit exemptions include children under 16, Florida residents 65+, residents with a qualifying disabled-person certificate, and qualifying resident military personnel home on leave. They do not override quota permits marked no exemptions or required deer tags. Hunters born on/after June 1, 1975 need hunter-safety certification or the lawful supervised mentoring exception. Youth require adult supervision; mentoring license holders require a licensed supervisor aged 21+. Consult the complete brochure.
- The official brochure includes PDF BROCHURE and PDF MAP ONLY controls. Follow its current maps, access restrictions and FWC closure notices.

## Wild Turkey: Rotenberger WMA / Commission-Managed Land, 2026-2027 expansion

Key: `turkey-rotenberger-3-2026-2027-expanded`. new draft.

Scope: managed_area: Rotenberger WMA

Review coverage: 2026-07-01 through 2027-06-30.

- [FWC Rotenberger WMA 2026-2027 regulations and map](https://app.myfwc.com/hgm/hgmsearch/wmad?brochureTitle=Rotenberger) — checked 2026-10-12. Interactive brochure checked: area dates, legal species, bag limits, methods, permits, access and exceptions; PDF map available on the same page.
- [FWC hunting licenses and permits](https://myfwc.com/license/recreational/hunting/) — checked 2026-10-12. General license, management-area and season permits; brochure exemptions and area-specific quota restrictions retained.

### Turkey take prohibited / Turkey take prohibited

Dates: 2026-07-01 to 2027-06-30

Bag: No turkey may be taken.

Licenses: No license or permit authorizes turkey take in this area.

Methods: Turkey hunting/take is prohibited by the area brochure.

**Explicit prohibition. Search must remain closed throughout these dates.**

- The area brochure expressly prohibits turkey. Private-land turkey dates and permits do not override this prohibition.

Conditions for the whole scope:

- Hunting over bait, taking swimming deer or spotted fawns, and hunting in posted closed areas are prohibited.
- Ordinary shooting hours are half an hour before sunrise through half an hour after sunset; turkey has separate hours.
- Night gun hunting, fully automatic firearms and centerfire semiautomatic rifles with magazines capable of more than 5 rounds are prohibited.
- Deer hunters and companions need 500 square inches of fluorescent orange above the waist, except bow-and-arrow hunting during archery season.
- Brochure license/permit exemptions include children under 16, Florida residents 65+, residents with a qualifying disabled-person certificate, and qualifying resident military personnel home on leave. They do not override quota permits marked no exemptions or required deer tags. Hunters born on/after June 1, 1975 need hunter-safety certification or the lawful supervised mentoring exception. Youth require adult supervision; mentoring license holders require a licensed supervisor aged 21+. Consult the complete brochure.
- The official brochure includes PDF BROCHURE and PDF MAP ONLY controls. Follow its current maps, access restrictions and FWC closure notices.
