from django.urls import path

from .views import CatalogView, RegulationSearchView, SpeciesView

urlpatterns = [
    path("species/", SpeciesView.as_view(), name="species"),
    path("catalog/", CatalogView.as_view(), name="catalog"),
    path("regulations/search/", RegulationSearchView.as_view(), name="regulation-search"),
]
