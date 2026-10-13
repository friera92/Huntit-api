from datetime import date

from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.test import TestCase

from .models import BagLimitRule, HuntingSeason, LandType, SeasonPeriod, SeasonType, Source, Species


class RegulatoryConstraintTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.species = Species.objects.create(common_name="Test species")
        cls.land_type = LandType.objects.create(name="Private Land")
        cls.source = Source.objects.create(
            organization="Test fixture", title="Synthetic test source",
            url="https://myfwc.com/hunting/regulations/",
        )
        cls.season_type = SeasonType.objects.create(name="Synthetic test season", code="TEST")
        cls.season = HuntingSeason.objects.create(
            species=cls.species, land_type=cls.land_type, source=cls.source,
            season_type=cls.season_type, season_year="2026-2027",
        )

    def bag_rule(self, **overrides):
        attrs = {
            "species": self.species, "land_type": self.land_type, "source": self.source,
            "season_year": "2026-2027", "limit_type": "DAILY", "limit": 1,
        }
        attrs.update(overrides)
        return BagLimitRule.objects.create(**attrs)

    def test_sqlite_rejects_reversed_periods_even_when_validation_is_bypassed(self):
        with self.assertRaises(IntegrityError), transaction.atomic():
            SeasonPeriod.objects.create(
                season=self.season, start_date=date(2026, 12, 2), end_date=date(2026, 12, 1),
            )
        self.assertEqual(SeasonPeriod.objects.count(), 0)

    def test_model_validation_explains_reversed_periods_before_sqlite_write(self):
        period = SeasonPeriod(season=self.season, start_date=date(2026, 12, 2), end_date=date(2026, 12, 1))
        with self.assertRaises(ValidationError):
            period.full_clean()

    def test_single_day_and_cross_year_periods_remain_valid(self):
        for start, end in [
            (date(2026, 12, 1), date(2026, 12, 1)),
            (date(2026, 12, 31), date(2027, 1, 1)),
        ]:
            SeasonPeriod.objects.create(season=self.season, start_date=start, end_date=end)
        self.assertEqual(SeasonPeriod.objects.count(), 2)

    def test_unlimited_rule_cannot_also_have_numeric_limit(self):
        with self.assertRaises(IntegrityError), transaction.atomic():
            self.bag_rule(is_unlimited=True, limit=1)
        self.assertEqual(BagLimitRule.objects.count(), 0)

    def test_unknown_limit_is_distinct_from_explicitly_unlimited(self):
        unknown = self.bag_rule(is_unlimited=False, limit=None)
        unlimited = self.bag_rule(is_unlimited=True, limit=None)
        self.assertFalse(unknown.is_unlimited)
        self.assertTrue(unlimited.is_unlimited)
        self.assertIsNone(unknown.limit)
        self.assertIsNone(unlimited.limit)

    def test_sqlite_rejects_unknown_limit_types_on_bulk_update(self):
        rule = self.bag_rule()
        with self.assertRaises(IntegrityError), transaction.atomic():
            BagLimitRule.objects.filter(pk=rule.pk).update(limit_type="UNRECOGNIZED")
        rule.refresh_from_db()
        self.assertEqual(rule.limit_type, "DAILY")
