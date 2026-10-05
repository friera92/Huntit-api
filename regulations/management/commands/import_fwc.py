from django.core.management.base import BaseCommand
from django.test import html

from regulations.models import Source
from regulations.services.fwc.client import FWCClient
from regulations.services.fwc.parsers.deer import (
    FWCDeerParser,
)

from regulations.services.fwc.parsers.turkey import (
    FWCTurkeyParser,
)

from regulations.services.fwc.parsers.wild_hog import (
    FWCWildHogParser,
)

from regulations.services.fwc.normalizer import (
    normalize_periods,
    normalize_season_type,
)

from regulations.services.fwc.importer import FWCImporter

from regulations.services.fwc.sources import (
    get_source_keys,
)

from django.db import transaction


class Command(BaseCommand):
    help = "Imports hunting regulation data from FWC"

    def add_arguments(self, parser):
        parser.add_argument(
            "--source",
            choices=get_source_keys(),
            default="season_dates",
            help="FWC source to import",
        )
        
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
        source_key = options["source"]

        client = FWCClient()

        self.stdout.write(
            f"Fetching FWC source: {source_key}..."
        )

        fetch_result = client.fetch(
            source_key
        )

        html = fetch_result.html

        self.stdout.write(
            f"Source: {fetch_result.source.title}"
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Downloaded {len(html):,} characters."
            )
        )

        if source_key == "season_dates":
            parser = FWCDeerParser(html)
        elif source_key == "wild_hog":
            parser = FWCWildHogParser(html)
        else:
            parser = FWCTurkeyParser(html)

        importer = FWCImporter(dry_run=options["dry_run"])

        source = importer.sync_source(fetch_result)

        print(source)

        self.stdout.write(
            "\nWILD HOG — PRIVATE LAND RAW DATA\n"
        )

        private_data = (
            parser.parse_private_land_rules(
                season_year
            )
        )

        public_data = (
            parser.parse_public_land_note(
                season_year
            )
        )

        private_result = (
            importer.import_wild_hog_private_land(
                private_data,
                source=source,
            )
        )

        public_result = (
            importer.import_wild_hog_public_note(
                public_data,
                source=source,
            )
        )

        season_result = private_result["season"]

        season_action = (
            "CREATE"
            if season_result["created"]
            else "UPDATE"
        )

        self.stdout.write(
            f"[{season_action}] "
            f"Wild Hog / Private Land / YEAR_ROUND"
        )

        bag_result = private_result["bag_limit"]

        bag_action = (
            "CREATE"
            if bag_result["created"]
            else "UPDATE"
        )

        self.stdout.write(
            f"[{bag_action}] "
            f"Wild Hog / GENERAL / No Limit"
        )

        note_result = private_result["note"]

        note_action = (
            "CREATE"
            if note_result["created"]
            else "UPDATE"
        )

        self.stdout.write(
            f"[{note_action}] "
            f"{note_result['object'].title}"
        )

        public_action = (
            "CREATE"
            if public_result["created"]
            else "UPDATE"
        )

        self.stdout.write(
            f"[{public_action}] "
            f"{public_result['note'].title}"
        )

        return

        self.stdout.write(
            "\nImporting Fall Turkey Seasons"
        )

        for zone in ["A", "B", "C", "D"]:
            data = parser.parse_fall_zone(
                zone,
                season_year,
            )

            results = importer.import_turkey_seasons(
                data,
                source_title=fetch_result.source.title,
            )

            for result in results:
                season = result["season"]

                action = (
                    "CREATE"
                    if result["created"]
                    else "UPDATE"
                )

                self.stdout.write(
                    f"[{action}] "
                    f"{season.species} / "
                    f"Zone {season.zone.code} / "
                    f"{season.season_type}"
                )

                for period in result["periods"]:
                    self.stdout.write(
                        f"    {period['start_date']} "
                        f"-> {period['end_date']}"
                    )

        self.stdout.write(
            "\nImporting Spring Turkey Seasons"
        )

        for area_code in [
            "NORTH_SR70",
            "SOUTH_SR70",
        ]:
            data = parser.parse_spring_area(
                area_code,
                season_year,
            )

            results = importer.import_turkey_seasons(
                data,
                source_title=fetch_result.source.title,
            )

            for result in results:
                season = result["season"]

                action = (
                    "CREATE"
                    if result["created"]
                    else "UPDATE"
                )

                self.stdout.write(
                    f"[{action}] "
                    f"{season.species} / "
                    f"{season.regulatory_area.name} / "
                    f"{season.season_type}"
                )

                for period in result["periods"]:
                    self.stdout.write(
                        f"    {period['start_date']} "
                        f"-> {period['end_date']}"
                    )

        self.stdout.write(
            "\nImporting Turkey Bag Limits"
        )

        for season_group in [
            "FALL",
            "SPRING",
        ]:
            data = parser.parse_bag_limits(
                season_group
            )

            results = importer.import_turkey_bag_limits(
                data,
                source_title=fetch_result.source.title,
                season_year=season_year,
            )

            for result in results:
                rule = result["rule"]

                action = (
                    "CREATE"
                    if result["created"]
                    else "UPDATE"
                )

                self.stdout.write(
                    f"[{action}] "
                    f"{rule.season_group} / "
                    f"{rule.limit_type} / "
                    f"{rule.limit}"
                )

        # if source_key == "season_dates":
        #     parser = FWCDeerParser(html)

        # elif source_key == "burmese_python_removal":
        #     raise NotImplementedError(
        #         "Burmese Python importer "
        #         "has not been implemented yet."
        #     )

        # else:
        #     raise NotImplementedError(
        #         f"Importer not implemented for "
        #         f"source: {source_key}"
        #     )

        # bag_limit_data = parser.parse_bag_limits()

       

        # bag_results = importer.import_deer_bag_limits(
        #     bag_limit_data,
        #     source_title=fetch_result.source.title,
        #     season_year=season_year,
        # )

        # self.stdout.write(
        #     "\nImporting Deer Bag Limits"
        # )

        # for result in bag_results["rules"]:
        #     rule = result["rule"]

        #     action = (
        #         "CREATE"
        #         if result["created"]
        #         else "UPDATE"
        #     )

        #     category = (
        #         rule.harvest_category.name
        #         if rule.harvest_category
        #         else "All Deer"
        #     )

        #     if rule.dmu:
        #         scope = f"DMU {rule.dmu.code}"
        #     else:
        #         scope = "General"

        #     value = (
        #         "No Limit"
        #         if rule.is_unlimited
        #         else str(rule.limit)
        #     )

        #     self.stdout.write(
        #         f"[{action}] "
        #         f"{scope} / "
        #         f"{rule.limit_type} / "
        #         f"{category} / "
        #         f"{value}"
        #     )

        # note_result = bag_results["note"]

        # if note_result:
        #     action = (
        #         "CREATE"
        #         if note_result["created"]
        #         else "UPDATE"
        #     )

        #     self.stdout.write(
        #         f"[{action}] Regulation Note / "
        #         f"{note_result['note'].title}"
        #     )

        # importer = FWCImporter(
        #             dry_run=options["dry_run"]
        #         )

        # with transaction.atomic():
        #     source = importer.sync_source(
        #         fetch_result
        #     )

        #     zones = ["A", "B", "C", "D"]

        #     for zone in zones:
        #         self.stdout.write(
        #             f"\nProcessing Antlerless Deer - Zone {zone}..."
        #         )

        #         data = parser.parse_antlerless_zone(
        #             zone=zone,
        #             season_year=season_year,
        #         )

        #         results = importer.import_antlerless_zone(
        #             data,
        #             source = source
        #         )

        #         for result in results:
        #             season = result["season"]

        #             action = (
        #                 "CREATE"
        #                 if result["created"]
        #                 else "UPDATE"
        #             )

        #             if season.dmu:
        #                 scope = (
        #                     f"Zone {season.zone.code} / "
        #                     f"DMU {season.dmu.code}"
        #                 )
        #             else:
        #                 scope = f"Zone {season.zone.code}"

        #             self.stdout.write(
        #                 f"[{action}] "
        #                 f"{season.species} / "
        #                 f"{season.harvest_category} / "
        #                 f"{scope} / "
        #                 f"{season.season_type}"
        #             )

        #             for period in result["periods"]:
        #                 self.stdout.write(
        #                     f"    {period['start_date']} "
        #                     f"-> {period['end_date']}"
        #                 )
            
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