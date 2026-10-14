"""Dinner Island source-shape, boundary and publication-boundary regressions."""
from copy import deepcopy
from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase

from regulations.models import LandType, ManagedArea, Species
from .extra_wma_data import AREA_NAME, BROCHURE, CALENDAR, SCHEDULE, seed_extra_wma_review_drafts
from .models import RegulationDraft, RegulatoryPublication


class DinnerIslandDraftTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.added = seed_extra_wma_review_drafts()
        cls.area = ManagedArea.objects.get(name=AREA_NAME)
        cls.wma = LandType.objects.get(name="Wildlife Management Area (WMA)")
        cls.public = LandType.objects.get(name="Commission-Managed Land")
        cls.species = {kind: Species.objects.get(common_name=name) for kind, name in {
            "deer": "White Tailed Deer", "hog": "Wild Hog", "turkey": "Wild Turkey", "python": "Burmese Python",
        }.items()}
        cls.reviewer = get_user_model().objects.create_superuser(
            "dinner-test-reviewer", "dinner@example.invalid", "Test-review-only-947!",
        )

    def draft(self, kind, land=None):
        land = land or self.wma
        return RegulationDraft.objects.get(key=f"{kind}-dinner-island-{land.pk}-2026-2027")

    def publish(self, kind, land=None):
        return self.draft(kind, land).publish(
            reviewer=self.reviewer, sources_checked=True,
            review_notes="Fictional isolated QA source-review action; does not approve shipped drafts.",
        )

    def search(self, kind, day, *, land=None, area=None):
        return self.client.get("/api/regulations/search/", {
            "species": self.species[kind].pk, "land_type": (land or self.wma).pk,
            "managed_area": (area or self.area).pk, "date": day,
        })

    def test_seed_is_valid_scoped_drafts_only_for_four_species_and_two_selectors(self):
        self.assertEqual(self.added, 8)
        self.assertEqual(RegulationDraft.objects.count(), 8)
        self.assertFalse(RegulatoryPublication.objects.exists())
        for draft in RegulationDraft.objects.all():
            draft.full_clean()
            self.assertEqual(draft.payload["scopes"], {"managed_area": self.area.pk})
            self.assertEqual(draft.payload["required_inputs"], ["managed_area"])
            self.assertEqual(draft.payload["coverage"], {"start_date": "2026-07-01", "end_date": "2027-06-30"})
            self.assertIn(BROCHURE, [row["url"] for row in draft.payload["sources"]])
            self.assertIn(CALENDAR, [row["url"] for row in draft.payload["sources"]])

    def test_seed_rerun_preserves_team_draft_and_catalog_edits(self):
        draft = self.draft("hog")
        draft.payload["alerts"].append("Team's later working note.")
        draft.save()
        before = deepcopy(draft.payload)
        self.area.description = "Team-maintained description."
        self.area.save()
        self.assertEqual(seed_extra_wma_review_drafts(), 0)
        draft.refresh_from_db()
        self.area.refresh_from_db()
        self.assertEqual(draft.payload, before)
        self.assertEqual(self.area.description, "Team-maintained description.")
        self.assertFalse(RegulatoryPublication.objects.exists())

    def test_unpublished_rules_do_not_leak_as_verified_public_answers(self):
        result = self.search("hog", "2026-10-12").json()
        self.assertEqual(result["status"], "needs_review")
        self.assertFalse(result["verified"])
        self.assertEqual(result["matched_seasons"], [])
        self.assertNotIn("No hunting license", result["licenses"])
        self.assertTrue(all(row["last_verified_at"] is None for row in result["sources"]))

    def test_every_positive_rule_period_start_and_end_matches_its_exact_season(self):
        for kind in self.species:
            self.publish(kind)
            for content in self.draft(kind).payload["rules"]:
                if content.get("prohibited"):
                    continue
                for bounds in content["periods"]:
                    for endpoint in ("start_date", "end_date"):
                        with self.subTest(kind=kind, season=content["code"], day=bounds[endpoint]):
                            response = self.search(kind, bounds[endpoint])
                            self.assertEqual(response.status_code, 200)
                            result = response.json()
                            self.assertEqual(result["status"], "reviewed")
                            self.assertIn(content["code"], [row["season_type_code"] for row in result["matched_seasons"]])

    def test_every_rule_does_not_match_immediately_outside_its_periods(self):
        for kind in self.species:
            self.publish(kind)
            for content in self.draft(kind).payload["rules"]:
                if content.get("prohibited"):
                    continue
                periods = content["periods"]
                for bounds in periods:
                    for endpoint, offset in (("start_date", -1), ("end_date", 1)):
                        day = date.fromisoformat(bounds[endpoint]) + timedelta(days=offset)
                        if any(date.fromisoformat(p["start_date"]) <= day <= date.fromisoformat(p["end_date"]) for p in periods):
                            continue
                        with self.subTest(kind=kind, season=content["code"], day=day):
                            result = self.search(kind, day.isoformat()).json()
                            self.assertNotIn(content["code"], [row["season_type_code"] for row in result["matched_seasons"]])

    def test_area_and_public_land_selectors_are_not_interchangeable_with_another_area(self):
        self.publish("deer", self.wma)
        self.publish("deer", self.public)
        for land in (self.wma, self.public):
            result = self.search("deer", "2026-09-25", land=land).json()
            self.assertEqual(result["status"], "reviewed")
            self.assertIn("1 antlered deer per quota permit", result["bag"])
        other = ManagedArea.objects.create(name="Dinner Island Ranch - Caracara Unit", area_type="WMA")
        self.assertEqual(self.search("deer", "2026-09-25", area=other).json()["status"], "no_data")

    def test_deer_family_limit_supervision_and_area_antlerless_exclusion(self):
        self.publish("deer")
        family = self.search("deer", "2026-09-19").json()
        self.assertIn("2 antlered deer per family quota permit", family["bag"])
        alerts = " ".join(family["alerts"])
        self.assertIn("youth ages 8-15", alerts)
        self.assertIn("Antlerless deer are not authorized", alerts)
        self.assertIn("no operating check station", alerts)
        self.assertEqual(self.search("deer", "2026-10-19").json()["status"], "closed")

    def test_deer_muzzleloader_and_turkey_broadhead_constraints_are_present_in_active_results(self):
        self.publish("deer")
        self.publish("turkey")
        muzzle = self.search("deer", "2026-09-11").json()
        self.assertIn("at least .30 caliber", " ".join(muzzle["alerts"]))
        self.assertIn("at least 20 gauge", " ".join(muzzle["alerts"]))
        self.assertIn("7/8 inch", " ".join(muzzle["alerts"]))
        turkey = self.search("turkey", "2027-03-06").json()
        self.assertIn("7/8 inch", " ".join(turkey["alerts"]))
        self.assertIn("does not authorize bullets here", " ".join(turkey["alerts"]))
        self.assertIn("PCP airguns propelling a bolt or arrow", turkey["methods"])

    def test_hog_small_game_has_centerfire_exception_and_no_hunting_license(self):
        self.publish("hog")
        small = self.search("hog", "2027-02-20").json()
        self.assertIn("No hunting license is required", small["licenses"])
        self.assertIn("No quota permit required", small["licenses"])
        self.assertIn("centerfire rifles expressly permitted", small["methods"])
        self.assertIn("No dogs for wild hog", small["methods"])
        self.assertEqual(self.search("hog", "2027-02-21").json()["status"], "closed")

    def test_turkey_hunts_never_authorize_hog_or_fall_turkey(self):
        self.publish("hog")
        self.publish("turkey")
        for first, last in SCHEDULE["YOUTH_TURKEY"] + SCHEDULE["SPRING_TURKEY"]:
            for day in (first, last):
                with self.subTest(day=day):
                    self.assertEqual(self.search("turkey", day).json()["status"], "reviewed")
                    hog = self.search("hog", day).json()
                    self.assertEqual(hog["status"], "closed")
                    self.assertEqual(hog["eligibility"], "no_open_season")
                    self.assertEqual(hog["matched_seasons"], [])
        self.assertEqual(self.search("turkey", "2026-09-25").json()["status"], "closed")
        youth = self.search("turkey", "2027-02-26").json()
        self.assertIn("may not harvest", youth["licenses"])
        self.assertIn("No. 2 or smaller shot", youth["methods"])
        self.assertIn("1 gobbler or bearded turkey per", youth["bag"])

    def test_python_keeps_nonfirearm_year_round_and_spring_firearm_uncertainty(self):
        self.publish("python")
        for day in ["2026-07-01", "2027-03-06", "2027-06-30"]:
            with self.subTest(day=day):
                result = self.search("python", day).json()
                self.assertEqual(result["status"], "reviewed")
                self.assertIn("Non-firearm methods may be used year-round", result["methods"])
                self.assertIn("does not establish a spring/youth-turkey firearm exception", " ".join(result["alerts"]))
                self.assertIn("may not remove live pythons", " ".join(result["alerts"]))
        self.assertEqual(self.search("python", "2027-07-01").json()["status"], "no_data")

    def test_seed_rerun_does_not_restore_a_withdrawn_publication(self):
        publication = self.publish("turkey")
        RegulatoryPublication.objects.filter(pk=publication.pk).update(is_current=False)
        self.assertEqual(seed_extra_wma_review_drafts(), 0)
        self.assertEqual(self.draft("turkey").publications.count(), 1)
        self.assertFalse(self.draft("turkey").publications.filter(is_current=True).exists())
