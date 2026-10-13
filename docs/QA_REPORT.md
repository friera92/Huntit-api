# HuntIt QA and SDS coverage

## Git distribution — 2026-10-12

The repository includes `.gitattributes` to preserve source bytes on checkout, including the checksum-protected JSON releases. This prevents Windows line-ending conversion from invalidating approved data checksums. The application code and regulatory data are unchanged from the neutral distribution verified below; this distribution contains 216 files. The publication checkout is checked against the ZIP and exercised with Windows-style Git line-ending settings before delivery.

## Neutral distribution verification — 2026-10-12

- Documentation, fictional test profiles, review descriptions and ignore-file comments use neutral team wording. Five PNG assets had only attribution metadata removed; their remaining chunks, dimensions and compressed image data are byte-identical. Regulatory content, original approval statements and dates are unchanged.
- **239 Django tests passed** in 66.055 seconds, including four new checksum/approval compatibility checks and the existing 782-request expansion matrix. **64 Angular tests passed**; after the final Results test wording update, all **17 Results tests** passed again. Django system and migration-drift checks passed.
- Real prior-release upgrade checks passed for both a full installation and a starter-only installation, seeding twice. Full-install publication and receipt rows remained exact; starter-only setup reached 58 current / 76 total curated publications while retaining the original 18 snapshots and review fields, original-data snapshot and old receipts. Both SQLite integrity checks passed. Stored history and withdrawals are preserved; unknown digests, altered approvals and changed regulatory content remain rejected.
- The exact reviewed expansion JSON and expansion release are unchanged. Current starter and original-data pins reflect descriptive provenance cleanup; only exact earlier approved digests remain compatible. Older QA sections below describe their historical releases before this presentation cleanup.
- Independent release audit passed: 215 safe, unique, CRC-valid files; all packaged bytes match the workspace, with no personal attribution, assistance references, image attribution metadata, databases, accounts, secrets or dependencies distributed. Fresh extracted migration, seed twice, system/schema checks and all release/review pins passed. Confirmed 58 current / 76 total curated publications, one original-data publication, three receipts, four species and zero account/personal state. All map links are clean; SQLite integrity is `ok` with zero foreign-key violations. Final documentation updates are repackaged and byte-checked before delivery.

## Source-link cleanup verification — 2026-10-12

- Removed tracking queries from four setup-fixture map links and the four corresponding approved-release links. A structured comparison against the prior ZIP confirmed that all regulatory fields and original approval statements/dates are unchanged; only those links and a separate distribution-cleanup record differ. The starter approval, expansion approval and exact expansion review artifacts are byte-identical.
- **235 Django tests passed**, including six new compatibility regressions; the suite also exercises the existing 782-request expansion boundary matrix. The focused original-data release suite passed all **21 tests**. Django system check and migration-drift check passed.
- Existing installations accept only the exact prior or cleaned approval digest, keep stored snapshots and receipts intact, preserve withdrawals, reject unknown digests, and return cleaned map links from a copy. Tests also check preservation of unrelated query strings and fragments. Fresh installations use the cleaned pinned release.
- Fresh extracted-ZIP migration, seed twice, system and migration-drift checks passed. Confirmed 58 current / 76 total curated publications, one approved original-data publication, three receipts, four species and zero users, sessions, admin logs or personal rows. All four working-zone links and all four returned approved-zone links are clean. SQLite integrity is `ok` with zero foreign-key violations. ZIP integrity, safe paths, 215 packaged files and absence of the removed tracker passed; final packaged bytes are checked against the workspace after documentation updates.
- No frontend code changed for this cleanup. Earlier Angular, build, browser and launcher results below remain historical evidence for unchanged code.

## Fresh Windows installation startup correction — 2026-10-12

- The user completed setup and `npm ci`, but Django alone was reachable and the original launcher announced the URL before Angular listened. The same Angular installation built successfully with first-run prompts disabled. The exact stalled prompt was not captured; see [STARTUP_FIX_REPORT.md](STARTUP_FIX_REPORT.md).
- Corrected `scripts/run_local.py` to disable interactive CLI setup prompts, forward labeled output safely on Windows cp1252 terminals, reject occupied ports and wait for both listeners before announcing readiness. Early exits and a 180-second timeout report errors and clean up the other server. HTTPS remains the default.
- **Nine isolated launcher regressions passed**, including a real cp1252 output stream and multiple Unicode-bearing log lines. No application database is involved in these tests.
- The corrected script was exercised in the actual fresh Downloads installation with Windows Python 3.13: both servers started, Angular built in 1.883 seconds, and the ready message appeared after both ports opened. HTTPS frontend and API returned 200, and admin returned its expected 302 login redirect. These requests validated the generated server certificate and hostname using an explicit local trust root.
- The test launcher was stopped after verification. The downloaded installation's database/accounts and application code were preserved; only its launch script was replaced. The distributable includes the correction and report. Previous application/data QA below remains historical evidence for unchanged application code, not a claim that all suites were rerun for this launcher-only correction.

## Approved publication release verification — 2026-10-12

The project owner checked the expansion sources and approved local publication with **“Sources checked — approve local publication.”** The exact reviewed JSON is pinned to SHA-256 `f54de4a3edbf240c5c20f8f6fc88fcb054dc64053dc227b544d2fc48d239374c`; see [DATA_EXPANSION_APPROVAL.md](DATA_EXPANSION_APPROVAL.md). The original review artifacts and two earlier approval files remain unchanged.

- **229 Django tests passed** (74.2 seconds), including 14 new frozen-publication regressions. **64 Angular tests passed** across 10 files. Production build passed (459.20 KB initial bundle), with the two existing CSS budget warnings. Django system and migration-drift checks passed.
- The actual approved defaults passed **782 API boundary requests** covering **58 scopes, 268 periods and 208 distinct open rules**, with 282 closed answers and 28 outside-coverage answers. The matrix uses the distributable approved loader directly. All 18 previous snapshots retain their original content, review timestamps and revision numbers.
- New tests cover release/review hashes, portable catalog IDs and keys, ambiguous identities, complete rollback on draft or publication conflicts, preservation of later reviews and withdrawals, receipt replay protection, and keeping the six linked Fisheating scopes together. Withdrawing newly curated turkey does not revive imported rules as primary guidance.
- The real local database published all 58 approved scopes, preserved the 18 previous revisions and original-data publication, and passed repeat setup with zero additions. Confirmed 58 current / 76 total curated revisions, three receipts, SQLite integrity `ok` and zero foreign-key violations. No reviewer account was created.
- Live browser QA against the real approved local data confirmed completed turkey methods/permits/profile and SR70 selectors, the Fisheating special-opportunity permit and closure after March 12, Corbett's Monday closure, and Holey Land's turkey prohibition. [Approved turkey screenshot](images/qa-approved-expansion-turkey.png). Temporary QA tabs and servers were closed.
- **Independent approved-ZIP audit passed: 212 clean source/documentation files.** Safe unique paths, ZIP integrity, SHA-256 sidecar and every packaged byte matched the workspace. No database, real credentials, keys, dependency folders, caches or account/personal state are distributed. Final comparison against the original ZIPs remains 23 frontend and 9 backend files modified, 127 added and zero original source files removed.
- **Fresh extracted setup passed** using the installed Python toolchain: migrations, seed twice, system check and no migration drift; SQLite integrity `ok` with zero foreign-key errors. Confirmed 58 drafts, 58 current / 76 historical curated publications, one current original-data publication and three receipts. Catalog counts remain four species, 102 original seasons, 78 original periods, 14 bag rules, five notes, seven permits, 32 areas and four regulatory-area choices. Users, sessions, admin logs and every personal table contain zero rows.
- Every fresh-install current snapshot exactly matches the mapped frozen approved pack, and the 18 original revisions retain their exact original bytes. All three release hashes and the reviewed-document hash passed. Eight independent guest checks confirmed complete turkey fall/spring/profile/permits, east/west Fisheating conditions and the east closing date, Corbett's Monday closure/Wednesday opening, and Holey Land's turkey prohibition. All 58 catalog scopes are reviewed. Final archive bytes and tested code/data were rechecked after the documentation-only repack.

## Previous staged data-expansion QA — 2026-10-12

- **215 Django tests passed** (56.3 seconds), including the original account/personal/regulatory suites and new turkey, WMA, Fisheating, install-preservation and public API regressions.
- **64 Angular tests passed** across 10 files. Production build passed with a 459.20 KB initial bundle; the two existing Home/App CSS budget warnings remain.
- **782 public GET boundary requests** over **58 draft scopes, 268 periods and 208 distinct open rules** passed. The matrix observed 282 closed answers and 28 outside-coverage answers. Test publications were created only inside disposable QA databases. All 18 earlier approved snapshots remained byte-identical as prior revisions.
- Django system check and migration drift check passed; no schema migration was needed for this update.
- Repeated setup preserves edited drafts, nonblank catalog values, published histories and withdrawals. The new data never inherits either earlier release's approval. New turkey profile fields become reviewed only through an approved containing snapshot.
- A regression confirms the old broad Fisheating python answer cannot establish year-round east-side permission while the exact regional drafts await human review. The historical immutable records remain intact.
- Independent release audit passed for **206 packaged files**: safe paths, ZIP integrity, every packaged byte matching the workspace, matching SHA-256 sidecar and no databases, account state, secrets, TLS keys, dependencies or caches. Compared with the original ZIPs, 23 frontend and 9 backend files are modified, 121 files are added and no original source is removed.
- Fresh extracted backend checks passed using the installed Python toolchain: migrations, seed twice, system check, migration drift, SQLite integrity and zero foreign-key errors. Confirmed 58 edition drafts; 18 unchanged current curated publications plus one approved legacy snapshot; two receipts; 4 species, 102 original seasons, 78 periods, 14 bag rules, 5 notes, 7 permits, 32 areas and 4 regulatory-area choices; zero users, sessions, admin logs or personal rows. Both earlier approval hashes and the original 292-record fixture are intact. Guest Fisheating is review-needed, while private turkey retains its earlier owner-approved dates pending review of the new requirements.
- Live browser QA confirmed private turkey permits/methods/profile, SR70-only options, weekday-closed Corbett turkey, Fisheating side/permit conditions and closure after March 12, and Dinner Island small-game hog methods/license exemption. At 355 by 812 there was no horizontal overflow; new link contrast was corrected and visually rechecked. See [mobile proof](images/qa-data-expansion-mobile.png), captured from a disposable test database.
- The first frontend run was blocked by sandbox temporary-cache rename permissions, before test execution. It passed after moving the cache into the workspace. Browser QA required loopback-capable execution because the restricted network sandbox blocked Angular's Django proxy. These environment restrictions did not require application security changes.

These results describe the staged expansion before owner approval. The sections below retain older integration QA history. Final approved-release results belong in the publication section above.

## Previous integration QA

Date: 2026-10-12. Reference: supplied SDS Part 1, especially scope/security and user stories US1–US8. Tests use disposable local databases and fictional accounts. No production account or personal data is distributed.

## Automated and release checks

- **150 Django tests passed** across accounts, personal data, regulations and integration (43.5 seconds).
- **61 Angular tests passed** across 10 files; the 14 Results tests also passed after the final verification-label edit. Production build passed (457.18 KB initial bundle).
- Django system check passed and `makemigrations --check --dry-run` reported no drift.
- SQLite migration/seed: 18 current curated publications plus one approved snapshot of the original teammate information, no bundled users, two release receipts; rerun adds zero and preserves existing records/withdrawals.
- HTTPS smoke passed using the actual development certificate as an explicit trust root, with hostname and certificate validation enabled. Checked frontend/API/admin/static routing, HTTPS CSRF registration, Secure/HttpOnly sessions, no-store/referrer headers, approved search and logout. No browser security interstitial was bypassed.
- Independent ZIP integrity, safe extraction and clean-content audit passed: **181 files**, every packaged file byte-identical to the workspace, no databases, credentials, accounts, TLS keys, dependency folders, caches or QA state. See the generated manifest for exact file differences.
- Fresh extracted-release smoke passed using the installed Python toolchain: migrate, seed, system check, migration consistency, repeat seed and SQLite integrity, with zero foreign-key violations. Confirmed state: 18 curated current publications, one current teammate snapshot, two receipts, four catalog species/102 original seasons and zero users/sessions/admin logs/personal rows. Both pinned approval hashes and every original fixture field matched. Original source timestamps stay intact; human approval is recorded separately in immutable snapshots.
- Guest API checks passed for private hog, private/public python, private deer, Corbett and newly available private turkey. Closed dates remain `closed`, unsupported scopes remain `no_data`, and guest export is denied. All approved source URLs are official FWC HTTPS links. Original lockfile, backend requirements and all nine original regulatory migrations are byte-identical.
- A connection-enforced read-only coverage audit made **195 public GET requests**. It reached **102/102 original seasons, 78/78 exact periods and notes, 14/14 bag rules, 5/5 full regulatory notes, and 4/4 species profiles**, checking period starts/ends and the D2 bag exception. WMA hog advice remains an advisory with no open season; undated year-round labels do not extend curated coverage. All original Unicode notes survive in the frozen release.
- New regression tests cover frozen-only joins, future live edits not inheriting approval, withdrawn snapshot preservation, tampered release hashes, date/region requirements, turkey FALL/SPRING limit association, unknown fields, safe rendering and UTC source dates.

Negative-test HTTP 400/401/403/405 messages are expected: they demonstrate invalid data, unauthenticated access, CSRF failures and forbidden mutations being rejected. There were no failed assertions in the final suites. The build retains the original Home/App stylesheet budget warnings. These are warnings, not compilation failures.

## Browser QA

Checked the running Angular/Django application through the browser, using loopback HTTP for UI automation and a separate TLS test for encrypted transport:

- Guest search: species selection, private hog rules, permission warning, missing public area prompt, public python guidance and official source links.
- Deer: private Zone A/DMU A2 changes to Corbett WMA for the same date; different season, bag limits and permits appear. Land changes clear incompatible geography. Outside-coverage dates show no-data rather than permission.
- Accounts: login, session persistence, logout, private route access and returning to the search after login. Backend tests independently cover registration and invalid credentials.
- Personal data: save/reopen a search; save preferences and prefill a new search; create a self-reported license; save a fictional harvest, reload, archive and restore it; export JSON; selectively archive harvests using Settings reset.
- Persistence: preferences, license status and saved search remain after logout/login. Logout while already on Home clears preference-derived selections.
- Mobile: live checks at 390×844 and 355×812. Profile, Settings, Licenses, Log, Home and Results were checked for wrapping/overflow; the confirmed Home land-selector overflow was repaired and rechecked. This is responsive browser QA, not testing every physical phone or browser engine.
- Approved-data update: used Home to select turkey/Zone C, then changed the Results date and SR70 region for spring. Original seasons, appropriate fall/spring limits, closed-period labels, missing requirements, owner-confirmed verification and source links appear. The supplemental section was checked at 355×812 without horizontal overflow. A midnight UTC retrieval date now displays October 7 rather than October 6 in US timezones.

Password changes, administrative resets/deletion/suspension and destructive deletion paths were tested with isolated Django test clients. The browser password form was inspected without changing a real user's credentials.

Evidence: [verified existing records](images/qa-verified-existing-records.jpg), [mobile profile](images/qa-mobile-profile.jpg), [archive/recovery](images/qa-mobile-archive.jpg), [license form](images/qa-mobile-licenses.jpg), [regulatory results](images/qa-mobile-results.jpg), [final mobile search](images/qa-final-search.jpg), [desktop search](images/qa-desktop-search.jpg).

## Requirement mapping

| SDS story | Implementation and evidence |
|---|---|
| US1: guest private-land hog search | Approved hog snapshot, permission handling, year-round dates, license/bag/method guidance and official source; engine tests and live guest search. |
| US2: public python removal | Exact supported-area scopes/names, lawful humane-method summary, anti-cruelty/live-transport alerts and official sources; starter/engine tests and live public-area search. |
| US3: private/WMA/date/location filtering | Home and Results filters; validated zone/DMU relationship, required selectors, per-area/date rules, closed/outside-coverage behavior; unit/API tests and live deer comparison. |
| US4: at least three species with dates | Frozen approved hog/python/deer curated publications plus all original owner-verified records, including private turkey dates/regions; source and verification provenance. Full original-record API coverage audit and release setup checks. |
| US5: authenticated preferences and persistence | Django password hashing/session/CSRF, owner-scoped personal APIs, persisted preferences/licenses/searches, rerunning current approved data; account-isolation and stale-response tests plus logout/login checks. |
| US6: admin-only regulatory changes | Django model permissions, explicit source acknowledgment/notes, publish permission, immutable revision history and restricted public APIs; ordinary/guest mutations and unsupported methods rejected in tests. |
| US7: private harvest log | Species/date/area/quantity/notes persisted per owner, edit/archive/restore/confirmed deletion; cross-account tests and live save/reload/archive/restore. |
| US8: sources and verification | Official source links and last-verified dates per approved payload; clear needs-review/no-data messages; schema/engine/publication tests and browser inspection. |
| Security and architecture | Angular + Django REST Framework + SQLite; hashed passwords, HTTPS launcher/secure cookies, role and owner permissions, private responses not cached, sensitive fields/query logs redacted; dedicated tests and transport check. |
| Additional requested account/data controls | User password change; authorized admin reset/suspend/reactivate/delete; no staff privilege escalation; personal export/selective reset and reversible harvest archive; account/personal/frontend regression tests. |

## Practical limits

The application implements the specified stories for its documented supported dataset. Reviewed dates/scopes are deliberately bounded; missing rules never imply permission. Future FWC changes and additional WMAs/species require ongoing human review. No live FWC license verification, official harvest submission or email password-recovery service is claimed. Forgotten passwords are handled by an authorized project admin. Local development servers are not an Internet production deployment.
