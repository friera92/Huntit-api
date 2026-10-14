"""Independent regressions for weekday/prohibition and reviewed profile support."""
from copy import deepcopy

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.management import call_command
from django.test import TestCase

from regulations.models import LandType, ManagedArea, RegulatoryArea, Species
from .legacy_release import current_approved_legacy_snapshot, install_approved_legacy_release
from .models import RegulationDraft, RegulatoryPublication, validate_payload
from .services import species_data
from .starter import seed_review_drafts
from .turkey_data import SPECIES_INFORMATION, seed_turkey_review_drafts, turkey_sources
from .wma_data import seed_wma_review_drafts


class ExpansionEngineRegressionTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("loaddata", "demo_regulations", verbosity=0)
        install_approved_legacy_release()
        seed_review_drafts()
        seed_turkey_review_drafts()
        seed_wma_review_drafts()
        cls.reviewer = get_user_model().objects.create_superuser(username="expansion-qa-reviewer", password="Isolated-QA-9473!")
        cls.turkey = Species.objects.get(common_name="Wild Turkey")
        cls.private = LandType.objects.get(name="Private Land")
        cls.wma = LandType.objects.get(name="Wildlife Management Area (WMA)")
        cls.public = LandType.objects.get(name="Commission-Managed Land")
        cls.corbett = ManagedArea.objects.get(name="J. W. Corbett WMA")

    def publish(self, draft):
        return draft.publish(reviewer=self.reviewer, sources_checked=True,
                             review_notes="Isolated QA publication; no real database approval is performed.")

    def area_draft(self, area, land=None):
        return RegulationDraft.objects.get(species=self.turkey, land_type=land or self.wma,
                                            payload__scopes__managed_area=area.pk)

    def search(self, **overrides):
        params = {"species": self.turkey.pk, "land_type": self.wma.pk,
                  "managed_area": self.corbett.pk, "date": "2027-03-10",
                  "landowner_permission": "false"}
        params.update(overrides)
        return self.client.get("/api/regulations/search/", params)

    def test_corbett_spring_uses_iso_wednesday_saturday_sunday(self):
        self.publish(self.area_draft(self.corbett))
        for when, expected in [("2027-03-06", "reviewed"), ("2027-03-07", "reviewed"),
                               ("2027-03-08", "closed"), ("2027-03-09", "closed"),
                               ("2027-03-10", "reviewed"), ("2027-03-11", "closed"),
                               ("2027-03-12", "closed"), ("2027-04-11", "reviewed"),
                               ("2027-04-12", "closed")]:
            with self.subTest(date=when):
                response = self.search(date=when)
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.json()["status"], expected)
                if expected == "closed":
                    self.assertEqual(response.json()["matched_seasons"], [])
                    self.assertEqual(response.json()["eligibility"], "no_open_season")
        result = self.search().json()
        self.assertIn("Wednesday, Saturday, Sunday only", result["dates"])
        self.assertEqual(result["matched_seasons"][0]["periods"][0]["weekdays"], [3, 6, 7])

    def test_corbett_youth_does_not_inherit_spring_weekday_filter(self):
        self.publish(self.area_draft(self.corbett))
        for when in ["2027-02-26", "2027-02-27", "2027-02-28", "2027-03-01"]:
            with self.subTest(date=when):
                answer = self.search(date=when).json()
                self.assertEqual(answer["status"], "reviewed")
                self.assertEqual({row["season_type_code"] for row in answer["matched_seasons"]}, {"YOUTH_TURKEY"})
        self.assertEqual(self.search(date="2027-03-02").json()["status"], "closed")

    def test_holey_and_rotenberger_prohibitions_never_report_an_open_season(self):
        for area_name in ["Holey Land WMA", "Rotenberger WMA"]:
            area = ManagedArea.objects.get(name=area_name)
            for land in [self.wma, self.public]:
                self.publish(self.area_draft(area, land))
                for when in ["2026-07-01", "2026-10-12", "2027-03-06", "2027-06-30"]:
                    with self.subTest(area=area_name, land=land.name, date=when):
                        answer = self.search(managed_area=area.pk, land_type=land.pk, date=when).json()
                        self.assertTrue(answer["verified"])
                        self.assertEqual(answer["status"], "closed")
                        self.assertEqual(answer["eligibility"], "no_open_season")
                        self.assertEqual(answer["matched_seasons"], [])
                        self.assertIn("No turkey may be taken", answer["bag"])
                        self.assertIn("prohibits turkey", " ".join(answer["alerts"]))

    def test_invalid_weekday_values_and_nonboolean_prohibitions_are_rejected(self):
        original = self.area_draft(self.corbett).payload
        for invalid in [[], [0], [8], [3, 3], ["3"], [True], "Wednesday"]:
            with self.subTest(weekdays=invalid):
                data = deepcopy(original)
                data["rules"][1]["periods"][0]["weekdays"] = invalid
                with self.assertRaises(ValidationError):
                    validate_payload(data)
        for invalid in ["true", 1, None]:
            with self.subTest(prohibited=invalid):
                data = deepcopy(original)
                data["rules"][0]["prohibited"] = invalid
                with self.assertRaises(ValidationError):
                    validate_payload(data)

    def test_draft_turkey_profile_and_postapproval_live_edits_stay_invisible(self):
        Species.objects.filter(pk=self.turkey.pk).update(scientific_name="Unreviewed edit", habitat="Unreviewed habitat")
        public_profile = next(row for row in self.client.get("/api/species/").json() if row["id"] == self.turkey.pk)
        self.assertEqual(public_profile["scientific"], "")
        self.assertEqual(public_profile["habitat"], "")
        self.assertEqual(public_profile["species_information_sources"], [])
        # The earlier owner's approval covers the blank frozen original, not
        # this module's additions or later live edits.
        self.assertTrue(public_profile["species_information_reviewed"])
        self.assertEqual(public_profile["species_information_verified_at"], "2026-10-12T19:59:07+00:00")

    def test_reviewed_profile_fills_frozen_blanks_without_reading_live_edits(self):
        draft = RegulationDraft.objects.get(key="turkey-private-spring-north_sr70-2026-2027")
        published = self.publish(draft)
        Species.objects.filter(pk=self.turkey.pk).update(description="Unreviewed replacement", habitat="Unreviewed habitat")
        answer = self.search(land_type=self.private.pk, managed_area="", date="2027-03-20",
                             regulatory_area=RegulatoryArea.objects.get(code="NORTH_SR70").pk).json()
        self.assertEqual(answer["about"], SPECIES_INFORMATION["description"])
        self.assertEqual(answer["habitat"], SPECIES_INFORMATION["habitat"])
        self.assertEqual(answer["species_information_verified_at"], published.reviewed_at.isoformat())
        self.assertEqual(answer["species_information_sources"], SPECIES_INFORMATION["source_urls"])
        draft.payload["species_information"]["habitat"] = "Later unpublished draft edit"
        draft.save()
        public_profile = next(row for row in self.client.get("/api/species/").json() if row["id"] == self.turkey.pk)
        self.assertEqual(public_profile["habitat"], SPECIES_INFORMATION["habitat"])

    def test_reviewed_supplement_cannot_replace_nonblank_frozen_teammate_profile(self):
        deer = Species.objects.filter(common_name__icontains="deer").first()
        frozen = next(row for row in current_approved_legacy_snapshot()["records"]["species"] if row["id"] == deer.pk)
        draft = RegulationDraft.objects.get(key="deer-private-a1-2026-2027")
        draft.payload["species_information"] = deepcopy(SPECIES_INFORMATION)
        draft.payload["sources"] += [row for row in turkey_sources()
                                     if row["url"] in SPECIES_INFORMATION["source_urls"]]
        draft.save()
        self.publish(draft)
        result = next(row for row in self.client.get("/api/species/").json() if row["id"] == deer.pk)
        for original_key, result_key in [("scientific_name", "scientific"), ("description", "about"),
                                         ("habitat", "habitat"), ("behavior", "behavior"), ("hunting_strategy", "tactics")]:
            if frozen[original_key]:
                self.assertEqual(result[result_key], frozen[original_key])

    def test_withdrawn_supplement_does_not_supply_reviewed_profile(self):
        publication = self.publish(RegulationDraft.objects.get(key="turkey-private-spring-north_sr70-2026-2027"))
        RegulatoryPublication.objects.filter(pk=publication.pk).update(is_current=False)
        result = next(row for row in self.client.get("/api/species/").json() if row["id"] == self.turkey.pk)
        self.assertEqual(result["habitat"], "")
        self.assertEqual(result["species_information_sources"], [])

    def test_invalid_profile_field_and_uncited_profile_sources_are_rejected(self):
        original = RegulationDraft.objects.get(key="turkey-private-spring-north_sr70-2026-2027").payload
        for value in [{"unknown_field": "text", "source_urls": SPECIES_INFORMATION["source_urls"]},
                      {"habitat": "", "source_urls": SPECIES_INFORMATION["source_urls"]},
                      {"habitat": "text", "source_urls": ["https://example.invalid/profile"]},
                      {"habitat": "text", "source_urls": []}]:
            with self.subTest(profile=value):
                data = deepcopy(original)
                data["species_information"] = value
                with self.assertRaises(ValidationError):
                    validate_payload(data)

    def test_mixed_unapproved_live_profile_cannot_inherit_complete_review_flag(self):
        # This direct helper test represents a new species without an approved
        # legacy snapshot: one published addition cannot verify live prose.
        draft = RegulationDraft.objects.get(key="turkey-private-spring-north_sr70-2026-2027")
        publication = self.publish(draft)
        self.turkey.description = "Unreviewed live description"
        self.turkey.save()
        result = species_data(self.turkey, None, publications=[publication])
        self.assertEqual(result["about"], "Unreviewed live description")
        self.assertEqual(result["scientific"], SPECIES_INFORMATION["scientific_name"])
        self.assertFalse(result["species_information_reviewed"])
        self.assertIsNone(result["species_information_verified_at"])
