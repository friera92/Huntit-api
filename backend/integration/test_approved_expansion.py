"""Regressions for the owner's exact source-reviewed local data expansion."""
from copy import deepcopy
from io import StringIO
from unittest.mock import Mock, patch

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase

from regulations.models import (
    DeerManagementUnit, HuntingZone, LandType, ManagedArea, RegulatoryArea, Source, Species,
)
from .approved_expansion import (
    RELEASE_ID, RELEASE_SHA256, REVIEW_SHA256, install_approved_expansion, read_approved_expansion,
)
from .approved_release import install_approved_release
from .data_expansion import seed_data_expansion
from .legacy_release import install_approved_legacy_release
from .models import (
    ApprovedImportedPublication, ApprovedReleaseInstallation, RegulationDraft,
    RegulatoryPublication, SCOPE_MODELS,
)
from .starter import seed_review_drafts


class ApprovedExpansionTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("loaddata", "demo_regulations", verbosity=0)
        seed_review_drafts()
        install_approved_release()
        install_approved_legacy_release()
        seed_data_expansion()

    def test_exact_owner_approved_expansion_installs_without_account_and_preserves_history(self):
        originals = list(RegulatoryPublication.objects.values("pk", "snapshot", "revision"))
        result = install_approved_expansion()
        self.assertEqual(result["added"], 58)
        self.assertFalse(result["already_installed"])
        self.assertEqual(RegulationDraft.objects.count(), 58)
        self.assertEqual(RegulatoryPublication.objects.count(), 76)
        self.assertEqual(RegulatoryPublication.objects.filter(is_current=True).count(), 58)
        self.assertEqual(ApprovedImportedPublication.objects.count(), 1)
        self.assertEqual(ApprovedReleaseInstallation.objects.count(), 3)
        self.assertEqual(get_user_model().objects.count(), 0)
        self.assertFalse(RegulatoryPublication.objects.filter(reviewed_by__isnull=False).exists())
        self.assertFalse(Source.objects.filter(last_verified_at__isnull=False).exists())
        for old in originals:
            stored = RegulatoryPublication.objects.get(pk=old["pk"])
            self.assertEqual(stored.snapshot, old["snapshot"])
            self.assertEqual(stored.revision, old["revision"])
            self.assertFalse(stored.is_current)
            self.assertTrue(stored.draft.publications.filter(revision=2, is_current=True).exists())
        for publication in RegulatoryPublication.objects.filter(is_current=True):
            self.assertIn("Sources checked — approve local publication", publication.review_notes)
            self.assertEqual(publication.snapshot["approved_expansion"]["sha256"], RELEASE_SHA256)
            self.assertEqual(publication.snapshot["approved_expansion"]["release_id"], RELEASE_ID)
            self.assertEqual(publication.snapshot["approved_expansion"]["approved_review_sha256"], REVIEW_SHA256)
            self.assertEqual(publication.snapshot["approved_expansion"]["approval"]["statement"],
                             "Sources checked — approve local publication")
            self.assertTrue(all(source["last_verified_at"] == publication.reviewed_at.isoformat()
                                for source in publication.snapshot["sources"]))
        self.assertEqual(ApprovedReleaseInstallation.objects.get(release_id=RELEASE_ID).publications_added, 58)

    def test_changed_release_bytes_cannot_inherit_human_approval(self):
        fake_path = Mock()
        fake_path.read_bytes.return_value = b'{"approval":"forged","review":{"drafts":[]}}'
        before = list(RegulatoryPublication.objects.values("pk", "snapshot", "is_current"))
        with patch("integration.approved_expansion.RELEASE_PATH", fake_path):
            with self.assertRaisesMessage(CommandError, "SHA-256 mismatch"):
                install_approved_expansion()
        self.assertEqual(list(RegulatoryPublication.objects.values("pk", "snapshot", "is_current")), before)
        self.assertFalse(ApprovedReleaseInstallation.objects.filter(release_id=RELEASE_ID).exists())

    def test_conflicting_working_edit_rolls_back_entire_installation(self):
        # Pick a late expansion record so an installer that commits incrementally
        # would have already changed the earlier drafts/publications.
        draft = RegulationDraft.objects.get(key="turkey-private-spring-south_sr70-2026-2027")
        draft.payload["rules"][0]["bag"] = "A later unreviewed team edit"
        draft.save()
        before = list(RegulatoryPublication.objects.values("pk", "snapshot", "is_current"))
        with self.assertRaises(CommandError):
            install_approved_expansion()
        self.assertEqual(list(RegulatoryPublication.objects.values("pk", "snapshot", "is_current")), before)
        self.assertFalse(ApprovedReleaseInstallation.objects.filter(release_id=RELEASE_ID).exists())
        draft.refresh_from_db()
        self.assertEqual(draft.payload["rules"][0]["bag"], "A later unreviewed team edit")

    def test_repeated_setup_preserves_unpublished_work_and_withdrawal(self):
        install_approved_expansion()
        draft = RegulationDraft.objects.get(key="turkey-private-spring-south_sr70-2026-2027")
        before = deepcopy(draft.publications.get(is_current=True).snapshot)
        draft.payload["alerts"].append("Future draft edit without another approval")
        draft.save()
        RegulatoryPublication.objects.filter(draft__key="hog-private-2026", is_current=True).update(is_current=False)
        call_command("seed_local_data", stdout=StringIO())
        draft.refresh_from_db()
        self.assertIn("Future draft edit without another approval", draft.payload["alerts"])
        self.assertEqual(draft.publications.get(is_current=True).snapshot, before)
        self.assertFalse(RegulatoryPublication.objects.filter(draft__key="hog-private-2026", is_current=True).exists())
        self.assertEqual(RegulatoryPublication.objects.count(), 76)
        self.assertEqual(RegulatoryPublication.objects.filter(is_current=True).count(), 57)

    def test_repeated_setup_preserves_a_later_manual_review(self):
        install_approved_expansion()
        draft = RegulationDraft.objects.get(key="turkey-private-spring-south_sr70-2026-2027")
        reviewer = get_user_model().objects.create_superuser("later-reviewer", password="Disposable-QA-8524!")
        draft.payload["alerts"].append("Subsequent team review")
        draft.save()
        newer = draft.publish(reviewer=reviewer, sources_checked=True, review_notes="Later explicit QA review")
        call_command("seed_local_data", stdout=StringIO())
        newer.refresh_from_db()
        self.assertTrue(newer.is_current)
        self.assertEqual(draft.publications.get(is_current=True).pk, newer.pk)
        self.assertEqual(RegulatoryPublication.objects.count(), 77)
        self.assertEqual(RegulatoryPublication.objects.filter(is_current=True).count(), 58)

    def test_missing_receipt_does_not_republish_withdrawn_or_superseded_information(self):
        install_approved_expansion()
        draft = RegulationDraft.objects.get(key="hog-private-2026")
        draft.publications.filter(is_current=True).update(is_current=False)
        ApprovedReleaseInstallation.objects.filter(release_id=RELEASE_ID).delete()
        result = install_approved_expansion()
        self.assertEqual(result["added"], 0)
        self.assertFalse(draft.publications.filter(is_current=True).exists())
        self.assertEqual(RegulatoryPublication.objects.count(), 76)

    def test_ambiguous_catalog_fails_before_any_partial_publication(self):
        Species.objects.create(common_name="Wild Turkey")
        before = list(RegulatoryPublication.objects.values("pk", "snapshot", "is_current"))
        with self.assertRaisesMessage(CommandError, "exactly one"):
            install_approved_expansion()
        self.assertEqual(list(RegulatoryPublication.objects.values("pk", "snapshot", "is_current")), before)
        self.assertFalse(ApprovedReleaseInstallation.objects.filter(release_id=RELEASE_ID).exists())

    def test_ambiguous_regulatory_area_name_is_not_guessed_from_numeric_id(self):
        region = RegulatoryArea.objects.get(code="FISHEATING_EAST_US27")
        RegulatoryArea.objects.create(code="DIFFERENT_CODE", name=region.name)
        before = list(RegulatoryPublication.objects.values("pk", "snapshot", "is_current"))
        with self.assertRaisesMessage(CommandError, "exactly one"):
            install_approved_expansion()
        self.assertEqual(list(RegulatoryPublication.objects.values("pk", "snapshot", "is_current")), before)
        self.assertFalse(ApprovedReleaseInstallation.objects.filter(release_id=RELEASE_ID).exists())

    def test_changed_original_snapshot_is_not_silently_superseded(self):
        original = RegulatoryPublication.objects.get(draft__key="hog-private-2026")
        changed = deepcopy(original.snapshot)
        changed["rules"][0]["bag"] = "Unexpected historical database change"
        RegulatoryPublication.objects.filter(pk=original.pk).update(snapshot=changed)
        before = list(RegulatoryPublication.objects.values("pk", "snapshot", "is_current"))
        with self.assertRaisesMessage(CommandError, "differs from its frozen release"):
            install_approved_expansion()
        self.assertEqual(list(RegulatoryPublication.objects.values("pk", "snapshot", "is_current")), before)
        self.assertFalse(ApprovedReleaseInstallation.objects.filter(release_id=RELEASE_ID).exists())

    def test_separate_fisheating_review_preserves_whole_interdependent_python_group(self):
        public = LandType.objects.get(name="Commission-Managed Land")
        draft = RegulationDraft.objects.get(key=f"python-fisheating-east-{public.pk}-2026-2027")
        reviewer = get_user_model().objects.create_superuser("fish-reviewer", password="Disposable-QA-9357!")
        draft.payload["alerts"].append("Separately reviewed Fisheating update")
        draft.save()
        manual = draft.publish(reviewer=reviewer, sources_checked=True, review_notes="Separate QA review")
        originals = list(RegulatoryPublication.objects.filter(draft__key__startswith="python-public-")
                         .values("pk", "snapshot"))
        result = install_approved_expansion()
        self.assertEqual(result["added"], 52)
        self.assertEqual(result["preserved"], 6)
        manual.refresh_from_db()
        self.assertTrue(manual.is_current)
        self.assertEqual(RegulatoryPublication.objects.filter(draft__key__startswith="python-fisheating-").count(), 1)
        for original in originals:
            stored = RegulatoryPublication.objects.get(pk=original["pk"])
            self.assertTrue(stored.is_current)
            self.assertEqual(stored.snapshot, original["snapshot"])

    def test_withdrawn_broad_python_scope_preserves_all_six_fisheating_group_members(self):
        public = LandType.objects.get(name="Commission-Managed Land")
        withdrawn = RegulatoryPublication.objects.get(draft__key=f"python-public-{public.pk}-2026")
        RegulatoryPublication.objects.filter(pk=withdrawn.pk).update(is_current=False)
        originals = list(RegulatoryPublication.objects.filter(draft__key__startswith="python-public-")
                         .values("pk", "snapshot", "revision", "is_current"))
        result = install_approved_expansion()
        self.assertEqual(result["added"], 52)
        self.assertEqual(result["preserved"], 6)
        self.assertFalse(RegulatoryPublication.objects.filter(draft__key__startswith="python-fisheating-").exists())
        self.assertEqual(RegulatoryPublication.objects.filter(draft__key__startswith="python-public-").count(), 2)
        for original in originals:
            stored = RegulatoryPublication.objects.get(pk=original["pk"])
            self.assertEqual(stored.snapshot, original["snapshot"])
            self.assertEqual(stored.revision, original["revision"])
            self.assertEqual(stored.is_current, original["is_current"])

    def test_published_turkey_fills_primary_fields_and_profile(self):
        install_approved_expansion()
        turkey = Species.objects.get(common_name="Wild Turkey")
        private = LandType.objects.get(name="Private Land")
        south = RegulatoryArea.objects.get(code="SOUTH_SR70")
        response = self.client.get("/api/regulations/search/", {
            "species": turkey.pk, "land_type": private.pk, "regulatory_area": south.pk,
            "date": "2027-03-06", "landowner_permission": "true"})
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertEqual(result["status"], "reviewed")
        self.assertIn("Turkey Permit", result["licenses"])
        for key in ["licenses", "methods", "bag", "about", "habitat", "behavior", "tactics"]:
            self.assertTrue(result[key], key)
            self.assertNotIn("not recorded", result[key].casefold())
        self.assertTrue(result["species_information_reviewed"])
        self.assertTrue(result["species_information_verified_at"])

    def test_fisheating_precise_east_and_west_publications_replace_broad_exception(self):
        install_approved_expansion()
        python = Species.objects.get(common_name="Burmese Python")
        fish = ManagedArea.objects.get(name="Fisheating Creek WMA")
        east = RegulatoryArea.objects.get(code="FISHEATING_EAST_US27")
        west = RegulatoryArea.objects.get(code="FISHEATING_WEST_US27")
        for name in ["Commission-Managed Land", "Wildlife Management Area (WMA)"]:
            land = LandType.objects.get(name=name)
            query = {"species": python.pk, "land_type": land.pk, "managed_area": fish.pk,
                     "regulatory_area": east.pk, "date": "2027-03-06"}
            opened = self.client.get("/api/regulations/search/", query).json()
            self.assertEqual(opened["status"], "reviewed")
            self.assertIn("Special-Opportunity Spring Turkey Permit", opened["licenses"])
            self.assertNotIn("No hunting license or removal permit", opened["licenses"])
            query["date"] = "2026-10-12"
            closed = self.client.get("/api/regulations/search/", query).json()
            self.assertEqual(closed["status"], "closed")
            self.assertEqual(closed["matched_seasons"], [])
            query["regulatory_area"] = west.pk
            west_answer = self.client.get("/api/regulations/search/", query).json()
            self.assertEqual(west_answer["status"], "reviewed")
            self.assertIn("management area permit is required when using a gun", west_answer["licenses"])


class ApprovedExpansionPortableCatalogTests(TestCase):
    def test_shifted_local_ids_map_location_scopes_and_dynamic_keys_by_identity(self):
        # Force each selector family away from the original fixture's IDs.
        Species.objects.create(pk=1000, common_name="Other species")
        LandType.objects.create(pk=1000, name="Other land")
        zone = HuntingZone.objects.create(pk=1000, code="X", name="Other zone")
        DeerManagementUnit.objects.create(pk=1000, code="X1", zone=zone)
        ManagedArea.objects.create(pk=1000, name="Other area")
        RegulatoryArea.objects.create(pk=1000, code="OTHER", name="Other region")
        seed_review_drafts()
        install_approved_release()
        seed_data_expansion()
        result = install_approved_expansion()
        self.assertEqual(result["added"], 58)
        self.assertEqual(RegulatoryPublication.objects.filter(is_current=True).count(), 58)
        release = read_approved_expansion()
        self.assertTrue(release)
        for publication in RegulatoryPublication.objects.filter(is_current=True):
            content = publication.snapshot
            self.assertGreater(content["species_id"], 1000)
            self.assertGreater(content["land_type_id"], 1000)
            self.assertEqual(content["species_id"], publication.draft.species_id)
            self.assertEqual(content["land_type_id"], publication.draft.land_type_id)
            for scopes in [content.get("scopes", {}), *(item.get("scopes", {}) for item in content["rules"])]:
                for field, value in scopes.items():
                    identifiers = value if isinstance(value, list) else [value]
                    self.assertTrue(all(identifier > 1000 for identifier in identifiers))
                    self.assertEqual(SCOPE_MODELS[field].objects.filter(pk__in=identifiers).count(), len(set(identifiers)))
        for land_name in ["Commission-Managed Land", "Wildlife Management Area (WMA)"]:
            land = LandType.objects.get(name=land_name)
            for side in ["east", "west"]:
                publication = RegulatoryPublication.objects.get(
                    draft__key=f"python-fisheating-{side}-{land.pk}-2026-2027", is_current=True)
                self.assertEqual(publication.snapshot["scopes"]["regulatory_area"],
                                 RegulatoryArea.objects.get(code=f"FISHEATING_{side.upper()}_US27").pk)
            self.assertTrue(RegulatoryPublication.objects.filter(
                draft__key=f"deer-dinner-island-{land.pk}-2026-2027", is_current=True).exists())
