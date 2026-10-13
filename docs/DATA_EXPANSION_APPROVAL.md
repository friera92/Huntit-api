# HuntIt data expansion — local publication approval

The project owner checked the FWC sources and explicitly approved the exact expansion for publication in the local app and shared ZIP:

> Sources checked — approve local publication

The approval was recorded at **2026-10-12 21:44:55 UTC**. This is the time the approval was recorded, not an assertion of the exact message-send time. The approval does not authorize a GitHub push; nothing was committed or pushed.

## Exact approved content

- Reviewed edition: `fwc-data-expansion-2026-10-12-v1`.
- Approved release ID: `fwc-data-expansion-2026-10-12-v1-approved`.
- Reviewed regulatory JSON: [DATA_EXPANSION_REVIEW.json](DATA_EXPANSION_REVIEW.json).
- Reviewed JSON SHA-256: `f54de4a3edbf240c5c20f8f6fc88fcb054dc64053dc227b544d2fc48d239374c`.
- Human-readable review pack: [DATA_EXPANSION_REVIEW.md](DATA_EXPANSION_REVIEW.md).
- Frozen publication artifact: [approved_data_expansion_2026_10_12.json](../backend/integration/fixtures/approved_data_expansion_2026_10_12.json).
- Complete frozen publication SHA-256: `79f6028abb74d8c7a2eeccad3509ffcdd783141218ca72cf19990b8dd7c021cf`.

The frozen publication contains the reviewed JSON content and separate approval provenance. The reviewed regulatory content, original approval statements and approval dates are preserved. The human-readable pack uses neutral team wording in this distribution; its historical pending-status language describes the review stage, and this approval record establishes the subsequent publication status. Documentation and release provenance may have new distribution hashes after presentation-only cleanup. Neither earlier approval was reused for the new data.

## Scope and behavior

This approval covers **58 curated scopes: 40 new scopes and 18 replacement revisions**, containing 268 explicit date periods. It includes the four existing species within the documented dates and locations; all-four-species coverage at J. W. Corbett, Holey Land, Rotenberger and Dinner Island Ranch; private-turkey requirements/profile; and precise east/west Fisheating Creek python restrictions. Some combinations are explicit prohibitions. Alternate public-land selectors repeat the same area facts rather than increasing the number of areas. Dinner Island's separately regulated Caracara Unit remains excluded.

Fresh setup installs the exact approved release with 58 current curated publications, 76 curated revisions including the original 18, one current frozen original-data publication and three installation receipts. It creates no user or reviewer account. Each developer receives an independent SQLite database. `seed_local_data` runs `load_approved_expansion` last, after the two earlier release loaders.

The expansion loader checks the pinned release and reviewed-content hashes, and preflights all 58 scopes before an atomic installation. A conflicting working payload, title, species or land type stops the entire installation without overwriting the conflict. Later separately reviewed publications and withdrawals are preserved; a one-time receipt prevents replay. The two broad python scopes and four precise Fisheating replacements are preserved as a group if any member has a withdrawal or later reviewed publication. Future imports or edits do not inherit this approval and require a new human source review.

The guard against the historical overbroad Fisheating answer remains in place so it cannot resurface if a precise replacement is withdrawn. Original supplemental records and prior publication bytes remain available as history; they do not override the approved area exceptions.

The approved content is published in the real local database: 58 current scopes, with all 18 earlier snapshots preserved as history. Repeated setup changed no approved answer. Post-publication QA passed 229 backend and 64 frontend tests, the 782-request API matrix, build/schema checks and live guest browser checks. The independent 212-file ZIP audit and fresh extracted migration/seed-twice checks also passed, reproducing the exact approved snapshots with zero bundled accounts or personal rows. See [DATA_UPDATE_REPORT.md](DATA_UPDATE_REPORT.md) for a short teammate-facing explanation and [QA_REPORT.md](QA_REPORT.md) for verification details.
