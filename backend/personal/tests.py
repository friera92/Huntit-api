from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.db.models.deletion import ProtectedError
from django.test import TestCase
from django.utils import timezone

from regulations.models import DeerManagementUnit, HuntingZone, LandType, ManagedArea, Species

from .models import Harvest, SavedSearch, UserLicense, UserPreference


class PersonalDataTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(username="hunter_a", password="test-password-for-a")
        cls.other_user = get_user_model().objects.create_user(username="hunter_b", password="test-password-for-b")
        cls.species = Species.objects.create(common_name="Synthetic species")
        cls.private = LandType.objects.create(name="Private Land")
        cls.public = LandType.objects.create(name="Wildlife Management Area (WMA)")
        cls.commission = LandType.objects.create(name="Commission-Managed Land")
        cls.area = ManagedArea.objects.create(name="Synthetic test WMA", area_type="WMA")
        cls.zone_a = HuntingZone.objects.create(name="Synthetic zone A", code="A")
        cls.zone_b = HuntingZone.objects.create(name="Synthetic zone B", code="B")
        cls.dmu_a1 = DeerManagementUnit.objects.create(code="A1", zone=cls.zone_a)

    def search(self, **overrides):
        fields = {
            "user": self.user, "species": self.species, "land_type": self.private,
            "hunting_date": date(2026, 12, 1),
        }
        fields.update(overrides)
        return SavedSearch.objects.create(**fields)

    def harvest(self, **overrides):
        fields = {
            "user": self.user, "species": self.species, "harvest_date": timezone.localdate(),
            "location": "Synthetic private property",
        }
        fields.update(overrides)
        return Harvest.objects.create(**fields)

    def test_preferences_link_existing_catalog_and_survive_reloading(self):
        preference = UserPreference.objects.create(user=self.user)
        preference.species.add(self.species)
        preference.managed_areas.add(self.area)
        preference.zones.add(self.zone_a)
        reloaded = get_user_model().objects.get(pk=self.user.pk).preferences
        self.assertEqual(list(reloaded.species.all()), [self.species])
        self.assertEqual(list(reloaded.managed_areas.all()), [self.area])
        self.assertEqual(list(reloaded.zones.all()), [self.zone_a])
        with self.assertRaises(ValidationError):
            UserPreference.objects.create(user=self.user)

    def test_user_license_defaults_to_unknown_and_preserves_self_report(self):
        license_report = UserLicense.objects.create(user=self.user, name="Synthetic license")
        self.assertEqual(license_report.status, UserLicense.Status.UNKNOWN)
        license_report.status = UserLicense.Status.HELD
        license_report.save()
        self.assertEqual(self.user.reported_licenses.get().status, "held")

    def test_license_date_validation_and_database_constraint(self):
        with self.assertRaises(ValidationError):
            UserLicense.objects.create(
                user=self.user, name="Synthetic license",
                valid_from=date(2026, 10, 12), expires_on=date(2026, 10, 11),
            )
        license_report = UserLicense.objects.create(user=self.user, name="Synthetic license")
        with self.assertRaises(IntegrityError), transaction.atomic():
            UserLicense.objects.filter(pk=license_report.pk).update(
                valid_from=date(2026, 10, 12), expires_on=date(2026, 10, 11),
            )

    def test_license_status_is_constrained_even_when_validation_is_bypassed(self):
        license_report = UserLicense.objects.create(user=self.user, name="Synthetic license")
        with self.assertRaises(IntegrityError), transaction.atomic():
            UserLicense.objects.filter(pk=license_report.pk).update(status="officially_verified")

    def test_saved_search_stores_inputs_and_allows_future_planning_dates(self):
        search = self.search(zone=self.zone_a, dmu=self.dmu_a1)
        reloaded = SavedSearch.objects.get(pk=search.pk)
        self.assertEqual(reloaded.hunting_date, date(2026, 12, 1))
        self.assertEqual(reloaded.species, self.species)
        self.assertEqual(reloaded.dmu, self.dmu_a1)
        self.assertNotIn("results", {field.name for field in SavedSearch._meta.fields})

    def test_dmu_must_match_selected_zone(self):
        for zone in [None, self.zone_b]:
            with self.subTest(zone=zone), self.assertRaises(ValidationError):
                self.search(zone=zone, dmu=self.dmu_a1)
        self.assertFalse(SavedSearch.objects.exists())

    def test_each_public_land_type_requires_a_managed_area(self):
        for land_type in [self.public, self.commission]:
            with self.subTest(land_type=land_type), self.assertRaises(ValidationError):
                self.search(land_type=land_type)
            saved = self.search(land_type=land_type, managed_area=self.area)
            self.assertEqual(saved.managed_area, self.area)

    def test_private_land_rejects_public_area_and_unknown_types_require_explicit_support(self):
        with self.assertRaises(ValidationError):
            self.search(managed_area=self.area)
        unsupported = LandType.objects.create(name="Synthetic unsupported land classification")
        with self.assertRaises(ValidationError):
            self.search(land_type=unsupported)

    def test_harvest_survives_reloading_with_private_location_or_catalog_area(self):
        private = self.harvest()
        public = self.harvest(location="", managed_area=self.area, quantity=2)
        self.assertEqual(Harvest.objects.get(pk=private.pk).location, "Synthetic private property")
        self.assertEqual(Harvest.objects.get(pk=public.pk).managed_area, self.area)
        self.assertEqual(Harvest.objects.get(pk=public.pk).quantity, 2)

    def test_harvest_rejects_missing_location_future_date_and_zero_quantity(self):
        for fields in [
            {"location": ""}, {"location": "   "},
            {"harvest_date": timezone.localdate() + timedelta(days=1)}, {"quantity": 0},
        ]:
            with self.subTest(fields=fields), self.assertRaises(ValidationError):
                self.harvest(**fields)
        self.assertFalse(Harvest.objects.exists())

    def test_sqlite_checks_harvest_quantity_and_location_on_bulk_updates(self):
        harvest = self.harvest()
        for fields in [{"quantity": 0}, {"location": "", "managed_area": None}]:
            with self.subTest(fields=fields), self.assertRaises(IntegrityError), transaction.atomic():
                Harvest.objects.filter(pk=harvest.pk).update(**fields)
        harvest.refresh_from_db()
        self.assertEqual(harvest.quantity, 1)
        self.assertEqual(harvest.location, "Synthetic private property")

    def test_owner_relationships_support_separate_user_queries(self):
        first = self.search()
        second = self.search(user=self.other_user)
        first_harvest = self.harvest()
        second_harvest = self.harvest(user=self.other_user)
        self.assertEqual(list(self.user.saved_searches.all()), [first])
        self.assertEqual(list(self.other_user.saved_searches.all()), [second])
        self.assertEqual(list(self.user.harvests.all()), [first_harvest])
        self.assertEqual(list(self.other_user.harvests.all()), [second_harvest])

    def test_deleting_user_cascades_personal_data_and_preserves_catalog(self):
        preference = UserPreference.objects.create(user=self.user)
        preference.species.add(self.species)
        self.search()
        self.harvest()
        UserLicense.objects.create(user=self.user, name="Synthetic license")
        self.search(user=self.other_user)
        owner_id = self.user.pk
        self.user.delete()
        for model in [UserPreference, SavedSearch, Harvest, UserLicense]:
            self.assertFalse(model.objects.filter(user_id=owner_id).exists())
        self.assertEqual(self.other_user.saved_searches.count(), 1)
        self.assertTrue(Species.objects.filter(pk=self.species.pk).exists())
        self.assertTrue(ManagedArea.objects.filter(pk=self.area.pk).exists())

    def test_personal_records_protect_their_catalog_species(self):
        self.harvest()
        with self.assertRaises(ProtectedError):
            self.species.delete()
        self.assertTrue(Species.objects.filter(pk=self.species.pk).exists())

    def test_owner_is_required_when_saving(self):
        with self.assertRaises(ValidationError):
            self.search(user=None)
