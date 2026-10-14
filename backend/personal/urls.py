from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import ExportView, HarvestViewSet, LicenseViewSet, PreferencesView, ResetView, SavedSearchViewSet

router = SimpleRouter()
router.register("licenses", LicenseViewSet, basename="personal-license")
router.register("harvests", HarvestViewSet, basename="personal-harvest")
router.register("saved-searches", SavedSearchViewSet, basename="personal-saved-search")

urlpatterns = [
    path("preferences/", PreferencesView.as_view(), name="personal-preferences"),
    path("export/", ExportView.as_view(), name="personal-export"),
    path("reset/", ResetView.as_view(), name="personal-reset"),
    path("", include(router.urls)),
]
