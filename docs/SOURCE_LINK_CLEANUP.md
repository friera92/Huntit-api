# Source-link tracking cleanup

The project owner requested removal of non-regulatory tracking from the distributed FWC map links. Four hunting-zone links in the setup fixture and the corresponding four links in the approved original-data release now use the same official map address without the tracking query. No season, species, permit, bag limit, method, source destination or human approval date changes.

The approved release records this distribution-only cleanup separately from its original human approval. Its historical upstream fixture digest remains provenance for the original supplied bytes. The cleaned distribution has its own pinned digest in `backend/integration/legacy_release.py`.

Fresh installations load the cleaned links. Existing installations recognize only the current digest and exact earlier approved digests; arbitrary digests are still rejected. Existing immutable publication history, installation receipts and withdrawal decisions are preserved. When returning an older approved snapshot for search, the application removes only the map-link tracking parameter from a copy; it does not rewrite stored approval history. Unrelated query parameters remain intact.

The starter and expansion regulatory content is unchanged. Earlier reports describing byte-for-byte preservation refer to their releases before distribution cleanup; regulatory content remains preserved.

## Neutral team distribution

Documentation, approval descriptions and fictional test profiles now use neutral team wording. Personal attribution and local account paths were removed. The five existing PNG assets had attribution metadata removed; every image-data chunk, dimension and pixel remains unchanged. No application screen or regulatory rule was redesigned.

The starter and original-data distributions have new pinned checksums because descriptive approval wording changed. Original approval statements, dates and regulatory records remain unchanged. Only exact earlier checksums are also accepted for compatibility. Older stored snapshots and receipts are preserved; expansion installation compares the prior approval against its exact pinned digest and still rejects any changed regulatory content or altered approval. The exact reviewed expansion JSON and expansion release are unchanged. Future regulatory edits still require a new source review.

## Verification

Verification results for the compatible loader and rebuilt ZIP are recorded in [QA_REPORT.md](QA_REPORT.md).
