from datetime import date

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import TestCase
from django.utils import timezone
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from .serializers import SearchInputSerializer
from .services import search_imported_records as search_records

from regulations.models import (
    BagLimitRule, DeerManagementUnit, HuntingSeason, HuntingZone, LandType,
    LicensePermit, ManagedArea, RegulationNote, RegulatoryArea, SeasonPeriod,
    SeasonType, Source, Species,
)


class ImportedWorkingDataTests(TestCase):
    """The legacy importer diagnostic remains tested, but is not a public API."""
    @classmethod
    def setUpTestData(cls):
        cls.species = Species.objects.create(common_name="Wild Hog", scientific_name="Test scientific name")
        cls.private = LandType.objects.create(name="Private Land")
        cls.public = LandType.objects.create(name="Commission-Managed Land")
        cls.zone_a = HuntingZone.objects.create(name="Zone A", code="A")
        cls.zone_b = HuntingZone.objects.create(name="Zone B", code="B")
        cls.dmu_a = DeerManagementUnit.objects.create(code="A1", zone=cls.zone_a)
        cls.dmu_b = DeerManagementUnit.objects.create(code="B1", zone=cls.zone_b)
        cls.north = RegulatoryArea.objects.create(code="NORTH", name="North test area")
        cls.south = RegulatoryArea.objects.create(code="SOUTH", name="South test area")
        cls.managed = ManagedArea.objects.create(name="Test Reserve", area_type="WMA")
        cls.other_managed = ManagedArea.objects.create(name="Other Reserve", area_type="WMA")
        cls.season_type = SeasonType.objects.create(name="Test season", code="GENERAL_GUN")
        cls.year_round = SeasonType.objects.create(name="Year-round label", code="YEAR_ROUND")
        cls.source = Source.objects.create(
            organization="Test", title="Season source", url="https://myfwc.com/hunting/regulations/"
        )
        cls.bag_source = Source.objects.create(
            organization="Test", title="Bag source", url="https://myfwc.com/hunting/regulations/limits/"
        )
        cls.note_source = Source.objects.create(
            organization="Test", title="Note source", url="https://myfwc.com/hunting/regulations/notes/"
        )
        cls.permit_source = Source.objects.create(
            organization="Test", title="Permit source", url="https://myfwc.com/hunting/regulations/permits/"
        )

    def season(self, *, with_period=True, **overrides):
        fields = {
            "species": self.species, "land_type": self.private, "season_type": self.season_type,
            "season_year": "2026-2027", "source": self.source,
        }
        fields.update(overrides)
        row = HuntingSeason.objects.create(**fields)
        if with_period:
            SeasonPeriod.objects.create(season=row, start_date=date(2026, 10, 1), end_date=date(2026, 10, 31))
        return row

    def bag(self, **overrides):
        fields = {"species": self.species, "land_type": self.private, "season_year": "2026-2027",
                  "source": self.bag_source, "limit_type": "DAILY", "limit": 3}
        fields.update(overrides)
        return BagLimitRule.objects.create(**fields)

    def search(self, **overrides):
        params = {"species": self.species.pk, "land_type": self.private.pk,
                  "date": "2026-10-12", "landowner_permission": "true"}
        params.update(overrides)
        serializer = SearchInputSerializer(data=params)
        try:
            serializer.is_valid(raise_exception=True)
            response = Response(search_records(serializer.validated_data))
        except ValidationError as exc:
            response = Response(exc.detail, status=400)
        # Preserve client-like convenience in these importer diagnostic tests.
        response.json = lambda: response.data
        return response

    def test_guest_catalogs_are_active_only_and_contain_no_user_information(self):
        Species.objects.create(common_name="Inactive species", is_active=False)
        ManagedArea.objects.create(name="Inactive reserve", is_active=False)
        species = self.client.get("/api/species/")
        self.assertEqual(species.status_code, 200)
        self.assertEqual([row["id"] for row in species.json()], [self.species.pk])
        self.assertEqual(species.json()[0]["image"], "/hog.png")
        catalog = self.client.get("/api/catalog/").json()
        self.assertEqual(len(catalog["managed_areas"]), 2)
        private = next(row for row in catalog["land_types"] if row["id"] == self.private.pk)
        self.assertTrue(private["is_private"])
        self.assertFalse(private["requires_managed_area"])
        user = get_user_model().objects.create_user(username="catalog-reader")
        self.client.force_login(user)
        self.assertEqual(self.client.get("/api/catalog/").json(), catalog)
        self.assertNotIn("user", catalog)

    def test_public_endpoints_reject_writes_without_changing_data(self):
        before = (Species.objects.count(), HuntingSeason.objects.count())
        for path in ["/api/species/", "/api/catalog/", "/api/regulations/search/"]:
            for method in ["post", "put", "patch", "delete"]:
                with self.subTest(path=path, method=method):
                    response = getattr(self.client, method)(path, {}, content_type="application/json")
                    self.assertEqual(response.status_code, 405)
        self.assertEqual((Species.objects.count(), HuntingSeason.objects.count()), before)

    def test_required_identifiers_date_and_invalid_catalog_values_are_rejected(self):
        self.assertEqual(self.client.get("/api/regulations/search/").status_code, 400)
        for invalid in [{"species": 99999}, {"land_type": 99999}, {"zone": 99999},
                        {"date": "not-a-date"}, {"landowner_permission": "unknown"}]:
            with self.subTest(invalid=invalid):
                self.assertEqual(self.search(**invalid).status_code, 400)

    def test_period_boundaries_are_inclusive_without_a_different_season_fallback(self):
        season = self.season()
        for when in ["2026-10-01", "2026-10-31"]:
            with self.subTest(date=when):
                response = self.search(date=when)
                self.assertEqual(response.status_code, 200)
                self.assertEqual([row["id"] for row in response.json()["matched_seasons"]], [season.pk])
        response = self.search(date="2026-11-01").json()
        self.assertEqual(response["status"], "no_data")
        self.assertEqual(response["matched_seasons"], [])
        self.assertIn("does not establish permission", " ".join(response["alerts"]))
        self.assertNotEqual(response["sources"], [])

    def test_inactive_species_seasons_areas_and_notes_are_excluded(self):
        self.season(is_active=False)
        inactive_area = ManagedArea.objects.create(name="Closed catalog entry", is_active=False)
        self.season(land_type=self.public, managed_area=inactive_area)
        RegulationNote.objects.create(species=self.species, source=self.note_source,
                                      text="Inactive note", is_active=False)
        self.assertEqual(self.search().json()["status"], "no_data")
        self.assertEqual(self.search(land_type=self.public.pk, managed_area=inactive_area.pk).status_code, 400)
        self.species.is_active = False
        self.species.save()
        self.assertEqual(self.search().status_code, 400)

    def test_zone_selection_returns_only_general_and_exact_zone_records(self):
        general = self.season()
        exact = self.season(zone=self.zone_a)
        self.season(zone=self.zone_b)
        missing = self.search()
        self.assertEqual(missing.status_code, 400)
        self.assertIn("zone", missing.json())
        response = self.search(zone=self.zone_a.pk).json()
        self.assertEqual({row["id"] for row in response["matched_seasons"]}, {general.pk, exact.pk})

    def test_dmu_is_required_when_relevant_and_must_agree_with_zone(self):
        general = self.season(zone=self.zone_a)
        exact = self.season(zone=self.zone_a, dmu=self.dmu_a)
        self.season(zone=self.zone_b, dmu=self.dmu_b)
        missing = self.search(zone=self.zone_a.pk)
        self.assertEqual(missing.status_code, 400)
        self.assertIn("dmu", missing.json())
        mismatch = self.search(zone=self.zone_a.pk, dmu=self.dmu_b.pk)
        self.assertEqual(mismatch.status_code, 400)
        response = self.search(dmu=self.dmu_a.pk).json()
        self.assertEqual(response["query"]["zone"], self.zone_a.pk)
        self.assertEqual({row["id"] for row in response["matched_seasons"]}, {general.pk, exact.pk})

    def test_relevant_regulatory_area_is_required_without_requiring_unrelated_selectors(self):
        exact = self.season(regulatory_area=self.north)
        self.season(regulatory_area=self.south)
        missing = self.search()
        self.assertEqual(missing.status_code, 400)
        self.assertIn("regulatory_area", missing.json())
        response = self.search(regulatory_area=self.north.pk).json()
        self.assertEqual([row["id"] for row in response["matched_seasons"]], [exact.pk])

    def test_public_land_requires_a_managed_area_and_cannot_match_another_area(self):
        exact = self.season(land_type=self.public, managed_area=self.managed)
        self.season(land_type=self.public, managed_area=self.other_managed)
        self.assertEqual(self.search(land_type=self.public.pk).status_code, 400)
        response = self.search(land_type=self.public.pk, managed_area=self.managed.pk).json()
        self.assertEqual([row["id"] for row in response["matched_seasons"]], [exact.pk])
        self.assertEqual(self.search(managed_area=self.managed.pk).status_code, 400)

    def test_selected_managed_area_filters_out_unrelated_geography_requirements(self):
        unzoned = self.season(land_type=self.public, managed_area=self.managed)
        zoned = self.season(land_type=self.public, managed_area=self.other_managed, zone=self.zone_a)
        self.bag(land_type=self.public, managed_area=self.other_managed, zone=self.zone_a, limit=9)

        response = self.search(land_type=self.public.pk, managed_area=self.managed.pk)
        self.assertEqual(response.status_code, 200)
        self.assertEqual([row["id"] for row in response.json()["matched_seasons"]], [unzoned.pk])
        self.assertNotIn("DAILY: 9", response.json()["bag"])

        missing = self.search(land_type=self.public.pk, managed_area=self.other_managed.pk)
        self.assertEqual(missing.status_code, 400)
        self.assertIn("zone", missing.json())
        response = self.search(land_type=self.public.pk, managed_area=self.other_managed.pk, zone=self.zone_a.pk)
        self.assertEqual(response.status_code, 200)
        self.assertEqual([row["id"] for row in response.json()["matched_seasons"]], [zoned.pk])
        self.assertIn("DAILY: 9", response.json()["bag"])

    def test_year_round_labels_disclose_missing_bounds_and_do_not_match_unrelated_years(self):
        season = self.season(with_period=False, season_type=self.year_round)
        response = self.search().json()
        self.assertEqual([row["id"] for row in response["matched_seasons"]], [season.pk])
        self.assertIn("explicit date bounds", response["dates"])
        self.assertFalse(response["verified"])
        self.assertEqual(self.search(date="2030-10-12").json()["status"], "no_data")

    def test_sources_include_seasons_bag_notes_and_permits_without_automatic_review(self):
        season = self.season()
        permit = LicensePermit.objects.create(name="Test permit", source=self.permit_source, requirements="Test conditions")
        season.permits.add(permit)
        self.bag()
        RegulationNote.objects.create(species=self.species, land_type=self.private, source=self.note_source,
                                      season_year="2026-2027", title="Test exception", text="Test exception text")
        self.source.last_verified_at = timezone.now()
        self.source.save()
        response = self.search().json()
        self.assertEqual({row["title"] for row in response["sources"]},
                         {"Season source", "Bag source", "Note source", "Permit source"})
        self.assertIn("Test permit", response["licenses"])
        self.assertIn("Test exception", " ".join(response["alerts"]))
        self.assertFalse(response["verified"])
        self.assertEqual(response["status"], "unverified")
        self.assertIsNotNone(next(row for row in response["sources"] if row["title"] == "Season source")["last_verified_at"])

    def test_bag_rules_obey_geography_year_season_type_and_group(self):
        self.season(zone=self.zone_a)
        self.bag(zone=self.zone_a, limit=3)
        self.bag(zone=self.zone_b, limit=17)
        self.bag(zone=self.zone_a, season_year="2030-2031", limit=99)
        other_type = SeasonType.objects.create(name="Other type", code="ARCHERY")
        self.bag(zone=self.zone_a, season_type=other_type, limit=88)
        self.bag(zone=self.zone_a, season_group="SPRING", limit=77)
        response = self.search(zone=self.zone_a.pk).json()
        self.assertIn("DAILY: 3", response["bag"])
        for value in [17, 99, 88, 77]:
            self.assertNotIn(f"DAILY: {value}", response["bag"])

    def test_missing_permits_and_methods_are_unknown_and_permission_input_is_preserved(self):
        self.season()
        response = self.search(landowner_permission="false").json()
        self.assertIn("not recorded", response["licenses"])
        self.assertIn("not recorded", response["methods"])
        self.assertFalse(response["query"]["landowner_permission"])
        self.assertTrue(any("not confirmed" in alert for alert in response["alerts"]))


class AdminIntegrationTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.species = Species.objects.create(common_name="Admin test species")
        cls.land_type = LandType.objects.create(name="Public test land")
        cls.area = ManagedArea.objects.create(name="Searchable Reserve", area_type="WMA")
        cls.season_type = SeasonType.objects.create(name="Admin test season", code="ADMIN_TEST")
        cls.source = Source.objects.create(organization="Test", title="Admin source", url="https://myfwc.com/")
        cls.season = HuntingSeason.objects.create(
            species=cls.species, land_type=cls.land_type, managed_area=cls.area,
            season_type=cls.season_type, season_year="2026-2027", source=cls.source,
        )
        cls.staff = get_user_model().objects.create_user(username="viewer", is_staff=True)
        cls.staff.user_permissions.add(Permission.objects.get(codename="view_huntingseason", content_type__app_label="regulations"))

    def test_admin_search_uses_managed_area_and_requires_staff_access(self):
        path = "/admin/regulations/huntingseason/?q=Searchable"
        self.assertEqual(self.client.get(path).status_code, 302)
        ordinary = get_user_model().objects.create_user(username="ordinary")
        self.client.force_login(ordinary)
        self.assertEqual(self.client.get(path).status_code, 302)
        self.client.force_login(self.staff)
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Searchable Reserve")

    def test_view_permission_does_not_grant_admin_write_permission(self):
        self.client.force_login(self.staff)
        response = self.client.post(f"/admin/regulations/huntingseason/{self.season.pk}/change/", {"season_year": "2030-2031"})
        self.assertEqual(response.status_code, 403)
        self.season.refresh_from_db()
        self.assertEqual(self.season.season_year, "2026-2027")
