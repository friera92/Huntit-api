"""Prevent Fisheating's narrow east/west rules becoming blanket permission."""
from copy import deepcopy

from django.contrib.auth import get_user_model
from django.test import TestCase

from regulations.models import LandType, ManagedArea, RegulatoryArea, Species
from .models import RegulationDraft, RegulatoryPublication
from .python_area_data import AREA_NAME, ORDER, seed_fisheating_python_drafts


class FisheatingPythonTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.created = seed_fisheating_python_drafts()
        cls.area = ManagedArea.objects.get(name=AREA_NAME)
        cls.python = Species.objects.get(common_name="Burmese Python")
        cls.wma = LandType.objects.get(name="Wildlife Management Area (WMA)")
        cls.public = LandType.objects.get(name="Commission-Managed Land")
        cls.regions = {side: RegulatoryArea.objects.get(code=f"FISHEATING_{side.upper()}_US27") for side in ["west", "east"]}
        cls.reviewer = get_user_model().objects.create_superuser(
            username="fish-test-reviewer", email="fish@example.invalid", password="Fish-test-only-4812!")

    def draft(self, side, land=None):
        return RegulationDraft.objects.get(key=f"python-fisheating-{side}-{(land or self.wma).pk}-2026-2027")

    def publish(self, side, land=None):
        return self.draft(side, land).publish(reviewer=self.reviewer, sources_checked=True,
                                            review_notes="Test-only review of Fisheating east/west EO and exact special-opportunity dates.")

    def search(self, side, when, land=None, **overrides):
        params = {"species": self.python.pk, "land_type": (land or self.wma).pk,
                  "managed_area": self.area.pk, "date": when}
        if side:
            params["regulatory_area"] = self.regions[side].pk
        params.update(overrides)
        return self.client.get("/api/regulations/search/", params)

    def test_four_valid_exact_scope_drafts_without_automatic_publication(self):
        self.assertEqual(self.created, 4)
        self.assertFalse(RegulatoryPublication.objects.exists())
        for draft in RegulationDraft.objects.all():
            draft.full_clean()
            self.assertEqual(set(draft.payload["required_inputs"]), {"managed_area", "regulatory_area"})
            self.assertIn(ORDER, [entry["url"] for entry in draft.payload["sources"]])
        result = self.search("east", "2027-03-06").json()
        self.assertEqual(result["status"], "needs_review")
        self.assertFalse(result["verified"])
        self.assertEqual(result["matched_seasons"], [])

    def test_reseeding_preserves_local_draft_edits_and_publication_bytes(self):
        draft = self.draft("west")
        draft.title = "Local working title"
        draft.save()
        publication = self.publish("west")
        snapshot = deepcopy(publication.snapshot)
        self.assertEqual(seed_fisheating_python_drafts(), 0)
        draft.refresh_from_db()
        publication.refresh_from_db()
        self.assertEqual(draft.title, "Local working title")
        self.assertEqual(publication.snapshot, snapshot)

    def test_missing_side_prompts_instead_of_combining_incompatible_rules(self):
        self.publish("west")
        self.publish("east")
        result = self.search(None, "2027-03-06")
        self.assertEqual(result.status_code, 400)
        self.assertIn("regulatory_area", result.json())

    def test_east_only_exact_special_opportunity_periods_are_open(self):
        self.publish("east")
        for when in ["2027-03-06", "2027-03-12", "2027-03-20", "2027-03-26"]:
            with self.subTest(date=when):
                result = self.search("east", when).json()
                self.assertTrue(result["verified"])
                self.assertEqual(result["status"], "reviewed")
                self.assertEqual(len(result["matched_seasons"]), 1)
                self.assertIn("Special-Opportunity Spring Turkey Permit", result["licenses"])
                self.assertIn("including removal without a firearm", result["licenses"])
        for when in ["2026-10-12", "2027-03-05", "2027-03-13", "2027-03-19", "2027-03-27", "2027-04-02"]:
            with self.subTest(date=when):
                result = self.search("east", when).json()
                self.assertEqual(result["status"], "closed")
                self.assertEqual(result["eligibility"], "no_open_season")
                self.assertEqual(result["matched_seasons"], [])

    def test_west_year_round_does_not_authorize_year_round_bows_or_airguns(self):
        self.publish("west")
        result = self.search("west", "2026-10-12").json()
        self.assertEqual(result["status"], "reviewed")
        self.assertIn("other than firearms, airguns, bows or crossbows", result["methods"])
        self.assertIn("only during open brochure hunting seasons", result["methods"])
        self.assertIn("management area permit is required when using a gun", result["licenses"])
        self.assertNotIn("Special-Opportunity Spring Turkey Permit", result["licenses"])

    def test_east_season_equipment_and_reptile_hours_do_not_expand_turkey_hours(self):
        self.publish("east")
        result = self.search("east", "2027-03-06").json()
        self.assertIn("No. 2 or smaller", result["methods"])
        self.assertIn("PCP bullets are not authorized", result["methods"])
        self.assertIn("1 p.m. cutoff", " ".join(result["alerts"]))
        self.assertIn("Reptile shooting hours", " ".join(result["alerts"]))

    def test_order_trap_captive_bolt_and_live_removal_restrictions_apply_to_both_sides(self):
        for side in ["west", "east"]:
            self.publish(side)
            result = self.search(side, "2027-03-06").json()
            alerts = " ".join(result["alerts"])
            self.assertIn("prohibits traps", alerts)
            self.assertIn("free-bolt", alerts)
            self.assertIn("No live python", alerts)
            self.assertIn("Dogs may not", alerts)

    def test_public_selector_aliases_retain_identical_east_and_west_facts(self):
        for side in ["west", "east"]:
            one = deepcopy(self.draft(side, self.wma).payload)
            two = deepcopy(self.draft(side, self.public).payload)
            one.pop("land_type_id")
            two.pop("land_type_id")
            self.assertEqual(one, two)
            self.publish(side, self.public)
            self.assertEqual(self.search(side, "2027-03-06", self.public).json()["status"], "reviewed")

    def test_side_scope_does_not_leak_to_another_area_or_another_region(self):
        self.publish("east")
        self.assertFalse(self.search("west", "2027-03-06").json()["verified"])
        other = ManagedArea.objects.create(name="Other WMA", area_type="WMA")
        self.assertFalse(self.search("east", "2027-03-06", managed_area=other.pk).json()["verified"])
        self.assertEqual(self.search("east", "2027-07-01").json()["status"], "no_data")
