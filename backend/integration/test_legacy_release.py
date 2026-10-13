from copy import deepcopy
from unittest.mock import Mock, patch

from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied, ValidationError
from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase

from regulations.models import HuntingSeason, RegulationNote, Source, Species
from .approved_release import install_approved_release
from .legacy_release import (
    EXPECTED_COUNTS, LEGACY_RELEASE_ID, LEGACY_RELEASE_SHA256, PREVIOUS_LEGACY_RELEASE_SHA256,
    PREVIOUS_CLEANED_LEGACY_RELEASE_SHA256,
    SELECTOR_FIELDS, SELECTOR_MODELS, _clean_zone_map_url,
    LegacyCatalogMissingError, current_approved_legacy_snapshot, install_approved_legacy_release, mapped_legacy_snapshot,
    read_approved_legacy_release,
)
from .models import ApprovedImportedPublication, ApprovedReleaseInstallation, RegulatoryPublication
from .starter import seed_review_drafts


class ApprovedTeammateInformationTests(TestCase):
    def setUp(self):
        call_command("loaddata", "demo_regulations", verbosity=0)

    def previous_installation(self, *, withdrawn=False, receipt=True):
        """Represent an existing pre-cleanup installation without bundling old links."""
        install_approved_legacy_release()
        publication = ApprovedImportedPublication.objects.get()
        snapshot = deepcopy(publication.snapshot)
        snapshot["sha256"] = PREVIOUS_LEGACY_RELEASE_SHA256
        snapshot.pop("distribution_cleanup")
        for row in snapshot["records"]["huntingzone"]:
            row["map_url"] += "?utm_source=legacy-tracker"
        ApprovedImportedPublication.objects.filter(pk=publication.pk).update(
            sha256=PREVIOUS_LEGACY_RELEASE_SHA256, snapshot=snapshot, is_current=not withdrawn)
        if receipt:
            ApprovedReleaseInstallation.objects.filter(release_id=LEGACY_RELEASE_ID).update(
                sha256=PREVIOUS_LEGACY_RELEASE_SHA256)
        else:
            ApprovedReleaseInstallation.objects.filter(release_id=LEGACY_RELEASE_ID).delete()
        return snapshot

    def test_previous_receipt_and_snapshot_remain_readable_without_rewriting_history(self):
        before = self.previous_installation()
        self.assertEqual(install_approved_legacy_release(), {"added": 0, "already_installed": True})
        actual = current_approved_legacy_snapshot()
        expected = deepcopy(before)
        for row in expected["records"]["huntingzone"]:
            row["map_url"] = "https://myfwc.com/hunting/season-dates/zone-map/"
        self.assertEqual(actual, expected)
        self.assertEqual(ApprovedImportedPublication.objects.get().snapshot, before)
        self.assertEqual(ApprovedImportedPublication.objects.get().sha256, PREVIOUS_LEGACY_RELEASE_SHA256)
        self.assertEqual(ApprovedReleaseInstallation.objects.get().sha256, PREVIOUS_LEGACY_RELEASE_SHA256)

    def test_previous_snapshot_with_missing_receipt_keeps_its_original_digest(self):
        before = self.previous_installation(receipt=False)
        self.assertEqual(install_approved_legacy_release(), {"added": 0, "already_installed": False})
        self.assertEqual(ApprovedImportedPublication.objects.get().snapshot, before)
        self.assertEqual(ApprovedReleaseInstallation.objects.get().sha256, PREVIOUS_LEGACY_RELEASE_SHA256)
        self.assertIsNotNone(current_approved_legacy_snapshot())

    def test_earlier_cleaned_digest_remains_readable_without_replacing_receipt(self):
        install_approved_legacy_release()
        ApprovedImportedPublication.objects.update(sha256=PREVIOUS_CLEANED_LEGACY_RELEASE_SHA256)
        ApprovedReleaseInstallation.objects.update(sha256=PREVIOUS_CLEANED_LEGACY_RELEASE_SHA256)
        before = deepcopy(ApprovedImportedPublication.objects.get().snapshot)
        self.assertTrue(install_approved_legacy_release()["already_installed"])
        self.assertIsNotNone(current_approved_legacy_snapshot())
        self.assertEqual(ApprovedImportedPublication.objects.get().snapshot, before)
        self.assertEqual(ApprovedReleaseInstallation.objects.get().sha256, PREVIOUS_CLEANED_LEGACY_RELEASE_SHA256)

    def test_pre_cleanup_withdrawal_is_preserved_with_or_without_receipt(self):
        before = self.previous_installation(withdrawn=True)
        self.assertEqual(install_approved_legacy_release(), {"added": 0, "already_installed": True})
        self.assertIsNone(current_approved_legacy_snapshot())
        ApprovedReleaseInstallation.objects.filter(release_id=LEGACY_RELEASE_ID).delete()
        self.assertEqual(install_approved_legacy_release(), {"added": 0, "already_installed": False})
        self.assertIsNone(current_approved_legacy_snapshot())
        self.assertEqual(ApprovedImportedPublication.objects.count(), 1)
        self.assertEqual(ApprovedImportedPublication.objects.get().snapshot, before)
        self.assertFalse(ApprovedImportedPublication.objects.get().is_current)

    def test_unknown_receipt_digest_is_still_rejected(self):
        install_approved_legacy_release()
        ApprovedReleaseInstallation.objects.update(sha256="0" * 64)
        with self.assertRaisesMessage(CommandError, "receipt has a different digest"):
            install_approved_legacy_release()

    def test_unknown_snapshot_digest_is_not_read_or_installed(self):
        install_approved_legacy_release()
        ApprovedReleaseInstallation.objects.all().delete()
        ApprovedImportedPublication.objects.update(sha256="0" * 64)
        self.assertIsNone(current_approved_legacy_snapshot())
        with self.assertRaisesMessage(CommandError, "publication has a different digest"):
            install_approved_legacy_release()
        self.assertFalse(ApprovedReleaseInstallation.objects.exists())

    def test_link_cleanup_preserves_other_query_values_fragments_and_other_destinations(self):
        base = "https://myfwc.com/hunting/season-dates/zone-map/"
        original = base + "?area=A%20B&utm_source=legacy-tracker&zoom=5+6&empty=#map"
        self.assertEqual(_clean_zone_map_url(original), base + "?area=A%20B&zoom=5+6&empty=#map")
        self.assertEqual(_clean_zone_map_url(base + "?utm%5Fsource=legacy-tracker#map"), base + "#map")
        for value in (base + "?UTM_SOURCE=legacy-tracker", base + "?ref=legacy-tracker",
                      "https://example.invalid/hunting/season-dates/zone-map/?utm_source=legacy-tracker",
                      "https://myfwc.com/hunting/other-map/?utm_source=legacy-tracker"):
            with self.subTest(value=value):
                self.assertEqual(_clean_zone_map_url(value), value)

    def test_all_292_original_records_are_retained_with_user_confirmation_provenance(self):
        self.assertEqual(install_approved_legacy_release(), {"added": 1, "already_installed": False})
        snapshot = current_approved_legacy_snapshot()
        self.assertEqual({kind: len(rows) for kind, rows in snapshot["records"].items()}, EXPECTED_COUNTS)
        self.assertEqual(snapshot["approval"]["type"], "project_owner_verification_confirmation")
        self.assertFalse(snapshot["approval"]["statement_is_paraphrase"])
        self.assertEqual(snapshot["approval"]["statement"], "include existing information on search result, all existing information has been verified")
        self.assertIn("Project owner confirmed verification", snapshot["approval"]["verification_basis"])
        self.assertEqual(snapshot["sha256"], LEGACY_RELEASE_SHA256)
        self.assertEqual(get_user_model().objects.count(), 0)
        self.assertEqual(ApprovedImportedPublication.objects.get().reviewed_at.isoformat(), "2026-10-12T19:59:07+00:00")

    def test_every_original_field_is_preserved_without_inventing_dates_or_missing_values(self):
        install_approved_legacy_release()
        snapshot = current_approved_legacy_snapshot()
        for original in read_approved_legacy_release()["original_fixture"]:
            kind = original["model"].removeprefix("regulations.")
            actual = next(row for row in snapshot["records"][kind] if row["id"] == original["pk"])
            self.assertEqual(actual, {"id": original["pk"], **original["fields"]})
        self.assertFalse(any(row["last_verified_at"] for row in snapshot["records"]["source"]))
        self.assertFalse(any(row["permits"] for row in snapshot["records"]["huntingseason"]))
        self.assertFalse(any(row["daily_bag_limit"] is not None for row in snapshot["records"]["huntingseason"]))
        period_ids = {row["season"] for row in snapshot["records"]["seasonperiod"]}
        self.assertEqual(sum(row["id"] not in period_ids for row in snapshot["records"]["huntingseason"]), 34)
        self.assertNotIn("coverage", snapshot)

    def test_semantic_catalog_mapping_does_not_depend_on_frozen_numeric_ids(self):
        shifted = deepcopy(read_approved_legacy_release())
        for row in shifted["original_fixture"]:
            kind = row["model"].removeprefix("regulations.")
            if kind in SELECTOR_MODELS:
                row["pk"] += 1000
            for field in SELECTOR_FIELDS:
                if row["fields"].get(field) is not None:
                    row["fields"][field] += 1000
        snapshot = mapped_legacy_snapshot(shifted)
        self.assertEqual({row["id"] for row in snapshot["records"]["species"]}, set(Species.objects.values_list("pk", flat=True)))
        self.assertEqual(snapshot["records"]["huntingseason"][0]["species"], 3)

    def test_future_import_changes_and_species_edits_cannot_change_approved_information(self):
        install_approved_legacy_release()
        before = current_approved_legacy_snapshot()
        HuntingSeason.objects.all().update(notes="New unreviewed import", season_year="2099")
        RegulationNote.objects.all().update(text="Changed after approval")
        Species.objects.all().update(hunting_strategy="New unreviewed tactics")
        Source.objects.all().update(url="https://example.invalid/unreviewed")
        self.assertEqual(install_approved_legacy_release(), {"added": 0, "already_installed": True})
        self.assertEqual(current_approved_legacy_snapshot(), before)

    def test_loader_does_not_change_original_source_verification_or_teammate_records(self):
        before = list(RegulationNote.objects.values("id", "title", "text"))
        sources = list(Source.objects.values("id", "retrieved_at", "last_verified_at", "notes"))
        install_approved_legacy_release()
        self.assertEqual(list(RegulationNote.objects.values("id", "title", "text")), before)
        self.assertEqual(list(Source.objects.values("id", "retrieved_at", "last_verified_at", "notes")), sources)

    def test_the_18_curated_publication_histories_are_preserved(self):
        seed_review_drafts()
        install_approved_release()
        original = list(RegulatoryPublication.objects.values("id", "snapshot", "is_current"))
        install_approved_legacy_release()
        self.assertEqual(list(RegulatoryPublication.objects.values("id", "snapshot", "is_current")), original)
        self.assertEqual(RegulatoryPublication.objects.filter(is_current=True).count(), 18)

    def test_withdrawal_is_not_reversed_by_repeated_setup(self):
        install_approved_legacy_release()
        ApprovedImportedPublication.objects.update(is_current=False)
        self.assertIsNone(current_approved_legacy_snapshot())
        install_approved_legacy_release()
        self.assertIsNone(current_approved_legacy_snapshot())
        self.assertEqual(ApprovedImportedPublication.objects.count(), 1)

    def test_existing_withdrawn_snapshot_without_receipt_is_preserved(self):
        install_approved_legacy_release()
        ApprovedImportedPublication.objects.update(is_current=False)
        ApprovedReleaseInstallation.objects.filter(release_id=LEGACY_RELEASE_ID).delete()
        self.assertEqual(install_approved_legacy_release(), {"added": 0, "already_installed": False})
        self.assertIsNone(current_approved_legacy_snapshot())

    def test_tampered_release_cannot_inherit_human_approval(self):
        fake_path = Mock()
        fake_path.read_bytes.return_value = b'{"original_fixture":[]}'
        with patch("integration.legacy_release.LEGACY_RELEASE_PATH", fake_path):
            with self.assertRaisesMessage(CommandError, "SHA-256 mismatch"):
                install_approved_legacy_release()
        self.assertFalse(ApprovedImportedPublication.objects.exists())

    def test_ambiguous_local_catalog_fails_closed_without_publication(self):
        Species.objects.create(common_name="Wild Hog")
        with self.assertRaisesMessage(CommandError, "exactly one local record"):
            install_approved_legacy_release()
        self.assertFalse(ApprovedImportedPublication.objects.exists())
        self.assertFalse(ApprovedReleaseInstallation.objects.exists())

    def test_explicit_loader_fails_closed_for_a_missing_catalog_identity(self):
        Species.objects.get(common_name="Wild Turkey").delete()
        with self.assertRaises(LegacyCatalogMissingError):
            call_command("load_approved_legacy_release", verbosity=0)
        self.assertFalse(ApprovedImportedPublication.objects.exists())

    def test_setup_does_not_suppress_a_tampered_release_error(self):
        fake_path = Mock()
        fake_path.read_bytes.return_value = b'{"original_fixture":[]}'
        with patch("integration.legacy_release.LEGACY_RELEASE_PATH", fake_path):
            with self.assertRaisesMessage(CommandError, "SHA-256 mismatch"):
                call_command("seed_local_data", verbosity=0)
        self.assertFalse(ApprovedImportedPublication.objects.exists())

    def test_setup_does_not_suppress_an_ambiguous_catalog_error(self):
        Species.objects.create(common_name="Wild Turkey")
        with self.assertRaisesMessage(CommandError, "exactly one local record"):
            call_command("seed_local_data", verbosity=0)
        self.assertFalse(ApprovedImportedPublication.objects.exists())

    def test_direct_snapshot_creation_and_edits_are_rejected(self):
        with self.assertRaises(PermissionDenied):
            ApprovedImportedPublication.objects.create(release_id="unreviewed", snapshot={},
                sha256="0" * 64, reviewed_at="2026-10-12T00:00:00Z", review_notes="Bypass")
        install_approved_legacy_release()
        publication = ApprovedImportedPublication.objects.get()
        publication.snapshot["records"]["species"][0]["hunting_strategy"] = "Changed"
        with self.assertRaises(ValidationError):
            publication.save()

    def test_authorized_reviewer_can_withdraw_snapshot_through_readonly_admin(self):
        install_approved_legacy_release()
        reviewer = get_user_model().objects.create_superuser("reviewer", "review@example.invalid", "Test-password-345!")
        self.client.force_login(reviewer)
        response = self.client.post("/admin/integration/approvedimportedpublication/", {
            "action": "withdraw_approved_import", "_selected_action": str(ApprovedImportedPublication.objects.get().pk),
            "index": "0"})
        self.assertEqual(response.status_code, 302)
        self.assertIsNone(current_approved_legacy_snapshot())
        self.assertEqual(ApprovedImportedPublication.objects.count(), 1)
