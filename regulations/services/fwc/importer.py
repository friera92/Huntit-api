from django.db import transaction

from regulations.models import (
    Species,
    HarvestCategory,
    HuntingZone,
    DeerManagementUnit,
    LandType,
    SeasonType,
    Source,
    HuntingSeason,
    SeasonPeriod,
    BagLimitRule,
    RegulationNote,
    RegulatoryArea,
    LegalMethod
)

from .normalizer import (
    normalize_periods,
    normalize_season_type,
)


class FWCImporter:
    def __init__(self, dry_run=False):
        self.dry_run = dry_run

    @transaction.atomic
    def import_deer_zone(self, data, source):
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

        # source = Source.objects.get(
        #     organization__icontains="Florida Fish and Wildlife"
        # )

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

    @transaction.atomic
    def import_antlerless_zone(self, data, source):
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

        # source = Source.objects.get(
        #     organization__icontains="Florida Fish and Wildlife"
        # )

        results = []

        for season_data in data["seasons"]:
            season_code = normalize_season_type(
                season_data["season_type"]
            )

            season_type = SeasonType.objects.get(
                code=season_code
            )

            for rule in season_data["rules"]:
                dmu = None

                if rule["dmu"]:
                    dmu = DeerManagementUnit.objects.get(
                        code=rule["dmu"],
                        zone=zone,
                    )

                periods = normalize_periods(
                    rule["date_text"],
                    data["season_year"],
                )

                hunting_season, created = (
                    HuntingSeason.objects.get_or_create(
                        species=species,
                        harvest_category=harvest_category,
                        land_type=land_type,
                        zone=zone,
                        dmu=dmu,
                        wma=None,
                        season_type=season_type,
                        season_year=data["season_year"],
                        defaults={
                            "source": source,
                            "is_active": True,
                        },
                    )
                )

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

                results.append({
                    "season": hunting_season,
                    "created": created,
                    "periods": periods,
                })

        if self.dry_run:
            transaction.set_rollback(True)

        return results

    @transaction.atomic
    def import_deer_bag_limits(self, data, source_title, season_year):
        species = Species.objects.get(
            common_name=data["species"]
        )

        land_type = LandType.objects.get(
            name="Private Land"
        )

        source = Source.objects.get(            
            title=source_title
        )

        note_result = None

        if data.get("note"):
            note, note_created = self.import_regulation_note(
                species=species,
                land_type=land_type,
                season_year=season_year,
                title="Bag Limit Exceptions",
                text=data["note"],
                source=source,
            )

            note_result = {
                "note": note,
                "created": note_created,
            }

        results = []

        for rule in data["rules"]:
            harvest_category = None
            dmu = None
            zone = None

            if rule["harvest_category"]:
                harvest_category = (
                    HarvestCategory.objects.get(
                        name=rule["harvest_category"]
                    )
                )

            if rule["dmu"]:
                dmu = DeerManagementUnit.objects.get(
                    code=rule["dmu"]
                )

                zone = dmu.zone

            bag_rule, created = (
                BagLimitRule.objects.update_or_create(
                    species=species,
                    land_type=land_type,
                    zone=zone,
                    dmu=dmu,
                    season_type=None,
                    season_year=season_year,
                    limit_type=rule["limit_type"],
                    harvest_category=harvest_category,
                    defaults={
                        "limit": rule["limit"],
                        "is_unlimited": rule[
                            "is_unlimited"
                        ],
                        "conditions": rule[
                            "conditions"
                        ],
                        "source": source,
                        "is_active": True,
                    },
                )
            )

            results.append({
                "rule": bag_rule,
                "created": created,
            })

        if self.dry_run:
            transaction.set_rollback(True)

        return {
            "rules": results,
            "note": note_result
        }

    def import_regulation_note(self, *, species, land_type, season_year, title, text, source):
        if not text:
            return None, False

        note, created = RegulationNote.objects.update_or_create(
            species=species,
            land_type=land_type,
            season_year=season_year,
            title=title,
            defaults={
                "text": text,
                "source": source,
                "is_active": True,
            },
        )

        return note, created

    @transaction.atomic
    def import_turkey_seasons(self, data, source_title):
        species = Species.objects.get(
            common_name=data["species"]
        )

        harvest_category = HarvestCategory.objects.get(
            name=data["harvest_category"]
        )

        land_type = LandType.objects.get(
            name="Private Land"
        )

        source = Source.objects.get(            
            title=source_title
        )

        zone = None

        if data["zone"]:
            zone = HuntingZone.objects.get(
                code=data["zone"]
            )

        regulatory_area = (
            self._sync_regulatory_area(data.get("regulatory_area"))
        )

        results = []

        for season_data in data["seasons"]:
            season_code = normalize_season_type(
                season_data["season_type"]
            )

            season_type = SeasonType.objects.get(
                code=season_code
            )

            periods = normalize_periods(
                season_data["date_text"],
                data["season_year"],
                initial_year=data["initial_year"],
            )

            hunting_season, created = (
                HuntingSeason.objects.get_or_create(
                    species=species,
                    harvest_category=harvest_category,
                    land_type=land_type,
                    zone=zone,
                    regulatory_area=regulatory_area,
                    dmu=None,
                    wma=None,
                    season_type=season_type,
                    season_year=data["season_year"],
                    defaults={
                        "source": source,
                        "is_active": True,
                    },
                )
            )

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

            results.append({
                "season": hunting_season,
                "created": created,
                "periods": periods,
            })

        if self.dry_run:
            transaction.set_rollback(True)

        return results

    @transaction.atomic
    def import_turkey_bag_limits(self, data, source_title, season_year):
        species = Species.objects.get(
            common_name=data["species"]
        )

        land_type = LandType.objects.get(
            name="Private Land"
        )

        source = Source.objects.get(            
            title=source_title
        )

        results = []

        for rule in data["rules"]:
            harvest_category = (
                HarvestCategory.objects.get(
                    name=rule["harvest_category"]
                )
            )

            bag_rule, created = (
                BagLimitRule.objects.update_or_create(
                    species=species,
                    land_type=land_type,
                    zone=None,
                    regulatory_area=None,
                    dmu=None,
                    season_type=None,
                    season_year=season_year,
                    season_group=rule["season_group"],
                    limit_type=rule["limit_type"],
                    harvest_category=harvest_category,
                    defaults={
                        "limit": rule["limit"],
                        "is_unlimited": rule[
                            "is_unlimited"
                        ],
                        "conditions": rule[
                            "conditions"
                        ],
                        "source": source,
                        "is_active": True,
                    },
                )
            )

            results.append({
                "rule": bag_rule,
                "created": created,
            })

        if self.dry_run:
            transaction.set_rollback(True)

        return results

    @transaction.atomic
    def import_wild_hog_private_land(self, data, source):
        species = Species.objects.get(
            common_name=data["species"]
        )

        land_type = LandType.objects.get(
            name=data["land_type"]
        )

        harvest_category = None

        if data["harvest_category"]:
            harvest_category, _ = (
                HarvestCategory.objects.get_or_create(
                    name=data["harvest_category"]
                )
            )

        season_code = normalize_season_type(
            data["season_type"]
        )

        season_type = SeasonType.objects.get(
            code=season_code
        )

        hunting_season, season_created = (
            HuntingSeason.objects.get_or_create(
                species=species,
                harvest_category=harvest_category,
                land_type=land_type,
                zone=None,
                regulatory_area=None,
                dmu=None,
                wma=None,
                season_type=season_type,
                season_year=data["season_year"],
                defaults={
                    "source": source,
                    "is_active": True,
                },
            )
        )

        changed = False

        if hunting_season.source_id != source.id:
            hunting_season.source = source
            changed = True

        if not hunting_season.is_active:
            hunting_season.is_active = True
            changed = True

        if changed:
            hunting_season.save()

        legal_methods = self._sync_legal_methods(
            data["legal_methods"]
        )

        hunting_season.legal_methods.set(
            legal_methods
        )

        bag_data = data["bag_limit"]

        bag_rule, bag_created = (
            BagLimitRule.objects.update_or_create(
                species=species,
                land_type=land_type,
                zone=None,
                regulatory_area=None,
                dmu=None,
                season_type=season_type,
                season_year=data["season_year"],
                season_group="",
                limit_type=bag_data["limit_type"],
                harvest_category=harvest_category,
                defaults={
                    "limit": bag_data["limit"],
                    "is_unlimited": bag_data[
                        "is_unlimited"
                    ],
                    "conditions": bag_data[
                        "conditions"
                    ],
                    "source": source,
                    "is_active": True,
                },
            )
        )

        note_data = data["note"]

        note, note_created = (
            self.import_regulation_note(
                species=species,
                land_type=land_type,
                season_year=data["season_year"],
                title=note_data["title"],
                text=note_data["text"],
                source=source,
            )
        )

        if self.dry_run:
            transaction.set_rollback(True)

        return {
            "season": {
                "object": hunting_season,
                "created": season_created,
            },
            "bag_limit": {
                "object": bag_rule,
                "created": bag_created,
            },
            "note": {
                "object": note,
                "created": note_created,
            },
        }

    def import_wild_hog_public_note(self, data, source):
        species = Species.objects.get(
            common_name=data["species"]
        )

        note, created = (
            self.import_regulation_note(
                species=species,
                land_type=None,
                season_year=data["season_year"],
                title=data["title"],
                text=data["text"],
                source=source,
            )
        )

        return {
            "note": note,
            "created": created,
        }

    def sync_source(self, fetch_result):
            source_info = fetch_result.source
    
            source, created = Source.objects.update_or_create(
                url=source_info.url,
                defaults={
                    "organization": source_info.organization,
                    "title": source_info.title,
                    "document_type": source_info.document_type,
                    "retrieved_at": fetch_result.retrieved_at,
                },
            )
    
            return source

    def _sync_regulatory_area(self, area_data):
        if not area_data:
            return None

        regulatory_area, created = (
            RegulatoryArea.objects.update_or_create(
                code=area_data["code"],
                defaults={
                    "name": area_data["name"],
                },
            )
        )

        return regulatory_area

    def _sync_legal_methods(self, method_names):
        methods = []

        for name in method_names:
            method, _ = (
                LegalMethod.objects.get_or_create(
                    name=name
                )
            )

            methods.append(method)

        return methods