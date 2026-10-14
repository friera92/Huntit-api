# HuntIt

HuntIt combines an Angular frontend, a Django backend and a local SQLite database for Florida hunting regulation searches, user accounts, saved preferences, self-reported licenses and private harvest records.

## Run locally

Install Python 3.12+ and Node.js 24.15+ in the 24.x series. From the project folder in PowerShell:

```powershell
python scripts/setup_local.py
npm.cmd ci
python scripts/run_local.py
```

Keep the terminal open and wait for **HuntIt is ready**, then open **https://127.0.0.1:4200/**. The development HTTPS certificate is self-signed; the launcher also accepts a trusted certificate or `--http` for loopback development. Press Ctrl+C to stop both servers.

Create your own administrator:

```powershell
.\.venv\Scripts\python.exe backend/manage.py createsuperuser
```

Django Admin is at **https://127.0.0.1:4200/admin/**. No shared account is included. Setup creates an independent SQLite database on each computer; databases, passwords, local secrets and dependency folders are not distributed.

## Project guides

- [Setup, accounts, APIs and configuration](docs/INTEGRATION.md)
- [Regulatory coverage and source-review workflow](docs/REGULATORY_REVIEW.md)
- [Requirements and test evidence](docs/QA_REPORT.md)

The approved dataset covers four species within documented locations and dates. Unsupported searches show missing data. Future regulatory changes require human source review before publication. Required data and approval records are retained in `backend/integration/fixtures/`.
