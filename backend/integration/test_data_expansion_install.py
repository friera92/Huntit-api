"""Regression checks for preserving original data and the review boundary."""
from copy import deepcopy
from django.core.management import call_command
from django.test import TestCase

from regulations.models import LandType, LicensePermit, ManagedArea, RegulatoryArea, Source, Species
from .catalog_data import seed_catalog_details
from .approved_release import install_approved_release
from .data_expansion import EDITION, seed_data_expansion
from .legacy_release import install_approved_legacy_release
from .models import RegulationDraft, RegulatoryPublication
from .starter import seed_review_drafts


class ExpansionInstallationTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Exercise staging in isolation. Normal setup now installs the exact
        # expansion that the project owner approved after checking its sources.
        call_command("loaddata", "demo_regulations", verbosity=0)
        seed_review_drafts()
        install_approved_release()
        install_approved_legacy_release()
        seed_data_expansion()

    def test_existing_publications_are_unchanged_and_new_content_remains_draft(self):
        self.assertEqual(RegulationDraft.objects.count(), 58)
        self.assertEqual(RegulatoryPublication.objects.count(), 18)
        changed = RegulationDraft.objects.filter(payload__data_expansion_edition=EDITION, publications__isnull=False)
        self.assertEqual(changed.count(), 18)
        for draft in changed:
            self.assertNotIn("data_expansion_edition", draft.publications.get().snapshot)
            self.assertNotEqual(draft.payload, draft.publications.get().snapshot)
        self.assertFalse(RegulatoryPublication.objects.filter(snapshot__species_information__isnull=False).exists())

    def test_repeat_setup_preserves_edits_withdrawals_and_blank_catalog_policy(self):
        draft = RegulationDraft.objects.filter(key__startswith="turkey-private").first()
        draft.payload["alerts"].append("New team review note")
        draft.save()
        original = deepcopy(draft.payload)
        area = ManagedArea.objects.get(name="Holey Land WMA")
        area.brochure_url = "https://myfwc.com/team-maintained-reference/"
        area.save()
        permit = LicensePermit.objects.get(name="Turkey Permit")
        permit.requirements = "Team-maintained new working requirement"
        permit.save()
        RegulatoryPublication.objects.filter(draft__key="hog-private-2026").update(is_current=False)
        result = seed_data_expansion()
        draft.refresh_from_db()
        area.refresh_from_db()
        permit.refresh_from_db()
        self.assertEqual(draft.payload, original)
        self.assertEqual(area.brochure_url, "https://myfwc.com/team-maintained-reference/")
        self.assertEqual(permit.requirements, "Team-maintained new working requirement")
        self.assertEqual(RegulatoryPublication.objects.filter(is_current=True).count(), 17)
        self.assertEqual(result["turkey_drafts_added"], 0)
        self.assertEqual(result["wma_drafts_added"], 0)
        self.assertEqual(result["extra_wma_drafts_added"], 0)
        self.assertEqual(result["python_exception_drafts_added"], 0)

    def test_original_source_verification_is_not_rewritten(self):
        self.assertEqual(Source.objects.count(), 4)
        self.assertFalse(Source.objects.filter(last_verified_at__isnull=False).exists())
        self.assertEqual(seed_catalog_details()["permits_added"], 0)

    def test_all_area_reference_links_available_without_approving_seasons(self):
        catalog = self.client.get("/api/catalog/").json()
        self.assertEqual(len(catalog["managed_areas"]), 32)
        self.assertTrue(all(row["brochure_url"].startswith("https://") for row in catalog["managed_areas"]))
        self.assertTrue(all(row["map_url"].startswith("https://myfwc.com/") for row in catalog["managed_areas"]))
        self.assertTrue(any(row["name"] == "Turkey Permit" for row in catalog["license_permits"]))
        self.assertEqual(sum(not row["reviewed"] for row in catalog["supported_scopes"]), 40)

    def test_historical_broad_python_answer_is_withheld_for_fisheating_pending_precise_review(self):
        python = Species.objects.get(common_name="Burmese Python")
        fish = ManagedArea.objects.get(name="Fisheating Creek WMA")
        east = RegulatoryArea.objects.get(code="FISHEATING_EAST_US27")
        for name in ["Commission-Managed Land", "Wildlife Management Area (WMA)"]:
            land = LandType.objects.get(name=name)
            response = self.client.get("/api/regulations/search/", {
                "species": python.pk, "land_type": land.pk, "managed_area": fish.pk,
                "regulatory_area": east.pk, "date": "2026-10-12"})
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertEqual(data["status"], "needs_review")
            self.assertFalse(data["verified"])
            self.assertFalse(data["matched_seasons"])
            self.assertNotIn("No hunting license or removal permit", data["licenses"])
        self.assertEqual(RegulatoryPublication.objects.count(), 18)
        scopes = self.client.get("/api/catalog/").json()["supported_scopes"]
        for scope in scopes:
            if scope["reviewed"] and scope["species"] == python.pk:
                areas = scope["scopes"].get("managed_area", [])
                areas = areas if isinstance(areas, list) else [areas]
                self.assertNotIn(fish.pk, areas)
