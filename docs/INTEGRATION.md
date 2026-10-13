# Running and sharing the integrated HuntIt project

The original Angular frontend is at the project root. The original Django backend is in `backend/`; its regulatory models and importers remain the foundation. Added `accounts`, `personal`, and `integration` apps supply authentication, private saved information, and a source-review boundary for public regulatory results. No separate backend repository is needed to run this copy.

## Clean local setup

Install **Python 3.12 or newer** and **Node.js 24.15 or newer in the 24.x series**. Verification used Python 3.12.14 and Node.js 24.15.0. Extract the ZIP, open a terminal in the extracted project folder, and run:

```powershell
python scripts/setup_local.py
npm ci
python scripts/run_local.py
```

Setup installs the backend dependencies, applies all migrations, creates `backend/db.sqlite3`, and seeds the regulatory working catalog and three exact human-approved releases. A fresh database contains **58 current curated publications, 76 curated revisions including the original 18, one approved snapshot of the existing teammate information and three installation receipts**. The expansion contains 40 new scopes and 18 approved revisions. The project owner checked its sources and explicitly approved local publication. Repeating setup preserves existing accounts, records, edited drafts, publication history and withdrawals. An existing catalog is not replaced by the fixture.

The launcher starts Django on loopback port 8000 and Angular on port 4200. **Wait for `HuntIt is ready` in the terminal**, then open **https://127.0.0.1:4200/**. The first frontend compilation can take longer. Startup output is labeled `[Django]` or `[Angular]`; the launcher disables first-run Angular prompts and reports a busy port, child-process failure or startup timeout. The default development TLS certificate is self-signed, so the browser asks whether to trust the local site. For a trusted local certificate covering the address you use, supply both files:

```powershell
python scripts/run_local.py --cert "C:\certificates\localhost.crt" --key "C:\certificates\localhost.key"
```

Keep private keys outside the shared project. **Ctrl+C stops both servers.** For loopback development or browser QA only, `python scripts/run_local.py --http` uses http://127.0.0.1:4200/. HTTP mode does not protect traffic in transit and is not the deployment path.

If the browser says **connection refused**, keep the launcher terminal open and check its startup messages. A successful `npm ci` installs dependencies; it does not start the app. Its funding, update and audit notices are not evidence that the local server started or the cause of a refused connection. If a port is occupied, stop the older HuntIt launcher with Ctrl+C before trying again. If startup fails, the error and the labeled server output identify the next issue to address. You do not need to reinstall dependencies or reset your SQLite database merely because the browser could not connect. See [STARTUP_FIX_REPORT.md](STARTUP_FIX_REPORT.md) for the fresh-install launcher correction.

To choose another SQLite file, set an absolute path in an existing directory before setup and launch:

```powershell
$env:HUNTIT_DATABASE = "C:\HuntItData\huntit.sqlite3"
python scripts/setup_local.py
python scripts/run_local.py
```

No database server, credentials, or `.env` file are required for local use. Python, Node, and package installation are still necessary. On macOS/Linux, direct backend commands use `.venv/bin/python`; the scripts select the correct environment path automatically.

## Accounts, private information, and administrator setup

Register through the application to create a hunter account. Profile saves preferred species, areas, and zones; Results saves search inputs; Licenses stores self-reported statuses; Harvest Log records private harvests. These workflows persist across sign-out/sign-in and enforce ownership in the backend. A saved search reads the current approved dataset for its saved date and location instead of storing an old regulatory answer. The harvest log does not submit an official FWC harvest report or verify a license.

Account & Data Settings supports password changes, a private JSON export, and selective reset. Reset can clear preferences, searches, and license records; it archives harvests so they remain recoverable. Harvest Log can restore archived entries or permanently remove one after a separate confirmation. Password changes preserve the current browser session and invalidate other sessions using the old password.

Create your own administrator; no administrator account or shared password is shipped:

```powershell
.\.venv\Scripts\python.exe backend/manage.py createsuperuser
```

With the default HTTPS launcher, open **https://127.0.0.1:4200/admin/** so admin pages and assets use the same TLS proxy. In HTTP development mode the admin is http://127.0.0.1:8000/admin/.

Django Admin provides regulatory editing and account management. Authorized account administrators can reset passwords, suspend a user by clearing **Active**, reactivate users, and delete accounts with confirmation. Account deletion cascades that user's personal records; reviewed regulatory snapshots survive with an empty reviewer reference. Support staff cannot promote accounts, modify another staff account, or delete themselves. A superuser controls staff status and permission assignments. Designated regulatory reviewers need staff status, draft view/change permissions, and **Can review and publish regulatory snapshots**.

## Regulatory data and reviewed publication

The distributed setup fixture and approved original-data release use cleaned official map links without tracking queries. The loader recognizes the exact prior approved checksum for existing installations, preserves immutable history and withdrawals, and returns cleaned links for older snapshots. The regulatory content and original approval dates remain unchanged; see [SOURCE_LINK_CLEANUP.md](SOURCE_LINK_CLEANUP.md).

The approved expansion completes missing private-turkey information and publishes all-four-species coverage for Corbett, Holey Land, Rotenberger and Dinner Island Ranch, plus distinct east/west Fisheating python restrictions. Some area/species combinations are explicit prohibitions. [DATA_UPDATE_REPORT.md](DATA_UPDATE_REPORT.md) explains exact changes, and [DATA_EXPANSION_APPROVAL.md](DATA_EXPANSION_APPROVAL.md) records the separate owner source-review approval. The original [review pack](DATA_EXPANSION_REVIEW.md) preserves its regulatory content with neutral team wording; its pending-status wording describes its pre-approval state. A guard prevents the known-overbroad historical Fisheating answer from resurfacing. All 32 catalog areas have official reference links, but that does not imply all species' seasons are complete for all 32.

Fresh setup imports the **292 original regulatory/catalog records**, containing four catalog species, installs the first **18 approved starter publications**, then installs the original-data snapshot and exact approved expansion. Curated coverage includes **wild hog, Burmese python, deer and turkey on private land; the specified public-python areas; all four species at the four documented WMAs; and east/west Fisheating python restrictions**. Matching original data is also included following the earlier owner verification confirmation, including **20 private-land turkey seasons** using fall hunting zones and spring/youth regions north or south of SR70. Other species/area/date combinations can return no reviewed data. This is a supported-scope application, not exhaustive coverage of every Florida hunting area.

**All three fixed releases were separately approved on 2026-10-12.** The project owner first confirmed reviewing the curated sources, then stated: “include existing information on search result, all existing information has been verified.” For the exact expansion, the project owner subsequently stated: **“Sources checked — approve local publication.”** No reviewer account is bundled. Setup does not approve arbitrary working data, future imports or later draft edits.

The starter release is [`fwc-2026-10-12-v1`](../backend/integration/fixtures/approved_regulations_2026_10_12.json). The supplemental original-data release is [`teammate-information-2026-10-12-v1`](../backend/integration/fixtures/approved_teammate_information_2026_10_12.json). The new release `fwc-data-expansion-2026-10-12-v1-approved` is frozen in [`approved_data_expansion_2026_10_12.json`](../backend/integration/fixtures/approved_data_expansion_2026_10_12.json); its [approval record](DATA_EXPANSION_APPROVAL.md) pins the exact review content and complete release. Setup invokes the release loaders, checks pinned SHA-256 values, maps catalog identities and records one-time receipts. `seed_local_data` runs `load_approved_expansion` last. Its preflight checks all 58 scopes: a working payload/title/species/land-type conflict stops the entire atomic expansion install without overwriting edits. Later separately reviewed publications and withdrawals are preserved, and the receipt prevents replay. The two broad python scopes and four precise Fisheating replacements are preserved together if any member has a withdrawal or later reviewed publication. Ambiguous identities or altered release bytes stop installation. An incomplete existing catalog causes only the supplemental original-data release to be skipped with a missing-identity message; reconcile it and run `load_approved_legacy_release` explicitly. Original source timestamps remain intact, including missing original verification dates; the supplemental snapshot separately records the owner verification confirmation. It does not represent a new source-by-source audit.

Results show matching approved seasons, periods, limits, exceptions, notes, habitat, behavior and hunting tactics. Curated answers remain primary where available, including the newly approved turkey requirements/profile and WMA rules; original records appear in **Additional Verified Project Records**. Closed periods are labeled, any remaining unknown fields stay unknown, and WMA advisories never establish an open season. Undated imported year-round labels do not extend the explicit coverage of curated publications.

For every future regulatory change, an authorized reviewer must compare the draft with its linked FWC sources, correct it as needed, acknowledge the source check, enter review notes, and choose **Publish reviewed revision**. Source collection does not replace that human approval. Saving a draft or running an importer cannot approve an update. Follow the detailed source pack and workflow in [REGULATORY_REVIEW.md](REGULATORY_REVIEW.md).

Public searches read immutable approved snapshots. A new draft edit or import cannot alter a published answer until a new review creates a replacement revision or separately approved imported release. Administrators can withdraw curated answers or the supplemental imported publication while retaining history; setup does not reactivate them. Results distinguish reviewed records, closed seasons, drafts awaiting review and missing coverage. They display official references and verification dates when available; unsupported results direct users to the official source and do not establish hunting permission.

Guest searches are not saved as personal histories. Authentication uses Django password hashing, sessions, validation, throttling, and CSRF protection. Angular sends relative requests through the local proxy and echoes `csrftoken` in `X-CSRFToken`; credentials are not stored in browser local storage. Account/personal/admin responses are private and not cached, and application request logs redact query values.

## API reference

Use the trailing slash shown below. Public endpoints accept GET/HEAD/OPTIONS. Personal endpoints require a signed-in session; all mutations require a valid CSRF token. Personal lists are JSON arrays. Each detail operation resolves records through the current owner; another user's record returns 404.

| Endpoint | Methods and purpose |
| --- | --- |
| `/api/species/` | GET active catalog species |
| `/api/catalog/` | GET land types, zones, DMUs, areas, permits, and supported coverage |
| `/api/regulations/search/` | GET the current reviewed result for the selected inputs |
| `/api/auth/csrf/` | GET a CSRF token and cookie |
| `/api/auth/register/` | POST username, email, password, password_confirm; creates a hunter session |
| `/api/auth/login/`, `/api/auth/logout/` | POST starts or ends a session |
| `/api/auth/me/` | GET current account; 401 when signed out |
| `/api/auth/password/change/` | POST current_password, new_password, new_password_confirm |
| `/api/personal/preferences/` | GET/PUT species, managed_areas, zones arrays |
| `/api/personal/licenses/` | GET list; POST a self-reported license |
| `/api/personal/harvests/` | GET active list; POST a harvest; `?archived=true` lists archived entries |
| `/api/personal/saved-searches/` | GET list; POST search inputs |
| `/api/personal/{licenses,harvests,saved-searches}/<id>/` | GET/PATCH/DELETE an owned record |
| `/api/personal/saved-searches/<id>/run/` | GET a fresh result from current approved records |
| `/api/personal/harvests/<id>/archive/`, `.../restore/` | POST archive or restore an owned harvest |
| `/api/personal/export/` | GET a JSON attachment of all the owner's personal information, including archived harvests |
| `/api/personal/reset/` | POST selective reset with explicit confirmation |

Search requires `species`, `land_type`, and `date` (`YYYY-MM-DD`). Optional inputs are `zone`, `dmu`, `regulatory_area`, `managed_area`, and `landowner_permission`. Public searches require a managed area; reviewed location-specific rules can require a zone or DMU. The interface requests missing information and preserves search filters in the URL. Saved searches use `hunting_date` in place of `date`.

Reset requires `preferences`, `saved_searches`, and `licenses` booleans, `harvests` set to `archive` or `keep`, and `confirmation` equal to `RESET MY DATA`. It returns counts and never deletes harvests. Export contains personal content and should be stored privately; it contains no passwords or session tokens.

## Sharing, upgrades, and configuration

Share source, migrations, the clean fixture, and the review drafts. Do not share the SQLite database, `.local-secret-key`, `.env` secrets, private TLS keys, virtual environment, dependency folders, or QA files. Each developer's database is independent; changes do not synchronize between copies. Keep a private backup of an existing database before upgrades.

Original regulatory migrations `0001` through `0009` are retained; `0010` adds integrity checks. Personal migrations `0001` through `0003` create private records, saved permission inputs, and harvest archiving; integration migrations `0001` and `0002` add review drafts, publication history, and the approved-release installation receipt. The original `0009` migration replaces the old WMA structure without copying its data: databases still on `0008` need a separate reviewed preservation upgrade. The supplied setup is verified against a fresh database; do not replace or merge another developer's old database/migration directories blindly.

A unique local Django secret is generated in ignored `backend/.local-secret-key`. Deployment requires `DJANGO_DEBUG=false`, a private `DJANGO_SECRET_KEY`, `DJANGO_ALLOWED_HOSTS`, and appropriate `DJANGO_CSRF_TRUSTED_ORIGINS`. Secure cookies, HTTPS redirects, and HSTS apply with debug disabled. Set `DJANGO_TRUST_PROXY_SSL=true` only behind a trusted proxy that controls the forwarded-protocol header; the local HTTPS launcher sets its own loopback proxy mode. A public deployment additionally needs a real TLS certificate, a production application server/reverse proxy, static-file serving, and backups. The supplied launcher hosts local development servers.

## Validation

Run from the project root:

```powershell
.\.venv\Scripts\python.exe backend/manage.py check
.\.venv\Scripts\python.exe backend/manage.py makemigrations --check --dry-run
.\.venv\Scripts\python.exe backend/manage.py test accounts personal regulations integration
npm test -- --watch=false
npm run build
```

The tests use synthetic publications to exercise approval and verify the fixed approved-release bootstrap separately. They do not approve later edits. See [QA_REPORT.md](QA_REPORT.md) for the release's actual automated/browser results and [TEAM_REPORT.md](TEAM_REPORT.md) for ownership and code-change details. Every future regulatory update still requires an administrator's human source review before publication.
