from io import StringIO

from django.core.management import call_command
from django.test import TestCase

from regulations.models import HuntingZone, LandType, RegulatoryArea, Species
from .models import ApprovedImportedPublication, RegulatoryPublication


class VerifiedImportedSearchIntegrationTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_local_data", stdout=StringIO())
        cls.hog = Species.objects.get(common_name="Wild Hog")
        cls.turkey = Species.objects.get(common_name="Wild Turkey")
        cls.private = LandType.objects.get(name="Private Land")
        cls.zone_c = HuntingZone.objects.get(code="C")

    def search(self, **changes):
        query = {"species": self.hog.pk, "land_type": self.private.pk,
                 "date": "2026-10-12", "landowner_permission": "true"}
        query.update(changes)
        return self.client.get("/api/regulations/search/", query)

    def test_hog_keeps_curated_answer_and_adds_verified_original_notes(self):
        result = self.search().json()
        self.assertEqual(result["status"], "reviewed")
        self.assertIn("No hunting license or nighttime", result["licenses"])
        self.assertTrue(result["species_information_reviewed"])
        self.assertIn("67 counties", result["habitat"])
        records = result["additional_records"]
        self.assertTrue(records["seasons"][0]["year_round"])
        self.assertEqual(records["seasons"][0]["periods"], [])
        self.assertTrue(records["verified_at"])
        self.assertTrue(records["notes"])
        self.assertTrue(all(row["source"]["last_verified_at"] for row in records["notes"]))

    def test_turkey_fall_and_spring_gain_date_scoped_results(self):
        fall = self.search(species=self.turkey.pk, zone=self.zone_c.pk).json()
        self.assertEqual(fall["status"], "reviewed")
        self.assertTrue(fall["verified"])
        self.assertTrue(fall["matched_seasons"])
        self.assertIn("Turkey Permit", fall["licenses"])
        self.assertNotIn("not recorded", fall["licenses"].lower())
        self.assertTrue(any(row["conditions"] for row in fall["additional_records"]["bag_rules"]))
        for area in RegulatoryArea.objects.filter(code__in=["NORTH_SR70", "SOUTH_SR70"]):
            spring = self.search(species=self.turkey.pk, date="2027-03-20", regulatory_area=area.pk).json()
            self.assertEqual(spring["status"], "reviewed")
            self.assertTrue(all(any(bounds["start_date"] <= "2027-03-20" <= bounds["end_date"]
                                    for bounds in row["periods"])
                                for row in spring["matched_seasons"]))
        missing = self.search(species=self.turkey.pk, date="2027-03-20")
        self.assertEqual(missing.status_code, 400)
        self.assertIn("regulatory_area", missing.json())

    def test_closed_turkey_does_not_turn_recorded_limits_into_permission(self):
        response = self.search(species=self.turkey.pk, zone=self.zone_c.pk, date="2027-06-15",
                               regulatory_area=RegulatoryArea.objects.get(code="NORTH_SR70").pk)
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertEqual(result["status"], "closed")
        self.assertEqual(result["eligibility"], "no_open_season")
        self.assertEqual(result["matched_seasons"], [])
        self.assertTrue(result["additional_records"]["seasons"])

    def test_undated_import_does_not_extend_curated_year_round_coverage(self):
        result = self.search(date="2027-01-01").json()
        self.assertEqual(result["status"], "no_data")
        self.assertFalse(result["verified"])
        self.assertTrue(result["additional_records"]["seasons"])
        self.assertFalse(result["matched_seasons"])

    def test_live_species_and_import_edits_cannot_change_verified_results(self):
        before = self.search().json()
        self.hog.habitat = "Future unreviewed edit"
        self.hog.hunting_strategy = "Future unreviewed tactic"
        self.hog.save()
        after = self.search().json()
        self.assertEqual(after["habitat"], before["habitat"])
        self.assertEqual(after["tactics"], before["tactics"])
        catalog = self.client.get("/api/species/").json()
        self.assertEqual(next(row for row in catalog if row["id"] == self.hog.pk)["habitat"], before["habitat"])

    def test_withdrawal_and_repeat_setup_preserve_publication_controls(self):
        ApprovedImportedPublication.objects.update(is_current=False)
        call_command("seed_local_data", stdout=StringIO())
        result = self.search().json()
        self.assertNotIn("additional_records", result)
        self.assertFalse(result["species_information_reviewed"])
        self.assertEqual(result["status"], "reviewed")
        self.assertEqual(RegulatoryPublication.objects.filter(is_current=True).count(), 58)

    def test_catalog_advertises_verified_turkey_dates(self):
        scopes = self.client.get("/api/catalog/").json()["supported_scopes"]
        turkey = [row for row in scopes if row["species"] == self.turkey.pk]
        self.assertTrue(turkey)
        self.assertTrue(any(row["reviewed"] for row in turkey))
        self.assertTrue(all(row["reviewed"] for row in turkey))
