# Fresh-install startup correction

Prepared October 12, 2026. No changes committed or pushed.

## Observed problem

On the downloaded fresh installation, backend setup and `npm ci` had completed successfully. Django answered on loopback port 8000, but Angular never listened on port 4200 during more than three minutes of observation. The browser therefore reported `ERR_CONNECTION_REFUSED`. The old launcher printed the application address immediately after starting its child processes, before confirming either server was ready.

Starting the same Angular installation on a separate test port with first-run prompts disabled and output captured produced a successful build in 2.235 seconds. This supports an interactive Angular CLI startup prompt as the likely trigger; the exact stalled prompt was not captured and is not established. The npm funding, version-update and dependency-audit notices did not explain the missing listener.

## Focused changes

- **`scripts/run_local.py`:** disables Angular analytics, forced terminal and autocomplete prompts for the child process; supplies closed standard input; forwards Django and Angular output with labels; checks for occupied ports before launching; and waits for both servers before printing `HuntIt is ready`. Output remains readable on Windows terminals whose encoding cannot display Angular's Unicode symbols. A child-process failure or 180-second startup timeout produces an explicit error and stops the other process. Default HTTPS, optional certificate arguments and `--http` loopback mode are retained.
- **`scripts/test_run_local.py`:** nine isolated regression tests cover first-run environment settings, readiness, occupied ports, startup exits, timeout, labeled output and Windows cp1252 log handling.
- **`docs/INTEGRATION.md`:** explains the readiness message, first compilation, labeled logs and connection-refused troubleshooting.
- **`docs/DATA_UPDATE_REPORT.md`:** links to this correction so the main handoff report includes it.

The correction does not change teammates' Angular application components, Django application behavior, the SQLite schema, personal records or approved regulatory data. Existing installations do not need a database reset or repeat dependency installation to use the corrected launcher.

## Verification

- All **nine launcher regression tests passed** using `python -m unittest discover -s scripts -p test_run_local.py -v`. Tests use mocks or in-memory streams and do not change the database.
- The corrected launcher was copied to the user's actual fresh installation at the extracted `HuntIt-integrated` project folder under Downloads. No account, database or application source was replaced. Its Windows Python 3.13 environment started Django and Angular successfully; the Angular build took 1.883 seconds, and the launcher printed its ready message only after both listeners opened.
- HTTPS checks using the generated local certificate as an explicit trust root returned **200** for the frontend, **200** for `/api/species/`, and the expected **302** login redirect for `/admin/`. Certificate and hostname validation remained enabled.
- The test launcher was stopped after verification so the user can start the app from their own PowerShell window. No background test server is intentionally left running.
- Only the launcher, its tests and explanatory documentation changed. The approved regulatory release files, schema, dependency lockfile and teammates' application components remain unchanged by this correction. The clean ZIP and checksum were rebuilt; see [QA_REPORT.md](QA_REPORT.md).
