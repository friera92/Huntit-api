# Running HuntIt

The Angular frontend is at the project root; Django is in `backend/`. Start with the [project README](../README.md).

## Local setup

Install Python 3.12+ and Node.js 24.15+ in the 24.x series. From the extracted project folder, run:

```powershell
python scripts/setup_local.py
npm ci
python scripts/run_local.py
```

Setup installs backend dependencies, applies migrations, creates `backend/db.sqlite3`, and loads the approved regulatory releases. Repeating setup preserves accounts, personal records, edited drafts, publication history and withdrawals.

Wait for **HuntIt is ready**, then open **https://127.0.0.1:4200/**. Keep the terminal open; Ctrl+C stops both servers. The first compilation can take longer. Startup errors identify a busy port, failed process or timeout. If a port is occupied, stop the older launcher before retrying.

The default development certificate is self-signed. To use a trusted certificate covering the address you open:

```powershell
python scripts/run_local.py --cert "C:\certificates\localhost.crt" --key "C:\certificates\localhost.key"
```

Keep private keys outside the shared project. `python scripts/run_local.py --http` serves loopback development at http://127.0.0.1:4200/.

No database server or `.env` file is needed locally. To choose another database, set `$env:HUNTIT_DATABASE` to an absolute file path in an existing directory before setup and launch. On macOS/Linux, direct backend commands use `.venv/bin/python` instead of `.venv\Scripts\python.exe`.

## Accounts and administration

Register through the app. Preferences, saved searches, self-reported licenses and harvests belong to the signed-in user. Settings supports password changes, private JSON export and selective reset. Reset archives harvests; Harvest Log can restore them or permanently delete a separately confirmed entry. License entries do not verify licenses, and the log does not submit official FWC reports.

Create your own administrator:

```powershell
.\.venv\Scripts\python.exe backend/manage.py createsuperuser
```

Open **https://127.0.0.1:4200/admin/**. In HTTP mode, use http://127.0.0.1:8000/admin/. Account administrators can reset passwords, suspend/reactivate users and delete accounts. A superuser assigns staff permissions. Account deletion removes the user's personal records while retaining regulatory review history.

For regulatory updates, compare drafts with their official sources, correct the content, acknowledge the source check, enter review notes and choose **Publish reviewed revision**. Saving or importing alone does not publish. Withdrawals retain history. See the [regulatory guide](REGULATORY_REVIEW.md) for coverage and maintenance.

## API

Use trailing slashes. Account and personal mutations require CSRF; personal endpoints also require a signed-in session and enforce record ownership. List responses are JSON arrays.

| Endpoint | Purpose |
|---|---|
| `/api/species/`, `/api/catalog/` | GET species and location choices |
| `/api/regulations/search/` | GET reviewed results |
| `/api/auth/csrf/`, `/api/auth/me/` | GET CSRF cookie or current user |
| `/api/auth/register/`, `/api/auth/login/`, `/api/auth/logout/` | POST account/session actions |
| `/api/auth/password/change/` | POST current password and confirmed new password |
| `/api/personal/preferences/` | GET/PUT preferences |
| `/api/personal/{licenses,harvests,saved-searches}/` | GET list or POST a record |
| `/api/personal/{licenses,harvests,saved-searches}/<id>/` | GET/PATCH/DELETE an owned record |
| `/api/personal/saved-searches/<id>/run/` | GET current results for saved inputs |
| `/api/personal/harvests/<id>/{archive,restore}/` | POST archive/restore |
| `/api/personal/export/`, `/api/personal/reset/` | GET private JSON export / POST selective reset |

Search requires `species`, `land_type` and ISO `date`; optional fields are `zone`, `dmu`, `regulatory_area`, `managed_area` and `landowner_permission`. Public searches require an area; particular rules can require additional geography. Saved searches use `hunting_date` instead of `date`.

## Sharing and configuration

Share source, migrations, fixtures and lockfiles. Exclude local databases, accounts, `.local-secret-key`, `.env` secrets, TLS keys, dependency folders and caches. Each installation has an independent database; back it up before upgrades. Databases still on the original `regulations.0008` migration need a reviewed data-preservation upgrade before `0009`, which replaces the older WMA structure without copying its data.

Deployment requires `DJANGO_DEBUG=false`, a private `DJANGO_SECRET_KEY`, `DJANGO_ALLOWED_HOSTS` and suitable `DJANGO_CSRF_TRUSTED_ORIGINS`. Enable `DJANGO_TRUST_PROXY_SSL=true` only behind a trusted proxy controlling the forwarded-protocol header. Use a production application server, TLS, static-file serving and backups for public hosting. The supplied launcher runs local development servers.

## Validation

```powershell
.\.venv\Scripts\python.exe backend/manage.py check
.\.venv\Scripts\python.exe backend/manage.py makemigrations --check --dry-run
.\.venv\Scripts\python.exe backend/manage.py test accounts personal regulations integration
npm test -- --watch=false
npm run build
```

See [QA and requirements](QA_REPORT.md) for verification and the PDF requirement mapping.
