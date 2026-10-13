# Dinner Island Ranch data expansion review

**Status: human-approved for local publication on October 12, 2026.** The project owner checked the sources and stated **“Sources checked — approve local publication.”** See [DATA_EXPANSION_APPROVAL.md](../DATA_EXPANSION_APPROVAL.md) for the exact approved expansion and provenance. The worksheet below retains its original pre-publication wording as source-review history; future edits still require review. Source check: October 12, 2026. Coverage: July 1, 2026 through June 30, 2027.

These eight new working drafts cover the existing Dinner Island Ranch WMA catalog entry for deer, wild hog, wild turkey and Burmese python through both public-land selectors. They exclude the separately regulated Caracara Unit. No imported season row, earlier approved release, team-maintained draft or existing publication is changed. The data remains unpublished until an authorized administrator personally checks the sources and publishes it.

## Official evidence

- [FWC 2026-2027 Dinner Island Ranch regulations brochure](https://app.myfwc.com/hgm/hgmsearch/wmad?brochureTitle=Dinner+Island+Ranch): the complete interactive brochure was read, including Attention Hunters, permits/quotas, bags, methods, access, each hunting season and non-native reptile provisions. The page's PDF BROCHURE and PDF MAP ONLY controls provide the area map and printable material.
- [FWC 2026-2027 Dinner Island Ranch hunt calendar](https://app.myfwc.com/hsc/wmahuntcalendar/?areaName=dinner+island+ranch): corroborates every date below, including cross-year endpoints. The calendar alone is not a source for bag limits, methods or access permission.
- [FWC hunting licenses and permits](https://myfwc.com/license/recreational/hunting/): individual license/season-permit exemptions are separate from area quota permits marked no exemptions.
- [FWC taking game](https://myfwc.com/hunting/regulations/taking-game/): deer muzzleloader minimum caliber/gauge and deer/turkey broadhead width, with stricter area methods preserved.
- [FWC wild hog guidance](https://myfwc.com/hunting/wild-hog/): hunting licenses are not required for wild hog on WMAs; management-area, season and quota permit rules still apply.
- [FWC public python removal](https://myfwc.com/wildlifehabitats/nonnatives/python/removing/) and [humane removal guidance](https://myfwc.com/wildlifehabitats/nonnatives/python/humane-killing-methods/): named-area public-removal exception, humane onsite removal, no public live transport, and property-specific firearm restrictions.

## Dated opportunities

| Area season | Explicit dates | Existing species supported |
|---|---|---|
| Archery | August 7-10, 14-17, 21-24 and 28-31, 2026 | Antlered deer and hog; bows with stated disability exception |
| Muzzleloading gun | September 11-13, 2026 | Antlered deer and hog; muzzleloading guns only |
| Family | September 19-20 and October 17-18, 2026 | Antlered deer and hog; family eligibility and quota conditions |
| General gun | September 25-27, October 2-4 and October 9-11, 2026 | Antlered deer and hog |
| Small game | October 19, 2026-February 20, 2027 | Hog; no deer; centerfire rifles expressly allowed; no hog dogs |
| Youth turkey | February 26-March 1, 2027 | Gobbler or bearded turkey; under 16 with direct adult supervision |
| Spring turkey | March 6-8, March 13-15 and April 3-5, 2027 | Gobbler or bearded turkey |
| Non-native reptile removal | Entire documented review coverage | Python, with non-firearm year-round provision and qualified firearm restrictions |

The dates are area-specific. No fall turkey dates, antlerless deer dates, statewide zone dates or Caracara Unit dates are substituted. A selected day between separate hunts is closed for that listed game species.

## Exceptions retained

Deer has a limit of one antlered deer per quota permit, except family hunts allow two per quota permit with no more than one per person. Guests share the quota bag. Statewide daily, possession and annual limits still apply. The area antler standard is three one-inch points on one antler or a ten-inch main beam, with the stated youth annual exception; antlerless deer are not authorized by these seasons. Fluorescent-orange and legal-ammunition requirements are included. Deer muzzleloaders need at least .30 caliber for a single bullet or 20 gauge for multiple balls, and deer/turkey arrows or bolts need broadheads at least 7/8 inch wide. The area's turkey PCP bolt/arrow-only restriction remains in force; statewide PCP bullet guidance does not expand it.

Hog has no bag or size limit. Archery, muzzleloading, family and general-gun hunts require the relevant no-exemption quota permit. The small-game season has no quota requirement and expressly allows centerfire rifles. Hog hunting is prohibited during youth and spring turkey hunts. Dogs may not hunt hog or deer; the leashed wounded-game tracking exception is retained.

Turkey has a shared limit of one gobbler or bearded turkey per youth/spring quota permit, alongside statewide spring limits. Both youth and spring hunts require quota permits without exemptions. Youth under 16 must be directly physically supervised by an adult at least 18; participating adults need the applicable credentials and cannot harvest during the youth hunt. Turkey methods are bows, crossbows, PCP bolt/arrow airguns or shotguns with No. 2 or smaller shot; rifles, pistols and PCP bullets are prohibited. Shooting ends at sunset.

Python removal is not a year-round firearm authorization. The brochure permits non-firearm methods year-round and restricts firearms to open area hunting seasons and methods allowed for that season. Dogs and public live removal are prohibited. The brochure also prohibits hunting other animals during spring turkey. Because it does not expressly resolve that interaction with non-native reptile firearm take, the draft directs users to confirm with FWC before using a firearm for python during a spring/youth turkey hunt. No blanket spring firearm exception is invented.

The prominent Attention Hunters notice overrides the brochure's standard check-station text: there is no operating check station in 2026-2027 and all check-station duties are waived. Deer/turkey logging before moving and official FWC reporting within 24 hours remain required, subject to earlier processing/transfer/out-of-state deadlines. HuntIt's private harvest log is separate from official reporting.

Access notes retain designated entrances, named/numbered roads, nighttime vehicle limits, the camping-permit exception, quota-hunter ATV/swamp-buggy road exceptions, closed areas, horse restrictions, designated camping and posted dove-field Saturday restrictions. Access notes do not establish that a particular parcel is open: users must check the brochure map and current closures.

## Reviewer and QA checklist

Compare the above against the full linked brochure and map before publishing. Review the four species through both public selectors, including family ages/bags, the youth turkey endpoint crossing into March, the no-check-station notice and the python spring firearm qualification. Use the normal administrator source acknowledgment and meaningful review notes. Saving or running setup alone does not publish these drafts.

`backend/integration/test_extra_wma_data.py` exercises every positive period's opening/closing endpoint and the days immediately outside it, both public selectors, wrong-area exclusion, antlerless/fall-turkey exclusions, hog permit/method exceptions, spring hog prohibition, python coverage limits, unpublished-answer protection and repeat-seed/withdrawal preservation. Test publications exist only in disposable test databases and do not constitute human approval of delivered data.
