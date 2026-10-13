# HuntIt validation

Documentation cleanup verification: the 193-file release retains three guides. Fresh migration, seed twice, system/schema checks, SQLite integrity, public API smoke and packaging checks passed without the removed review exports. Setup reproduces 58 current/76 total curated publications, one original-data publication, three receipts and zero accounts/personal records. All local documentation links resolve; default packaging does not recreate the change manifest. Application code, approved fixtures and public assets are unchanged from the tested baseline.

Baseline verified on 2026-10-12 before documentation cleanup: **239 Django tests, 64 Angular tests, the final 17-test Results subset and 9 launcher tests passed**. The approved-data matrix passed **782 API requests across 58 scopes and 268 date periods** (`backend/integration/test_expansion_public_matrix.py`). Production build, Django system/schema checks, fresh installation and prior-release upgrade checks passed. Tests use disposable databases and fictional accounts.

## SDS acceptance evidence

Test paths below are relative to `backend/`; frontend tests are in `src/app/`.

| Story | Coverage and test evidence |
|---|---|
| US1: private-land hog | Permission, license exemptions and official sources: `integration/test_publication.py`. |
| US2: python removal | Humane methods and public-area restrictions: `integration/test_publication.py`, `integration/test_python_area_data.py`. |
| US3: land/date/location rules | Required selectors, zone/DMU validation, seasons and limits: `integration/test_data_expansion_engine.py`; `results/results.spec.ts`. |
| US4: baseline species data | Four species, dated approved rules and repeatable seed: `integration/test_bootstrap.py`, `integration/test_approved_expansion.py`. |
| US5: accounts and preferences | Hashed passwords, login, persistence, ownership and current saved-search results: `accounts/tests.py`, `personal/test_api.py`. |
| US6: protected regulation updates | Admin permissions and explicit publication: `integration/test_publication.py`. |
| US7: private harvest log | Persistence, isolation, archive/restore and deletion: `personal/test_api.py`. |
| US8: source transparency | Sources, verification dates and missing-data responses: `integration/tests.py`, `integration/test_legacy_search.py`. |

Authentication, CSRF, private-data access and account administration also have dedicated account/personal regression tests. Desktop and mobile browser workflows were checked, including narrow-screen overflow.

## Limits

Coverage is bounded to documented species, areas and dates; the 32-area directory is not complete statewide regulatory coverage. Future rules require source review. License status is self-reported; there is no official harvest submission or email password recovery. The build retains two stylesheet size-budget warnings. Local development hosting is not a production deployment.
