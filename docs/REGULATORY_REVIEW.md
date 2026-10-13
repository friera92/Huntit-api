# Regulatory data and source maintenance

Public answers use approved, immutable snapshots; edits and imports cannot publish themselves. Setup installs **58 current curated scopes and 76 curated revisions**, including 18 starter revisions, plus an approved snapshot of **292 original regulatory/catalog records**. Repeat setup preserves existing data, later reviews and withdrawals.

## Supported coverage

The four species are wild hog, Burmese python, white-tailed deer and wild turkey. Curated coverage includes private-land rules, specified public-python areas, and all four species at J. W. Corbett, Holey Land, Rotenberger and Dinner Island Ranch. Some combinations explicitly prohibit take. Dinner Island's separately regulated Caracara Unit is excluded.

The original 18 scopes comprise **one private hog, three python, twelve private-land deer DMU and two Corbett deer selector scopes**. The expansion adds 40 scopes and 18 replacements. Public-land selector aliases do not increase area coverage. The 32-area catalog is a directory, not exhaustive species/date coverage. Missing data never establishes permission.

Fisheating Creek python rules distinguish east and west of U.S. 27. West-side year-round removal excludes firearms, airguns, bows and crossbows outside permitted hunting seasons; gun use requires the applicable management-area permit. East-side coverage is limited to the designated Special-Opportunity Spring Turkey Area, March 6–12 or March 20–26, 2027, with the relevant Special-Opportunity Spring Turkey Permit. The older broad year-round answer cannot override these exceptions. Current closures and superseding rules still require checking.

## Approved release evidence

Paths below are relative to the project root. Times record when approval was recorded on **2026-10-12**, in UTC; no reviewer account is distributed.

| Frozen fixture | Role | Approval recorded |
|---|---|---|
| `backend/integration/fixtures/approved_regulations_2026_10_12.json` | Original 18 source-reviewed starter scopes | 19:19:10 |
| `backend/integration/fixtures/approved_teammate_information_2026_10_12.json` | Confirmed verification and inclusion of all 292 original records | 19:59:07 |
| `backend/integration/fixtures/approved_data_expansion_2026_10_12.json` | Exact 58-scope reviewed expansion | 21:44:55 |

The exact reviewed JSON remains in the expansion's **`review` object**, SHA-256 `f54de4a3edbf240c5c20f8f6fc88fcb054dc64053dc227b544d2fc48d239374c`. Metadata retains the historical filename `docs/DATA_EXPANSION_REVIEW.json`; this duplicate is no longer distributed or needed at runtime. Draft-status wording describes its pre-approval state; `approval` records subsequent approval. Loaders enforce pinned hashes and unambiguous catalog identities.

## Reviewing future changes

1. Check draft dates, limits, methods, permits and exceptions against official sources; keep source URLs and verification dates accurate.
2. In Django Admin, the reviewer needs draft view/change permissions and **Can review and publish regulatory snapshots**. Acknowledge checking sources, enter notes and select **Publish reviewed revision**. Saving/importing alone does not publish.
3. **Withdraw selected drafts' current published answers** removes answers while retaining history; setup does not reactivate them. Future revisions require fresh review.

Official starting references: [FWC hunting regulations](https://myfwc.com/hunting/regulations/), [WMA brochures](https://myfwc.com/hunting/wma-brochures/), [python removal](https://myfwc.com/wildlifehabitats/nonnatives/python/removing/) and [humane-killing guidance](https://myfwc.com/wildlifehabitats/nonnatives/python/humane-killing-methods/). Each approved payload retains its more specific source links.

Generate a working review pack from the project root with `.venv\Scripts\python.exe backend/manage.py export_data_review --output-dir review-output`. The JSON/Markdown export does not approve or publish data. See [INTEGRATION.md](INTEGRATION.md) for setup and [QA_REPORT.md](QA_REPORT.md) for acceptance evidence.
