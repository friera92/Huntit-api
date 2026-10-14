from django.contrib import admin

from .models import Harvest, SavedSearch, UserLicense, UserPreference


@admin.register(UserPreference)
class UserPreferenceAdmin(admin.ModelAdmin):
    list_display = ["user", "updated_at"]
    filter_horizontal = ["species", "managed_areas", "zones"]


@admin.register(UserLicense)
class UserLicenseAdmin(admin.ModelAdmin):
    list_display = ["user", "name", "status", "expires_on"]
    list_filter = ["status"]
    search_fields = ["user__username", "name"]


@admin.register(SavedSearch)
class SavedSearchAdmin(admin.ModelAdmin):
    list_display = ["user", "title", "species", "land_type", "hunting_date", "managed_area"]
    list_filter = ["land_type"]
    search_fields = ["user__username", "title"]


@admin.register(Harvest)
class HarvestAdmin(admin.ModelAdmin):
    list_display = ["user", "species", "harvest_date", "managed_area", "location", "quantity"]
    search_fields = ["user__username", "location"]
