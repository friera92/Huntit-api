from django.core.management.base import BaseCommand

from regulations.services.fwc.client import FWCClient
from regulations.services.fwc.parser import FWCSeasonParser
from regulations.services.fwc.normalizer import (
    normalize_periods,
    normalize_season_type,
)
from regulations.services.fwc.importer import FWCImporter


class Command(BaseCommand):
    help = "Imports hunting regulation data from FWC"

    def add_arguments(self, parser):
        parser.add_argument(
            "--season",
            default="2026-2027",
            help="Hunting season year",
        )

        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Parse data without modifying the database",
        )

    def handle(self, *args, **options):
        season_year = options["season"]

        self.stdout.write(
            "Fetching FWC season data..."
        )

        client = FWCClient()
        html = client.get_season_dates_page()

        self.stdout.write(
            self.style.SUCCESS(
                f"Downloaded {len(html):,} characters."
            )
        )

        parser = FWCSeasonParser(html)

        antlerless_data = parser.parse_antlerless_zone(
            zone="A",
            season_year=season_year,
        )

        self.stdout.write(
            "\nParsed Antlerless Deer - Zone A\n"
        )

        for season in antlerless_data["seasons"]:
            self.stdout.write(
                f"\n{season['season_type']}"
            )

        for dmu_data in season["dmu_periods"]:
            periods = normalize_periods(
                dmu_data["date_text"],
                season_year,
            )

        for period in periods:
            self.stdout.write(
                f"  DMU {dmu_data['dmu']}: "
                f"{period['start_date']} -> "
                f"{period['end_date']}"
            )

        # zones = ["A", "B", "C", "D"]

        # importer = FWCImporter(dry_run=options["dry_run"])

        # for zone in zones:
        #     self.stdout.write(
        #         f"\nProcessing Antlered Deer - Zone {zone}..."
        #     )

        #     data = parser.parse_deer_zone(
        #         harvest_category="Antlered",
        #         zone=zone,
        #         season_year=season_year,
        #     )

        #     results = importer.import_deer_zone(data)

        #     for result in results:
        #         season = result["season"]

        #         action = (
        #             "CREATE"
        #             if result["created"]
        #             else "UPDATE"
        #         )

        #         self.stdout.write(
        #             f"[{action}] "
        #             f"{season.species} / "
        #             f"{season.harvest_category} / "
        #             f"Zone {season.zone.code} / "
        #             f"{season.season_type}"
        #         )

        #         for period in result["periods"]:
        #             self.stdout.write(
        #                 f"    {period['start_date']} "
        #                 f"-> {period['end_date']}"
        #             )

        if options["dry_run"]:
            self.stdout.write(
                self.style.WARNING(
                    "\nDRY RUN — changes rolled back."
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    "\nImport completed successfully."
                )
            )