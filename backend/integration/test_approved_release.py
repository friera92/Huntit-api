from copy import deepcopy
import hashlib
import json
from unittest.mock import Mock, patch

from django.contrib.auth import get_user_model
from django.core.management.base import CommandError
from django.test import TestCase

from regulations.models import DeerManagementUnit, HuntingZone, LandType, Species
from .approved_release import (
    PREVIOUS_RELEASE_SHA256, RELEASE_ID, RELEASE_SHA256, install_approved_release,
    matches_original_snapshot, read_approved_release,
)
from .models import ApprovedReleaseInstallation, RegulationDraft, RegulatoryPublication
from .starter import seed_review_drafts


class ApprovedReleaseTests(TestCase):
    def setUp(self):
        # These local IDs deliberately differ from the original ZIP fixture.
        seed_review_drafts()

    def test_prior_receipt_preserves_withdrawal_and_publication_history(self):
        install_approved_release()
        ApprovedReleaseInstallation.objects.update(sha256=PREVIOUS_RELEASE_SHA256)
        RegulatoryPublication.objects.filter(draft__key="hog-private-2026").update(is_current=False)
        before = list(RegulatoryPublication.objects.values("pk", "snapshot", "is_current"))
        self.assertTrue(install_approved_release()["already_installed"])
        self.assertEqual(list(RegulatoryPublication.objects.values("pk", "snapshot", "is_current")), before)
        self.assertEqual(ApprovedReleaseInstallation.objects.get().sha256, PREVIOUS_RELEASE_SHA256)

    def test_unknown_receipt_digest_is_rejected_without_publication_changes(self):
        install_approved_release()
        ApprovedReleaseInstallation.objects.update(sha256="0" * 64)
        before = list(RegulatoryPublication.objects.values("pk", "snapshot"))
        with self.assertRaisesMessage(CommandError, "different digest"):
            install_approved_release()
        self.assertEqual(list(RegulatoryPublication.objects.values("pk", "snapshot")), before)

    def test_prior_metadata_requires_exact_approval_and_regulatory_content(self):
        install_approved_release()
        expected = RegulatoryPublication.objects.get(draft__key="hog-private-2026").snapshot
        earlier = deepcopy(expected)
        earlier["approved_release"]["sha256"] = PREVIOUS_RELEASE_SHA256
        earlier["approved_release"]["approval"]["provenance"] = "Earlier distribution description"
        digest = hashlib.sha256(json.dumps(earlier["approved_release"]["approval"],
            sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")).hexdigest()
        with patch("integration.approved_release.PREVIOUS_APPROVAL_SHA256", digest):
            self.assertTrue(matches_original_snapshot(earlier, expected))
            for field in ("regulation", "approval", "digest", "extra_metadata"):
                changed = deepcopy(earlier)
                if field == "regulation":
                    changed["rules"][0]["bag"] = "Unreviewed replacement limit"
                elif field == "approval":
                    changed["approved_release"]["approval"]["statement"] = "Different approval"
                elif field == "digest":
                    changed["approved_release"]["sha256"] = "0" * 64
                else:
                    changed["approved_release"]["extra"] = True
                with self.subTest(field=field):
                    self.assertFalse(matches_original_snapshot(changed, expected))

    def test_exact_human_approved_release_installs_without_an_account(self):
        result = install_approved_release()
        self.assertEqual(result, {"added": 18, "preserved": 0, "already_installed": False})
        self.assertEqual(RegulatoryPublication.objects.count(), 18)
        self.assertEqual(get_user_model().objects.count(), 0)
        self.assertFalse(RegulatoryPublication.objects.filter(reviewed_by__isnull=False).exists())
        for publication in RegulatoryPublication.objects.all():
            self.assertEqual(publication.snapshot["approved_release"]["sha256"], RELEASE_SHA256)
            self.assertEqual(publication.reviewed_at.date().isoformat(), "2026-10-12")
            self.assertIn("I checked them", publication.review_notes)
            self.assertTrue(all(source["last_verified_at"] for source in publication.snapshot["sources"]))
        self.assertEqual(ApprovedReleaseInstallation.objects.get().release_id, RELEASE_ID)

    def test_catalog_ids_are_mapped_by_exact_identity_not_original_numeric_id(self):
        install_approved_release()
        public = LandType.objects.get(name="Commission-Managed Land")
        publication = RegulatoryPublication.objects.get(draft__key=f"python-public-{public.pk}-2026")
        self.assertEqual(publication.snapshot["land_type_id"], public.pk)
        self.assertEqual(publication.draft.land_type_id, public.pk)

    def test_mutable_starter_and_draft_edits_cannot_inherit_release_approval(self):
        install_approved_release()
        draft = RegulationDraft.objects.get(key="hog-private-2026")
        before = deepcopy(draft.publications.get().snapshot)
        draft.payload["rules"][0]["bag"] = "Unreviewed new import or mutable starter edit"
        draft.save()
        seed_review_drafts()
        self.assertTrue(install_approved_release()["already_installed"])
        self.assertEqual(draft.publications.get().snapshot, before)
        self.assertEqual(RegulatoryPublication.objects.count(), 18)

    def test_release_rerun_preserves_withdrawal_and_immutable_history(self):
        install_approved_release()
        draft = RegulationDraft.objects.get(key="hog-private-2026")
        draft.publications.update(is_current=False)
        self.assertTrue(install_approved_release()["already_installed"])
        self.assertEqual(RegulatoryPublication.objects.filter(is_current=True).count(), 17)
        self.assertEqual(RegulatoryPublication.objects.count(), 18)

    def test_a_changed_release_file_is_never_approved(self):
        fake_path = Mock()
        fake_path.read_bytes.return_value = b'{"approval": "forged", "drafts": []}'
        with patch("integration.approved_release.RELEASE_PATH", fake_path):
            with self.assertRaisesMessage(CommandError, "SHA-256 mismatch"):
                install_approved_release()
        self.assertFalse(RegulatoryPublication.objects.exists())
        self.assertFalse(ApprovedReleaseInstallation.objects.exists())

    def test_conflicting_unpublished_working_edit_is_preserved_and_install_rolls_back(self):
        draft = RegulationDraft.objects.get(key="hog-private-2026")
        draft.payload["rules"][0]["bag"] = "Team's newer unreviewed working content"
        draft.save()
        with self.assertRaisesMessage(CommandError, "differs from the approved release"):
            install_approved_release()
        self.assertFalse(RegulatoryPublication.objects.exists())
        self.assertFalse(ApprovedReleaseInstallation.objects.exists())
        draft.refresh_from_db()
        self.assertIn("newer unreviewed", draft.payload["rules"][0]["bag"])

    def test_existing_human_reviewed_publication_is_not_replaced(self):
        reviewer = get_user_model().objects.create_superuser("existing-reviewer", "test@example.invalid", "Strong-test-469!")
        draft = RegulationDraft.objects.get(key="hog-private-2026")
        draft.payload["rules"][0]["bag"] = "A separately reviewed team-maintained rule"
        draft.save()
        original = draft.publish(reviewer=reviewer, sources_checked=True, review_notes="Separate test human review")
        result = install_approved_release()
        self.assertEqual(result["preserved"], 1)
        self.assertEqual(result["added"], 17)
        original.refresh_from_db()
        self.assertTrue(original.is_current)
        self.assertEqual(original.reviewed_by, reviewer)
        self.assertEqual(draft.publications.count(), 1)
        self.assertIn("separately reviewed", original.snapshot["rules"][0]["bag"])

    def test_duplicate_species_identity_fails_closed_before_installation(self):
        Species.objects.create(common_name="Wild Hog")
        with self.assertRaisesMessage(CommandError, "exactly one existing record"):
            install_approved_release()
        self.assertFalse(RegulatoryPublication.objects.exists())

    def test_changed_dmu_zone_catalog_association_fails_closed(self):
        dmu = DeerManagementUnit.objects.get(code="A2")
        dmu.zone = HuntingZone.objects.get(code="B")
        dmu.save()
        with self.assertRaisesMessage(CommandError, "different zone"):
            install_approved_release()
        self.assertFalse(RegulatoryPublication.objects.exists())

    def test_frozen_release_contains_only_legitimate_official_fwc_source_urls(self):
        from urllib.parse import urlparse
        release = read_approved_release()
        self.assertEqual(len(release["drafts"]), 18)
        for draft in release["drafts"]:
            for source in draft["payload"]["sources"]:
                parsed = urlparse(source["url"])
                self.assertEqual(parsed.scheme, "https")
                self.assertIn(parsed.hostname, ["myfwc.com", "app.myfwc.com"])
