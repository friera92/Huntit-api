from django.contrib import admin

from .models import (
    BagLimitRule,
    RegulationNote,
    RegulatoryArea,
    Species,
    HuntingZone,
    LandType,
    SeasonType,
    Source,
    WildlifeManagementArea,
    LicensePermit,
    LegalMethod,
    HuntingSeason,
    SeasonPeriod,
    DeerManagementUnit,
    HarvestCategory
)


@admin.register(Species)
class SpeciesAdmin(admin.ModelAdmin):
    list_display = (
        "common_name",
        "scientific_name",
        "is_active",
    )

    search_fields = (
        "common_name",
        "scientific_name",
    )

    list_filter = (
        "is_active",
    )


@admin.register(HuntingZone)
class HuntingZoneAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "name",
    )


@admin.register(WildlifeManagementArea)
class WildlifeManagementAreaAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "county",
        "region",
        "is_active",
    )

    search_fields = (
        "name",
        "county",
    )

    list_filter = (
        "region",
        "is_active",
    )


class SeasonPeriodInline(admin.TabularInline):
    model = SeasonPeriod
    extra = 1


@admin.register(HuntingSeason)
class HuntingSeasonAdmin(admin.ModelAdmin):
    list_display = (
        "species",
        "season_type",
        "season_year",
        "land_type",
        "zone",
        "wma",
        "is_active",
    )

    list_filter = (
        "season_year",
        "season_type",
        "land_type",
        "zone",
        "is_active",
    )

    search_fields = (
        "species__common_name",
        "wma__name",
    )

    inlines = [
        SeasonPeriodInline,
    ]

@admin.register(DeerManagementUnit)
class DeerManagementUnitAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "zone",
    )

    list_filter = (
        "zone",
    )

    search_fields = (
        "code",
    )


admin.site.register(LandType)
admin.site.register(SeasonType)
admin.site.register(Source)
admin.site.register(LicensePermit)
admin.site.register(LegalMethod)
admin.site.register(HarvestCategory)
admin.site.register(BagLimitRule)
admin.site.register(RegulationNote)
admin.site.register(RegulatoryArea)