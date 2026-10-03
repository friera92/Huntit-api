from django.db import transaction

from regulations.models import (
    Species,
    HarvestCategory,
    HuntingZone,
    LandType,
    SeasonType,
    Source,
    HuntingSeason,
    SeasonPeriod,
)

from .normalizer import (
    normalize_periods,
    normalize_season_type,
)


class FWCImporter:
    def __init__(self, dry_run=False):
        self.dry_run = dry_run

    @transaction.atomic
    def import_deer_zone(self, data):
        species = Species.objects.get(
            common_name=data["species"]
        )

        harvest_category = HarvestCategory.objects.get(
            name=data["harvest_category"]
        )

        zone = HuntingZone.objects.get(
            code=data["zone"]
        )

        land_type = LandType.objects.get(
            name="Private Land"
        )

        source = Source.objects.get(
            organization__icontains="Florida Fish and Wildlife"
        )

        results = []

        for season_data in data["seasons"]:
            result = self._import_season(
                season_data=season_data,
                species=species,
                harvest_category=harvest_category,
                zone=zone,
                land_type=land_type,
                source=source,
                season_year=data["season_year"],
            )

            results.append(result)

        if self.dry_run:
            transaction.set_rollback(True)

        return results

    def _import_season(
        self,
        *,
        season_data,
        species,
        harvest_category,
        zone,
        land_type,
        source,
        season_year,
    ):
        season_code = normalize_season_type(
            season_data["season_type"]
        )

        season_type = SeasonType.objects.get(
            code=season_code
        )

        periods = normalize_periods(
            season_data["date_text"],
            season_year,
        )

        hunting_season, created = (
            HuntingSeason.objects.get_or_create(
                species=species,
                harvest_category=harvest_category,
                land_type=land_type,
                zone=zone,
                dmu=None,
                wma=None,
                season_type=season_type,
                season_year=season_year,
                defaults={
                    "source": source,
                    "is_active": True,
                },
            )
        )

        # Keep mutable information synchronized.
        changed = False

        if hunting_season.source_id != source.id:
            hunting_season.source = source
            changed = True

        if not hunting_season.is_active:
            hunting_season.is_active = True
            changed = True

        if changed:
            hunting_season.save()

        self._sync_periods(
            hunting_season,
            periods,
        )

        return {
            "season": hunting_season,
            "created": created,
            "periods": periods,
        }

    def _sync_periods(
        self,
        hunting_season,
        periods,
    ):
        expected_periods = {
            (
                period["start_date"],
                period["end_date"],
            )
            for period in periods
        }

        existing_periods = {
            (
                period.start_date,
                period.end_date,
            ): period
            for period in hunting_season.periods.all()
        }

        # Create missing periods.
        for start_date, end_date in expected_periods:
            if (start_date, end_date) not in existing_periods:
                SeasonPeriod.objects.create(
                    season=hunting_season,
                    start_date=start_date,
                    end_date=end_date,
                )

        # Remove periods no longer present in FWC data.
        for dates, period in existing_periods.items():
            if dates not in expected_periods:
                period.delete()