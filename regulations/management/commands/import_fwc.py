from django.core.management.base import (
    BaseCommand,
    CommandError,
)
from django.db import transaction

from regulations.services.fwc.client import (
    FWCClient,
)
from regulations.services.fwc.importer import (
    FWCImporter,
)

from regulations.services.fwc.parsers.deer import (
    FWCDeerParser,
)
from regulations.services.fwc.parsers.turkey import (
    FWCTurkeyParser,
)
from regulations.services.fwc.parsers.wild_hog import (
    FWCWildHogParser,
)
from regulations.services.fwc.parsers.python import (
    FWCBurmesePythonParser,
)


IMPORTABLE_SOURCES = (
    "season_dates",
    "wild_hog",
    "burmese_python_removal",
)

ZONES = (
    "A",
    "B",
    "C",
    "D",
)

TURKEY_SPRING_AREAS = (
    "NORTH_SR70",
    "SOUTH_SR70",
)

TURKEY_SEASON_GROUPS = (
    "FALL",
    "SPRING",
)


class Command(BaseCommand):
    help = "Imports hunting regulation data from FWC"

    def add_arguments(self, parser):
        parser.add_argument(
            "--source",
            choices=(
                *IMPORTABLE_SOURCES,
                "all",
            ),
            default=None,
            help=(
                "FWC source to import. "
                "If omitted, all supported sources "
                "are imported."
            ),
        )

        parser.add_argument(
            "--season",
            default="2026-2027",
            help="Hunting season year",
        )

        parser.add_argument(
            "--dry-run",
            action="store_true",
            help=(
                "Parse and import data without "
                "persisting database changes"
            ),
        )

    def handle(self, *args, **options):
        season_year = options["season"]
        requested_source = options["source"]
        dry_run = options["dry_run"]

        source_keys = self._resolve_sources(
            requested_source
        )

        client = FWCClient()

        # Fetch everything BEFORE opening the
        # database transaction.
        fetch_results = {}

        for source_key in source_keys:
            fetch_results[source_key] = (
                self._fetch_source(
                    client,
                    source_key,
                )
            )

        importer = FWCImporter(
            dry_run=dry_run
        )

        try:
            with transaction.atomic():

                for source_key in source_keys:
                    self._import_source(
                        source_key=source_key,
                        fetch_result=(
                            fetch_results[source_key]
                        ),
                        importer=importer,
                        season_year=season_year,
                    )

                # Guarantees Source and all other
                # changes are rolled back too.
                if dry_run:
                    transaction.set_rollback(
                        True
                    )

        except Exception as exc:
            raise CommandError(
                f"FWC import failed: {exc}"
            ) from exc

        if dry_run:
            self.stdout.write(
                self.style.WARNING(
                    "\nDRY RUN — all changes "
                    "rolled back."
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    "\nImport completed successfully."
                )
            )

    def _resolve_sources(
        self,
        requested_source,
    ):
        if (
            requested_source is None
            or requested_source == "all"
        ):
            return IMPORTABLE_SOURCES

        return (
            requested_source,
        )

    def _fetch_source(
        self,
        client,
        source_key,
    ):
        self.stdout.write(
            f"\nFetching FWC source: "
            f"{source_key}..."
        )

        fetch_result = client.fetch(
            source_key
        )

        self.stdout.write(
            f"Source: "
            f"{fetch_result.source.title}"
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Downloaded "
                f"{len(fetch_result.html):,} "
                f"characters."
            )
        )

        return fetch_result

    def _import_source(self, *, source_key, fetch_result, importer, season_year):
        source = importer.sync_source(
            fetch_result
        )

        html = fetch_result.html

        handlers = {
            "season_dates": (
                self._import_season_dates
            ),
            "wild_hog": (
                self._import_wild_hog
            ),
            "burmese_python_removal": (
                self._import_burmese_python_source
            ),
        }

        try:
            handler = handlers[source_key]
        except KeyError:
            raise CommandError(
                f"Unsupported import source: "
                f"{source_key}"
            )

        handler(
            html=html,
            importer=importer,
            source=source,
            season_year=season_year,
        )

    def _import_season_dates(self,*, html, importer, source, season_year):
        deer_parser = FWCDeerParser(html)       
        turkey_parser = FWCTurkeyParser(html)
        
        self._import_deer(
            parser=deer_parser,
            importer=importer,
            source=source,
            season_year=season_year,
        )
        
        self._import_turkey(
            parser=turkey_parser,
            importer=importer,
            source=source,
            season_year=season_year,
        )

    def _import_deer(self,*, parser, importer, source, season_year):
        self.stdout.write(
            "\n=== White Tailed Deer ==="
        )

        self.stdout.write(
            "\nImporting Antlered Deer..."
        )

        for zone in ZONES:
            data = parser.parse_deer_zone(
                harvest_category="ANTLERED",
                zone=zone,
                season_year=season_year,
            )

            results = (
                importer.import_deer_zone(
                    data,
                    source=source,
                )
            )

            self._print_season_results(
                results
            )

        self.stdout.write(
            "\nImporting Antlerless Deer..."
        )

        for zone in ZONES:
            data = (
                parser.parse_antlerless_zone(
                    zone=zone,
                    season_year=season_year,
                )
            )

            results = (
                importer.import_antlerless_zone(
                    data,
                    source=source,
                )
            )

            self._print_season_results(
                results
            )

        self.stdout.write(
            "\nImporting Deer Bag Limits..."
        )

        bag_data = parser.parse_bag_limits()

        bag_results = (
            importer.import_deer_bag_limits(
                bag_data,
                source=source,
                season_year=season_year,
            )
        )

        self._print_bag_results(
            bag_results["rules"]
        )

        note_result = bag_results["note"]

        if note_result:
            self._print_note_result(
                note_result["note"],
                note_result["created"],
            )
    def _import_turkey(self,*, parser, importer, source, season_year):
        self.stdout.write(
            "\n=== Wild Turkey ==="
        )

        self.stdout.write(
            "\nImporting Fall Turkey..."
        )

        for zone in ZONES:
            data = parser.parse_fall_zone(
                zone,
                season_year,
            )

            results = (
                importer.import_turkey_seasons(
                    data,
                    source=source,
                )
            )

            self._print_season_results(
                results
            )

        self.stdout.write(
            "\nImporting Spring Turkey..."
        )

        for area_code in (
            TURKEY_SPRING_AREAS
        ):
            data = (
                parser.parse_spring_area(
                    area_code,
                    season_year,
                )
            )

            results = (
                importer.import_turkey_seasons(
                    data,
                    source=source,
                )
            )

            self._print_season_results(
                results
            )

        self.stdout.write(
            "\nImporting Turkey Bag Limits..."
        )

        for season_group in (
            TURKEY_SEASON_GROUPS
        ):
            data = parser.parse_bag_limits(
                season_group
            )

            results = (
                importer.import_turkey_bag_limits(
                    data,
                    source=source,
                    season_year=season_year,
                )
            )

            self._print_bag_results(
                results
            )

    def _import_wild_hog(self,*, html, importer, source, season_year):
        self.stdout.write(
            "\n=== Wild Hog ==="
        )

        parser = FWCWildHogParser(
            html
        )

        private_data = (
            parser.parse_private_land_rules(
                season_year
            )
        )

        result = (
            importer.import_wild_hog_private_land(
                private_data,
                source=source,
            )
        )

        self._print_object_result(
            result["season"]["object"],
            result["season"]["created"],
        )

        self._print_object_result(
            result["bag_limit"]["object"],
            result["bag_limit"]["created"],
        )

        self._print_note_result(
            result["note"]["object"],
            result["note"]["created"],
        )

        public_data = (
            parser.parse_public_land_note(
                season_year
            )
        )

        public_result = (
            importer.import_wild_hog_public_note(
                public_data,
                source=source,
            )
        )

        self._print_note_result(
            public_result["note"],
            public_result["created"],
        )

    def _import_burmese_python_source(self,*, html, importer, source, season_year):
        parser = FWCBurmesePythonParser(
            html
        )

        self._import_burmese_python(
            parser=parser,
            importer=importer,
            source=source,
            season_year=season_year,
        )


    def _import_burmese_python(self, *, parser, importer, source, season_year):
            self.stdout.write(
                "\nImporting Burmese Python"
            )
    
            private_data = (
                parser.parse_private_land_rules(
                    season_year
                )
            )
    
            private_result = (
                importer.import_burmese_python_private_land(
                    private_data,
                    source=source,
                )
            )
    
            season_result = private_result["season"]
    
            action = (
                "CREATE"
                if season_result["created"]
                else "UPDATE"
            )
    
            self.stdout.write(
                f"[{action}] "
                f"Burmese Python / "
                f"Private Land / YEAR_ROUND"
            )
    
            bag_result = private_result["bag_limit"]
    
            action = (
                "CREATE"
                if bag_result["created"]
                else "UPDATE"
            )
    
            self.stdout.write(
                f"[{action}] "
                f"Burmese Python / "
                f"Private Land / GENERAL / No Limit"
            )
    
            note_result = private_result["note"]
    
            action = (
                "CREATE"
                if note_result["created"]
                else "UPDATE"
            )
    
            self.stdout.write(
                f"[{action}] "
                f"{note_result['object'].title}"
            )
    
            # -----------------------------------
            # Commission-managed lands
            # -----------------------------------
    
            managed_data = (
                parser.parse_managed_land_rules(
                    season_year
                )
            )
    
            managed_result = (
                importer.import_burmese_python_managed_land(
                    managed_data,
                    source=source,
                )
            )
    
            self.stdout.write(
                "\nCommission-Managed Lands"
            )
    
            for result in managed_result["seasons"]:
                season = result["season"]
    
                action = (
                    "CREATE"
                    if result["created"]
                    else "UPDATE"
                )
    
                self.stdout.write(
                    f"[{action}] "
                    f"Burmese Python / "
                    f"{season.managed_area.name} / "
                    f"YEAR_ROUND"
                )
    
            bag_result = managed_result["bag_limit"]
    
            action = (
                "CREATE"
                if bag_result["created"]
                else "UPDATE"
            )
    
            self.stdout.write(
                f"[{action}] "
                f"Burmese Python / "
                f"Commission-Managed Land / "
                f"GENERAL / No Limit"
            )
    
            note_result = managed_result["note"]
    
            action = (
                "CREATE"
                if note_result["created"]
                else "UPDATE"
            )
    
            self.stdout.write(
                f"[{action}] "
                f"{note_result['object'].title}"
            )


    def _action(self, created):
        return (
            "CREATE"
            if created
            else "UPDATE"
        )

    def _print_season_results(self, results):
        for result in results:
            season = result["season"]

            scope = []

            if season.zone:
                scope.append(
                    f"Zone {season.zone.code}"
                )

            if season.dmu:
                scope.append(
                    f"DMU {season.dmu.code}"
                )

            if season.regulatory_area:
                scope.append(
                    season.regulatory_area.name
                )

            if season.managed_area:
                scope.append(
                    season.managed_area.name
                )

            scope_text = (
                " / ".join(scope)
                if scope
                else season.land_type.name
            )

            action = self._action(
                result["created"]
            )

            self.stdout.write(
                f"[{action}] "
                f"{season.species} / "
                f"{scope_text} / "
                f"{season.season_type}"
            )

            for period in result.get(
                "periods",
                [],
            ):
                self.stdout.write(
                    f"    "
                    f"{period['start_date']} "
                    f"-> "
                    f"{period['end_date']}"
                )

    def _print_bag_results(self, results):
        for result in results:
            rule = result["rule"]

            action = self._action(
                result["created"]
            )

            value = (
                "No Limit"
                if rule.is_unlimited
                else rule.limit
            )

            scope = (
                rule.season_group
                if rule.season_group
                else "General"
            )

            if rule.dmu:
                scope = (
                    f"DMU {rule.dmu.code}"
                )

            self.stdout.write(
                f"[{action}] "
                f"{rule.species} / "
                f"{scope} / "
                f"{rule.limit_type} / "
                f"{value}"
            )

    def _print_note_result(self, note, created):
        action = self._action(
            created
        )

        self.stdout.write(
            f"[{action}] "
            f"Regulation Note / "
            f"{note.title}"
        )

    def _print_object_result(self, obj, created):
        action = self._action(
            created
        )

        self.stdout.write(
            f"[{action}] {obj}"
        )