# Wild turkey additions — source review worksheet

**Status: human-approved for local publication on October 12, 2026.** The project owner checked the sources and stated **“Sources checked — approve local publication.”** The exact approved expansion and provenance are pinned in [DATA_EXPANSION_APPROVAL.md](../DATA_EXPANSION_APPROVAL.md). Source checks: **October 12, 2026**. Edition: **2026–2027**. The worksheet below retains its original working-draft terminology and review instructions as source-review history; those instructions apply again to future changes. Existing imported records and their earlier owner-approved frozen release are unchanged.

`backend/integration/turkey_data.py` creates six private-land drafts with 20 rules and 23 explicitly bounded periods. Four fall drafts use Zone A–D; two spring drafts use the north/south State Road 70 boundary. Fall review coverage ends January 31, 2027; spring coverage runs February 1–June 30, 2027. The coverage split prevents asking for a fall zone during a spring-only lookup. A closed day remains a closed answer within that edition.

| Official FWC source | Fields checked |
|---|---|
| [2026–2027 seasons](https://myfwc.com/hunting/season-dates/) | All private fall/weapon and regional spring periods, bearded/gobbler category, daily and combined season limits; the page explicitly excludes WMA schedules. |
| [Licenses and permits](https://myfwc.com/license/recreational/hunting/) | Hunting license, Turkey Permit and weapon-season permits. |
| [Exemptions](https://myfwc.com/license/recreational/do-i-need-one/) | Conditional age/residency/homestead/disability/military/preserve exemptions. |
| [General information](https://myfwc.com/hunting/regulations/general-information/) | Fall versus spring hours, private access, evidence of legal harvest and carcass transfer labels. |
| [Taking game](https://myfwc.com/hunting/regulations/taking-game/) | Legal equipment, projectile thresholds, feeding-station buffer, prohibited turkey methods and road restrictions. |
| [Harvest reporting](https://myfwc.com/hunting/deer/harvest-report/) | Log before movement, earliest reporting deadline, confirmation number; this FWC page covers both deer and wild turkey. |
| [2027 youth hunts](https://myfwc.com/hunting/get-started/youth-turkey-hunting/) | Four-day regional youth dates, age/supervision, participating-adult permits and shared spring limit. |
| [Species profile](https://myfwc.com/wildlifehabitats/profiles/birds/game-birds/wild-turkeys/) | Scientific name, Florida subspecies, habitat and behavior, using concise original summaries. |
| [Getting started](https://myfwc.com/hunting/turkey/get-started/) | Scouting/patience supplement and links for safe turkey hunting. |

The 2027 youth ranges are **February 26–March 1 south of SR70** and **March 12–15 north of SR70**, confirmed on both the edition's season page and the youth page. Do not shorten these to two days based on earlier seasons. Fall Zone D's crossbow period has a gap and resumes; its late deer muzzleloading period is not a turkey season. Zone A fall turkey starts October 5 rather than the earlier deer general-gun opening.

Added species information is stored inside each draft payload as a source-linked `species_information` supplement. It does not overwrite the original Species record or the earlier frozen owner approval. Only the reviewed snapshot can supply reviewed profile additions to public answers.

Administrator review should confirm the linked edition, all selectors and date bounds, lawful harvest category, permits/exemptions, hours, reporting and restrictions before publication. WMA quotas and area-specific restrictions are handled in separate named-area data; these private-land drafts must not be used as WMA regulations. Future editions require a new source check rather than copying these dates forward.

Targeted QA: `python manage.py test integration.test_turkey_data`. Tests exercise open/closed endpoints, fall/deer differences, split crossbow periods, the SR70 selector, all youth endpoints, permits/methods/hours/reporting, publication isolation, non-destructive repeat seeding and out-of-edition dates.
