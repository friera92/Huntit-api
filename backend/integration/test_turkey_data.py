"""Boundary and publication QA for the additional FWC turkey edition."""
from copy import deepcopy

from django.contrib.auth import get_user_model
from django.test import TestCase

from regulations.models import HuntingSeason, HuntingZone, LandType, RegulatoryArea, Species
from .models import RegulationDraft, RegulatoryPublication, validate_payload
from .turkey_data import (
    EXEMPTIONS, FALL_DATES, HARVEST, LICENSES, METHODS, PROFILE, SEASONS,
    SPECIES_INFORMATION, SPRING_DATES, YOUTH, seed_turkey_review_drafts,
)


class TurkeyDataTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Represent a teammate's original blank turkey profile. Supplements must
        # not overwrite its working record or inherit historical approval.
        cls.turkey = Species.objects.create(common_name="Wild Turkey")
        seed_turkey_review_drafts()
        cls.private = LandType.objects.get(name="Private Land")
        cls.zones = {row.code: row for row in HuntingZone.objects.all()}
        cls.regions = {row.code: row for row in RegulatoryArea.objects.all()}
        cls.reviewer = get_user_model().objects.create_superuser(username="turkey-qa-reviewer", password="Isolated-QA-5824!")

    def publish(self):
        for draft in RegulationDraft.objects.filter(species=self.turkey):
            draft.publish(reviewer=self.reviewer, sources_checked=True,
                          review_notes="Isolated test approval for source-linked turkey boundary QA.")

    def search(self, **overrides):
        params = {"species": self.turkey.pk, "land_type": self.private.pk,
                  "date": "2026-10-05", "landowner_permission": "true"}
        params.update(overrides)
        return self.client.get("/api/regulations/search/", params)

    def test_drafts_do_not_approve_or_modify_original_working_records(self):
        self.assertEqual(RegulationDraft.objects.count(), 6)
        self.assertEqual(sum(len(row.payload["rules"]) for row in RegulationDraft.objects.all()), 20)
        self.assertEqual(sum(len(rule["periods"]) for row in RegulationDraft.objects.all()
                             for rule in row.payload["rules"]), 23)
        self.assertFalse(RegulatoryPublication.objects.exists())
        self.assertFalse(HuntingSeason.objects.exists())
        self.turkey.refresh_from_db()
        self.assertEqual(self.turkey.description, "")
        self.assertEqual(self.turkey.scientific_name, "")
        answer = self.search(zone=self.zones["A"].pk).json()
        self.assertEqual(answer["status"], "needs_review")
        self.assertFalse(answer["verified"])
        self.assertNotIn("Turkey Permit required", answer["licenses"])

    def test_all_payloads_are_valid_and_source_linked(self):
        for row in RegulationDraft.objects.all():
            validate_payload(row.payload)
            row.full_clean()
            urls = {source["url"] for source in row.payload["sources"]}
            self.assertTrue({SEASONS, LICENSES, EXEMPTIONS, METHODS, HARVEST, YOUTH, PROFILE}.issubset(urls))
            self.assertTrue(set(row.payload["species_information"]["source_urls"]).issubset(urls))
            for item in row.payload["rules"]:
                self.assertEqual(item["category"], "Gobblers and bearded turkeys only")
                self.assertNotIn("unknown", item["licenses"].lower())
                self.assertNotIn("unknown", item["methods"].lower())

    def test_repeat_seed_preserves_local_draft_edits(self):
        row = RegulationDraft.objects.first()
        content = deepcopy(row.payload)
        content["alerts"].append("Administrator working note.")
        row.payload = content
        row.save()
        self.assertEqual(seed_turkey_review_drafts(), 0)
        row.refresh_from_db()
        self.assertEqual(row.payload, content)
        self.assertFalse(RegulatoryPublication.objects.exists())

    def test_zone_a_fall_gap_and_open_boundary(self):
        self.publish()
        gap = self.search(zone=self.zones["A"].pk, date="2026-10-04").json()
        start = self.search(zone=self.zones["A"].pk, date="2026-10-05").json()
        end = self.search(zone=self.zones["A"].pk, date="2026-10-18").json()
        closed = self.search(zone=self.zones["A"].pk, date="2026-10-19").json()
        self.assertEqual([answer["status"] for answer in [gap, start, end, closed]],
                         ["closed", "reviewed", "reviewed", "closed"])
        self.assertIn("Turkey Permit required", start["licenses"])
        self.assertIn("Shotguns, rifles", start["methods"])
        self.assertIn("Daily limit 2", start["bag"])

    def test_turkey_fall_does_not_inherit_longer_deer_gun_season(self):
        self.publish()
        for zone, open_day, closed_day in [("B", "2027-01-31", "2027-02-01"),
                                           ("C", "2027-01-03", "2027-01-04"),
                                           ("D", "2027-01-17", "2027-01-18")]:
            with self.subTest(zone=zone):
                self.assertEqual(self.search(zone=self.zones[zone].pk, date=open_day).json()["status"], "reviewed")
                # February uses the spring geography even before a season opens.
                extra = {"regulatory_area": self.regions["NORTH_SR70"].pk} if closed_day.startswith("2027-02") else {}
                self.assertEqual(self.search(zone=self.zones[zone].pk, date=closed_day, **extra).json()["status"], "closed")

    def test_split_zone_d_crossbow_gap_is_closed_for_that_method(self):
        self.publish()
        gap = self.search(zone=self.zones["D"].pk, date="2026-11-28").json()
        resumed = self.search(zone=self.zones["D"].pk, date="2026-11-30").json()
        # Fall gun turkey is open during the crossbow gap; it must not be
        # mislabeled as an open crossbow season or require its season permit.
        self.assertEqual({row["season_type_code"] for row in gap["matched_seasons"]}, {"FALL_TURKEY"})
        self.assertEqual({row["season_type_code"] for row in resumed["matched_seasons"]}, {"CROSSBOW"})
        self.assertIn("Crossbow season permit", resumed["licenses"])
        self.assertIn("Crossbows, bows and airbows", resumed["methods"])

    def test_archery_and_muzzleloading_permits_and_methods(self):
        self.publish()
        archery = self.search(zone=self.zones["C"].pk, date="2026-09-20").json()
        muzzle = self.search(zone=self.zones["C"].pk, date="2026-10-30").json()
        self.assertIn("Archery season permit", archery["licenses"])
        self.assertIn("Bows only", archery["methods"])
        self.assertIn("Muzzleloading gun season permit", muzzle["licenses"])
        self.assertIn("Muzzleloaders, crossbows", muzzle["methods"])

    def test_spring_uses_sr70_instead_of_requiring_a_zone(self):
        self.publish()
        north = self.search(regulatory_area=self.regions["NORTH_SR70"].pk, date="2027-03-20")
        south = self.search(regulatory_area=self.regions["SOUTH_SR70"].pk, date="2027-03-06")
        self.assertEqual((north.status_code, south.status_code), (200, 200))
        self.assertEqual(north.json()["status"], "reviewed")
        self.assertEqual(south.json()["status"], "reviewed")
        self.assertEqual(self.search(date="2027-03-20").status_code, 400)
        self.assertEqual(self.search(date="2026-10-05").status_code, 400)

    def test_all_four_youth_days_and_earliest_reporting_conditions(self):
        self.publish()
        for region, first, last, next_day in [("SOUTH_SR70", "2027-02-26", "2027-03-01", "2027-03-02"),
                                               ("NORTH_SR70", "2027-03-12", "2027-03-15", "2027-03-16")]:
            with self.subTest(region=region):
                beginning = self.search(regulatory_area=self.regions[region].pk, date=first).json()
                ending = self.search(regulatory_area=self.regions[region].pk, date=last).json()
                after = self.search(regulatory_area=self.regions[region].pk, date=next_day).json()
                self.assertEqual([answer["status"] for answer in [beginning, ending, after]], ["reviewed", "reviewed", "closed"])
                self.assertIn("Youth-hunt harvest counts", beginning["bag"])
                self.assertIn("they may not shoot", beginning["licenses"])
                alerts = " ".join(beginning["alerts"])
                self.assertIn("15 and younger", alerts)
                self.assertIn("24 hours", alerts)
                self.assertIn("whichever is first", alerts)
                self.assertIn("does not submit an FWC report", alerts)

    def test_hours_baiting_equipment_and_permission_are_explicit(self):
        self.publish()
        fall = self.search(zone=self.zones["A"].pk).json()
        spring = self.search(regulatory_area=self.regions["NORTH_SR70"].pk, date="2027-03-20",
                             landowner_permission="false").json()
        self.assertIn("one-half hour after sunset", " ".join(fall["alerts"]))
        self.assertIn("sunset during spring", " ".join(spring["alerts"]))
        self.assertNotIn("one-half hour after sunset", " ".join(spring["alerts"]))
        self.assertEqual(spring["eligibility"], "permission_required")
        for detail in ["100 yards", "roosted", "7/8 inch", ".20-caliber", "name, address"]:
            self.assertIn(detail, " ".join(spring["alerts"]))

    def test_species_supplement_is_source_linked_and_does_not_mutate_catalog(self):
        self.assertEqual(SPECIES_INFORMATION["scientific_name"], "Meleagris gallopavo")
        for key in ["description", "habitat", "behavior", "hunting_strategy", "source_urls"]:
            self.assertTrue(SPECIES_INFORMATION[key])
        self.turkey.refresh_from_db()
        self.assertEqual(self.turkey.habitat, "")
        self.assertEqual(self.turkey.behavior, "")

    def test_new_edition_does_not_extend_beyond_explicit_coverage(self):
        self.publish()
        result = self.search(regulatory_area=self.regions["NORTH_SR70"].pk, date="2027-07-01").json()
        self.assertFalse(result["verified"])
        self.assertEqual(result["status"], "no_data")
        self.assertEqual(result["matched_seasons"], [])
