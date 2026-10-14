"""Frozen-search acceptance tests: scopes, dates, unknowns and provenance."""
from copy import deepcopy
from datetime import date
import json
from pathlib import Path

from django.test import SimpleTestCase
from rest_framework.exceptions import ValidationError

from .legacy_search import ApprovedLegacySearch


class Context:
    def __init__(self, when="2026-10-12", **selections):
        self.hunting_date = date.fromisoformat(when)
        self.selections = {"species": 1, "land_type": 1, **selections}

    def identifier(self, field):
        return self.selections.get(field)

    def require(self, fields):
        missing = {field: ["Select this location."] for field in fields if self.identifier(field) is None}
        if missing:
            raise ValidationError(missing)


def snapshot():
    return {"approval": {"recorded_at": "2026-10-12T19:59:07+00:00",
                         "verification_basis": "Project owner verification confirmation."},
            "records": {
                "source": [{"id": 1, "organization": "FWC", "title": "Original source",
                            "url": "https://myfwc.com/hunting/season-dates/", "document_type": "Web Page",
                            "effective_date": None, "retrieved_at": "2026-10-07T00:27:51.879Z",
                            "last_verified_at": None, "notes": "Outside WMA system."}],
                "landtype": [{"id": 1, "name": "Private Land"}, {"id": 2, "name": "Commission-Managed Land"}],
                "huntingzone": [{"id": 1, "code": "A"}, {"id": 2, "code": "B"}],
                "deermanagementunit": [{"id": 1, "code": "A1", "zone": 1}],
                "regulatoryarea": [{"id": 1, "code": "NORTH", "name": "North of State Road 70"}],
                "managedarea": [{"id": 1, "name": "First WMA", "is_active": True},
                                {"id": 2, "name": "Other WMA", "is_active": True}],
                "seasontype": [{"id": 1, "name": "General gun", "code": "GENERAL_GUN", "description": "Lawful guns only."},
                               {"id": 2, "name": "Year-round", "code": "YEAR_ROUND", "description": ""},
                               {"id": 3, "name": "Archery", "code": "ARCHERY", "description": "Bows only."},
                               {"id": 4, "name": "Spring turkey", "code": "SPRING_TURKEY", "description": ""},
                               {"id": 5, "name": "Youth turkey", "code": "YOUTH_TURKEY", "description": ""}],
                "harvestcategory": [{"id": 1, "name": "Antlered"}], "huntingseason": [],
                "seasonperiod": [], "baglimitrule": [], "regulationnote": [],
                "licensepermit": [], "legalmethod": [],
            }}


def season(data, identifier=1, periods=(("2026-10-01", "2026-10-31", "Recorded restriction."),), **values):
    row = {"id": identifier, "species": 1, "land_type": 1, "season_type": 1,
           "season_year": "2026-2027", "harvest_category": 1, "source": 1,
           "is_active": True, "notes": "Season-specific note.", "permits": [], "legal_methods": [], **values}
    data["records"]["huntingseason"].append(row)
    for start, end, note in periods:
        data["records"]["seasonperiod"].append({"id": len(data["records"]["seasonperiod"]) + 1,
                                                "season": identifier, "start_date": start,
                                                "end_date": end, "notes": note})
    return row


def bag(data, identifier=1, **values):
    row = {"id": identifier, "species": 1, "land_type": 1, "season_year": "2026-2027",
           "limit_type": "DAILY", "limit": 2, "is_unlimited": False, "conditions": "",
           "source": 1, "is_active": True, **values}
    data["records"]["baglimitrule"].append(row)
    return row


class ApprovedLegacySearchTests(SimpleTestCase):
    # SimpleTestCase prohibits all database queries: every relationship below
    # must come from the supplied frozen copy, even while working tables change.

    def test_no_snapshot_exposes_no_unapproved_information(self):
        search = ApprovedLegacySearch(Context(), None)
        self.assertFalse(search.has_coverage)
        self.assertEqual(search.active_seasons, [])
        self.assertEqual(search.sources, [])
        self.assertIsNone(search.records()["verified_at"])

    def test_period_boundaries_are_inclusive_and_full_closed_periods_keep_notes(self):
        data = snapshot()
        season(data, periods=(("2026-10-01", "2026-10-31", "First exact note."),
                              ("2026-12-01", "2026-12-05", "Second exact note.")))
        for when in ["2026-10-01", "2026-10-31", "2026-12-05"]:
            with self.subTest(when=when):
                search = ApprovedLegacySearch(Context(when), data)
                self.assertEqual(len(search.active_seasons), 1)
                self.assertEqual(len(search.records()["seasons"][0]["periods"]), 2)
        closed = ApprovedLegacySearch(Context("2026-11-01"), data)
        self.assertTrue(closed.has_coverage)
        self.assertEqual(closed.active_seasons, [])
        self.assertEqual(closed.records()["seasons"][0]["periods"][1]["notes"], "Second exact note.")
        self.assertEqual(closed.coverage, [{"start_date": "2026-10-01", "end_date": "2026-10-31"},
                                           {"start_date": "2026-12-01", "end_date": "2026-12-05"}])
        self.assertFalse(ApprovedLegacySearch(Context("2028-10-12"), data).has_coverage)

    def test_undated_year_round_keeps_coarse_year_without_inventing_periods(self):
        data = snapshot()
        season(data, periods=(), season_type=2)
        for when in ["2026-01-01", "2027-12-31"]:
            result = ApprovedLegacySearch(Context(when), data)
            self.assertTrue(result.active_seasons[0]["year_round"])
            self.assertEqual(result.active_seasons[0]["periods"], [])
            self.assertEqual(result.coverage, [])
            self.assertEqual(result.active_seasons[0]["season_year"], "2026-2027")
        self.assertFalse(ApprovedLegacySearch(Context("2028-01-01"), data).has_coverage)
        # A missing period on an ordinary season never establishes an open date.
        data["records"]["huntingseason"][0]["season_type"] = 1
        self.assertEqual(ApprovedLegacySearch(Context(), data).active_seasons, [])

    def test_all_supplied_scopes_filter_before_unrelated_requirements(self):
        data = snapshot()
        season(data, land_type=2, managed_area=1)
        season(data, 2, land_type=2, managed_area=2, zone=2, dmu=1)
        result = ApprovedLegacySearch(Context(land_type=2, managed_area=1), data)
        self.assertEqual([row["id"] for row in result.active_seasons], [1])
        self.assertIn("First WMA", result.active_seasons[0]["scope"])
        with self.assertRaises(ValidationError) as caught:
            ApprovedLegacySearch(Context(land_type=2), data).records()
        self.assertIn("managed_area", caught.exception.detail)

    def test_turkey_requires_active_family_selectors_without_closed_other_family(self):
        data = snapshot()
        season(data, season_type=3, zone=1)
        season(data, 2, season_type=4, regulatory_area=1,
               periods=(("2027-03-20", "2027-04-25", "Spring note."),))
        with self.assertRaises(ValidationError) as caught:
            ApprovedLegacySearch(Context(), data).records()
        self.assertEqual(set(caught.exception.detail), {"zone"})
        autumn = ApprovedLegacySearch(Context(zone=1), data)
        self.assertEqual([row["id"] for row in autumn.records()["seasons"]], [1])
        spring = ApprovedLegacySearch(Context("2027-03-25", regulatory_area=1), data)
        self.assertEqual([row["id"] for row in spring.records()["seasons"]], [2])

    def test_closed_scoped_family_does_not_force_unselected_other_family(self):
        data = snapshot()
        season(data, season_type=3, zone=1)
        season(data, 2, season_type=4, regulatory_area=1,
               periods=(("2027-03-20", "2027-04-25", ""),))
        result = ApprovedLegacySearch(Context("2026-11-12", zone=1), data)
        self.assertTrue(result.has_coverage)
        self.assertEqual(result.active_seasons, [])
        self.assertEqual([row["id"] for row in result.records()["seasons"]], [1])
        with self.assertRaises(ValidationError) as caught:
            ApprovedLegacySearch(Context("2026-11-12"), data).records()
        self.assertEqual(set(caught.exception.detail), {"zone", "regulatory_area"})

    def test_turkey_bags_follow_fall_archery_and_spring_youth_families(self):
        data = snapshot()
        season(data, season_type=3, zone=1)
        season(data, 2, season_type=5, regulatory_area=1,
               periods=(("2027-03-12", "2027-03-15", "Youth restrictions."),))
        bag(data, season_group="FALL", limit=2)
        bag(data, 2, season_group="SPRING", limit=1)
        autumn = ApprovedLegacySearch(Context(zone=1, regulatory_area=1), data).records()
        self.assertEqual([row["id"] for row in autumn["bag_rules"]], [1])
        self.assertIn("DAILY: 2", autumn["seasons"][0]["bag"])
        # A displayed closed spring season retains its own spring rule.
        self.assertIn("DAILY: 1", autumn["seasons"][1]["bag"])
        spring = ApprovedLegacySearch(Context("2027-03-13", regulatory_area=1), data).records()
        self.assertEqual([row["id"] for row in spring["bag_rules"]], [2])

    def test_preserves_linked_permit_and_method_text_and_frozen_inputs(self):
        data = snapshot()
        season(data, permits=[9], legal_methods=[8])
        data["records"]["licensepermit"] = [{"id": 9, "name": "Example permit", "description": "Full permit description.",
                                               "requirements": "Full permit requirement.", "source": 1, "is_active": True}]
        data["records"]["legalmethod"] = [{"id": 8, "name": "Example method", "description": "Full method restriction."}]
        original = deepcopy(data)
        result = ApprovedLegacySearch(Context(), data).records()["seasons"][0]
        self.assertIn("Full permit description.", result["licenses"])
        self.assertIn("Full permit requirement.", result["licenses"])
        self.assertIn("Full method restriction.", result["methods"])
        self.assertIn("Lawful guns only.", result["methods"])
        self.assertEqual(data, original)

    def test_missing_values_remain_unknown_and_inactive_rows_do_not_appear(self):
        data = snapshot()
        season(data, season_type=2)
        season(data, 2, is_active=False)
        season(data, 3, land_type=2, managed_area=1)
        data["records"]["managedarea"][0]["is_active"] = False
        result = ApprovedLegacySearch(Context(), data).records()["seasons"]
        self.assertEqual([row["id"] for row in result], [1])
        self.assertIn("not recorded", result[0]["licenses"])
        self.assertIn("not recorded", result[0]["bag"])
        self.assertIn("not recorded", result[0]["methods"])
        self.assertFalse(ApprovedLegacySearch(Context(land_type=2, managed_area=1), data).has_coverage)

    def test_wma_advisory_is_not_private_rule_or_season_coverage(self):
        data = snapshot()
        data["records"]["regulationnote"] = [{"id": 1, "species": 1, "land_type": None,
                                               "season_year": "2026-2027", "title": "WMA-Specific Wild Hog Regulations",
                                               "text": "Area-specific seasons apply.", "source": 1, "is_active": True}]
        self.assertEqual(ApprovedLegacySearch(Context(), data).records()["notes"], [])
        public = ApprovedLegacySearch(Context(land_type=2, managed_area=1), data)
        self.assertFalse(public.has_coverage)
        self.assertEqual(public.active_seasons, [])
        self.assertIn("WMA advisory", public.records()["notes"][0]["scope"])
        self.assertEqual(len(public.sources), 1)

    def test_sources_distinguish_user_approval_from_original_unverified_metadata(self):
        data = snapshot()
        season(data)
        source = ApprovedLegacySearch(Context(), data).sources[0]
        self.assertEqual(source["last_verified_at"], data["approval"]["recorded_at"])
        self.assertEqual(source["verification_basis"], data["approval"]["verification_basis"])
        self.assertIsNone(source["original_last_verified_at"])
        self.assertIsNone(source["source_checked_on"])
        self.assertIsNone(source["effective_date"])
        self.assertEqual(source["notes"], "Outside WMA system.")
        self.assertEqual(source["retrieved_at"], "2026-10-07T00:27:51.879Z")

    def test_actual_original_fixture_scopes_seasons_exceptions_and_unicode(self):
        data = snapshot()
        original = json.loads((Path(__file__).parent / "fixtures" / "demo_regulations.json").read_text(encoding="utf-8"))
        data["records"] = {}
        for row in original:
            data["records"].setdefault(row["model"].removeprefix("regulations."), []).append(
                {"id": row["pk"], **row["fields"]})
        # Source text comes from the frozen UTF-8 copy, not the working DB's
        # historical replacement-character corruption.
        hog = ApprovedLegacySearch(Context(species=2), data)
        self.assertEqual(len(hog.active_seasons), 1)
        self.assertIn("owner’s", hog.records()["notes"][0]["text"])
        self.assertEqual(len(hog.records()["notes"]), 1)
        self.assertEqual(len(hog.active_seasons[0]["periods"]), 0)
        turkey = ApprovedLegacySearch(Context("2026-08-05", species=4, zone=1), data)
        self.assertEqual({row["code"] for row in turkey.active_seasons}, {"ARCHERY", "CROSSBOW"})
        self.assertEqual(len(turkey.records()["seasons"]), 4)
        self.assertEqual(len(turkey.records()["bag_rules"]), 3)
        north = ApprovedLegacySearch(Context("2027-03-13", species=4, regulatory_area=1), data)
        self.assertEqual([row["code"] for row in north.active_seasons], ["YOUTH_TURKEY"])
        self.assertEqual(north.active_seasons[0]["periods"][0]["start_date"], "2027-03-12")
        deer = ApprovedLegacySearch(Context("2026-12-15", species=3, zone=4, dmu=12), data)
        exceptions = [row for row in deer.records()["bag_rules"] if row["category"] == "Antlerless"]
        self.assertEqual({row["limit"] for row in exceptions}, {2, 3})
        self.assertIn("D2", next(row["scope"] for row in exceptions if row["limit"] == 3))
        python = ApprovedLegacySearch(Context(species=1, land_type=3, managed_area=13), data)
        self.assertEqual(len(python.active_seasons), 1)
        self.assertIn("Corbett", python.active_seasons[0]["scope"])
        self.assertFalse(ApprovedLegacySearch(Context(species=4, land_type=2, managed_area=13), data).has_coverage)
