# Huntit

This project was generated using [Angular CLI](https://github.com/angular/angular-cli) version 22.1.8.

## Development server

To start a local development server, run:

```bash
ng serve
```

Once the server is running, open your browser and navigate to `http://localhost:4200/`. The application will automatically reload whenever you modify any of the source files.

## Code scaffolding

Angular CLI includes powerful code scaffolding tools. To generate a new component, run:

```bash
ng generate component component-name
```

For a complete list of available schematics (such as `components`, `directives`, or `pipes`), run:

```bash
ng generate --help
```

## Building

To build the project run:

```bash
ng build
```

This will compile your project and store the build artifacts in the `dist/` directory. By default, the production build optimizes your application for performance and speed.

## Running unit tests

To execute unit tests with the [Vitest](https://vitest.dev/) test runner, use the following command:

```bash
ng test
```

## Running end-to-end tests

For end-to-end (e2e) testing, run:

```bash
ng e2e
```

Angular CLI does not come with an end-to-end testing framework by default. You can choose one that suits your needs.

## Additional Resources

For more information on using the Angular CLI, including detailed command references, visit the [Angular CLI Overview and Command Reference](https://angular.dev/tools/cli) page.

## Combined Django and Angular setup

HuntIt combines an Angular frontend, a Django REST Framework backend, and a local SQLite database. It supports regulation searches, user accounts, private saved information, and reviewed regulatory publication. Install Python 3.12+ and Node.js 24.15+ in the 24.x series, then run these commands from this folder:

```powershell
python scripts/setup_local.py
npm ci
python scripts/run_local.py
```

Wait for **HuntIt is ready**, then open **https://127.0.0.1:4200/**; the default local development certificate is self-signed. The launcher accepts trusted certificate/key files, and `--http` is available for loopback development and QA. Django Admin is at **https://127.0.0.1:4200/admin/**. Create your own administrator with `.venv\Scripts\python.exe backend/manage.py createsuperuser`; no shared account is included.

Use [the integration guide](docs/INTEGRATION.md) for database setup, security, APIs, and sharing; [the regulatory review pack](docs/REGULATORY_REVIEW.md) for supported scopes and source review; and [the QA report](docs/QA_REPORT.md) for validation. Fresh setup installs **58 current approved regulatory scopes** for four species, including private-land turkey information, four WMAs and specific Fisheating Creek python restrictions. The original 18 curated publications remain as prior revisions, alongside the approved original-data snapshot. Original records and their dates are retained; unknown fields remain unknown where no approved supplement supplies them. Unsupported dates/areas return a clear missing-data response. Future changes require new human review before publication.
