"""Area boundaries and exceptions that broad statewide data cannot represent."""
from copy import deepcopy

from django.contrib.auth import get_user_model
from django.test import TestCase

from regulations.models import LandType, ManagedArea, Species
from .models import RegulationDraft, RegulatoryPublication
from .starter import seed_review_drafts
from .wma_data import AREA_NAMES, BROCHURES, TAKING_GAME, seed_wma_review_drafts


class WmaExpansionTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        seed_review_drafts()
        cls.created = seed_wma_review_drafts()
        cls.wma = LandType.objects.get(name="Wildlife Management Area (WMA)")
        cls.public = LandType.objects.get(name="Commission-Managed Land")
        cls.species = {kind: Species.objects.get(common_name=name) for kind, name in
                       {"hog": "Wild Hog", "deer": "White Tailed Deer", "turkey": "Wild Turkey", "python": "Burmese Python"}.items()}
        cls.areas = {key: ManagedArea.objects.get(name=name) for key, name in AREA_NAMES.items()}
        cls.reviewer = get_user_model().objects.create_superuser(
            username="wma-test-reviewer", email="wma@example.invalid", password="Wma-test-only-8234!")

    def draft(self, kind, area, land=None):
        return RegulationDraft.objects.get(key=f"{kind}-{area}-{(land or self.wma).pk}-2026-2027-expanded")

    def publish(self, kind, area, land=None):
        return self.draft(kind, area, land).publish(
            reviewer=self.reviewer, sources_checked=True,
            review_notes="Test-only source acknowledgement for exact area dates, restrictions and permit conditions.")

    def search(self, kind, area, when, land=None):
        response = self.client.get("/api/regulations/search/", {
            "species": self.species[kind].pk, "land_type": (land or self.wma).pk,
            "managed_area": self.areas[area].pk, "date": when,
        })
        self.assertEqual(response.status_code, 200, response.content)
        return response.json()

    def test_seed_adds_22_valid_drafts_but_publishes_nothing(self):
        self.assertEqual(self.created, 22)
        self.assertFalse(RegulatoryPublication.objects.exists())
        for draft in RegulationDraft.objects.filter(key__endswith="expanded"):
            draft.full_clean()
            self.assertIn("managed_area", draft.payload["required_inputs"])
        result = self.search("hog", "holey-land", "2026-08-08")
        self.assertEqual(result["status"], "needs_review")
        self.assertFalse(result["verified"])
        self.assertEqual(result["matched_seasons"], [])
        self.assertNotIn("No hunting license", result["licenses"])

    def test_reseeding_preserves_custom_work_and_reviewed_snapshots(self):
        draft = self.draft("hog", "corbett")
        draft.title = "Local editor's working copy"
        draft.save()
        publication = self.publish("hog", "corbett")
        snapshot = deepcopy(publication.snapshot)
        self.assertEqual(seed_wma_review_drafts(), 0)
        draft.refresh_from_db()
        publication.refresh_from_db()
        self.assertEqual(draft.title, "Local editor's working copy")
        self.assertEqual(publication.snapshot, snapshot)
        self.assertTrue(publication.is_current)

    def test_corbett_deer_existing_drafts_are_not_duplicated(self):
        self.assertFalse(RegulationDraft.objects.filter(key__startswith="deer-corbett", key__endswith="expanded").exists())
        self.assertEqual(RegulationDraft.objects.filter(key__startswith="deer-corbett").count(), 2)

    def test_public_selector_aliases_have_identical_area_facts(self):
        for area in AREA_NAMES:
            for kind in ("hog", "turkey", "python"):
                with self.subTest(area=area, species=kind):
                    left = deepcopy(self.draft(kind, area, self.wma).payload)
                    right = deepcopy(self.draft(kind, area, self.public).payload)
                    left.pop("land_type_id")
                    right.pop("land_type_id")
                    self.assertEqual(left, right)

    def test_corbett_hog_boundaries_and_small_game_are_area_specific(self):
        self.publish("hog", "corbett")
        for when, code in [("2026-08-29", "ARCHERY"), ("2026-09-20", "ARCHERY"),
                           ("2026-10-03", "MUZZLELOADER"), ("2026-10-18", "MUZZLELOADER"),
                           ("2026-11-07", "GENERAL_GUN"), ("2027-01-03", "GENERAL_GUN"),
                           ("2027-01-04", "SMALL_GAME"), ("2027-02-21", "SMALL_GAME")]:
            with self.subTest(date=when):
                result = self.search("hog", "corbett", when)
                self.assertEqual(result["status"], "reviewed")
                self.assertEqual([row["season_type_code"] for row in result["matched_seasons"]], [code])
                self.assertIn("No hunting license", result["licenses"])
        for when in ["2026-08-28", "2026-09-21", "2026-10-19", "2027-02-22"]:
            self.assertEqual(self.search("hog", "corbett", when)["status"], "closed")

    def test_rotenberger_hog_does_not_gain_small_game_or_vehicle_hunt(self):
        self.publish("hog", "rotenberger")
        for when in ["2026-11-21", "2026-12-07", "2027-03-07"]:
            result = self.search("hog", "rotenberger", when)
            self.assertEqual(result["status"], "closed")
            self.assertEqual(result["matched_seasons"], [])

    def test_holey_vehicle_hunt_retains_quota_and_access_conditions(self):
        self.publish("deer", "holey-land")
        result = self.search("deer", "holey-land", "2026-11-21")
        self.assertEqual(result["status"], "reviewed")
        self.assertIn("no quota exemptions", result["licenses"])
        self.assertIn("per FWC antlered deer tag", result["bag"])
        self.assertIn("walk-hunting is closed", " ".join(result["alerts"]))
        self.assertEqual(self.search("deer", "holey-land", "2026-12-07")["status"], "closed")

    def test_hog_vehicle_hunt_still_does_not_require_hunting_license(self):
        self.publish("hog", "holey-land")
        result = self.search("hog", "holey-land", "2026-11-21")
        self.assertIn("No hunting license is required", result["licenses"])
        self.assertIn("quota/track permit", result["licenses"])
        self.assertIn("Management area permit", result["licenses"])

    def test_turkey_prohibition_is_reviewed_closed_without_a_fake_open_season(self):
        for area in ["holey-land", "rotenberger"]:
            self.publish("turkey", area)
            for when in ["2026-07-01", "2027-03-06", "2027-06-30"]:
                with self.subTest(area=area, date=when):
                    result = self.search("turkey", area, when)
                    self.assertTrue(result["verified"])
                    self.assertEqual(result["status"], "closed")
                    self.assertEqual(result["eligibility"], "no_open_season")
                    self.assertEqual(result["matched_seasons"], [])
                    self.assertIn("prohibited", result["methods"].lower())

    def test_corbett_spring_turkey_only_wednesday_saturday_and_sunday(self):
        self.publish("turkey", "corbett")
        for when in ["2027-03-06", "2027-03-07", "2027-03-10", "2027-04-11"]:
            with self.subTest(date=when):
                result = self.search("turkey", "corbett", when)
                self.assertEqual(result["status"], "reviewed")
                self.assertIn("resident turkey hunters", " ".join(result["alerts"]))
                self.assertIn("No. 2 or smaller", result["methods"])
                self.assertIn("Area daily limit 1", result["bag"])
        for when in ["2027-03-08", "2027-03-09", "2027-03-11", "2027-03-12", "2027-04-12", "2026-11-07"]:
            with self.subTest(date=when):
                self.assertEqual(self.search("turkey", "corbett", when)["status"], "closed")

    def test_corbett_youth_turkey_is_separate_from_weekday_limited_spring_hunt(self):
        self.publish("turkey", "corbett")
        for when in ["2027-02-26", "2027-03-01"]:
            result = self.search("turkey", "corbett", when)
            self.assertEqual([row["season_type_code"] for row in result["matched_seasons"]], ["YOUTH_TURKEY"])
            self.assertIn("may not harvest", " ".join(result["alerts"]))
        self.assertEqual(self.search("turkey", "corbett", "2027-03-02")["status"], "closed")

    def test_deer_limits_antlers_and_muzzleloader_design_remain_area_specific(self):
        self.publish("deer", "rotenberger")
        result = self.search("deer", "rotenberger", "2026-09-05")
        self.assertIn("Area season limit 1 antlered", result["bag"])
        self.assertIn("2 points", " ".join(result["alerts"]))
        self.assertIn("20 gauge", " ".join(result["alerts"]))
        self.assertIn("ordinary archery equipment is prohibited", result["methods"])

    def test_deer_and_turkey_equipment_details_are_cited_without_expanding_area_methods(self):
        self.publish("deer", "holey-land")
        deer = self.search("deer", "holey-land", "2026-08-08")
        self.assertIn("7/8 inch", " ".join(deer["alerts"]))
        self.assertIn(".30-caliber", " ".join(deer["alerts"]))
        self.assertIn("Bows only", deer["methods"])
        self.assertIn(TAKING_GAME, [row["url"] for row in deer["sources"]])
        self.publish("turkey", "corbett")
        turkey = self.search("turkey", "corbett", "2027-03-06")
        self.assertIn("7/8 inch", " ".join(turkey["alerts"]))
        self.assertIn(".20-caliber", " ".join(turkey["alerts"]))
        self.assertIn("PCP bullets remain prohibited", " ".join(turkey["alerts"]))
        self.assertIn(TAKING_GAME, [row["url"] for row in turkey["sources"]])
        self.publish("hog", "holey-land")
        hog = self.search("hog", "holey-land", "2026-08-08")
        self.assertNotIn("7/8 inch", " ".join(hog["alerts"]))
        self.assertNotIn(TAKING_GAME, [row["url"] for row in hog["sources"]])

    def test_python_current_area_restrictions_do_not_grant_year_round_firearm_permission(self):
        for area in AREA_NAMES:
            self.publish("python", area)
            result = self.search("python", area, "2027-05-01")
            self.assertEqual(result["status"], "reviewed")
            self.assertIn("Non-firearm removal", result["methods"])
            self.assertIn("only during open brochure hunting seasons", result["methods"])
            self.assertIn("No live python", " ".join(result["alerts"]))
            self.assertIn(BROCHURES[area], [row["url"] for row in result["sources"]])

    def test_area_publication_does_not_leak_to_another_area_or_beyond_review_coverage(self):
        self.publish("hog", "holey-land")
        self.assertFalse(self.search("hog", "corbett", "2026-08-08")["verified"])
        self.assertEqual(self.search("hog", "holey-land", "2027-07-01")["status"], "no_data")
