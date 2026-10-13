from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Prefetch
from copy import deepcopy

from regulations.models import DeerManagementUnit, HuntingZone, LandType, LicensePermit, ManagedArea, RegulatoryArea, Species
from .serializers import SearchInputSerializer, is_private
from .services import species_data
from .engine import ComplianceEngine
from .models import RegulationDraft, RegulatoryPublication
from .legacy_release import current_approved_legacy_snapshot


def supported_scope(draft):
    publication = draft.current_publications[0] if draft.current_publications else None
    payload = publication.snapshot if publication else draft.payload
    scopes = deepcopy(payload.get("scopes", {}))
    if draft.species.common_name.casefold() == "burmese python" and "regulatory_area" not in scopes:
        fish_id = ManagedArea.objects.filter(name="Fisheating Creek WMA").values_list("pk", flat=True).first()
        if isinstance(scopes.get("managed_area"), list) and fish_id in scopes["managed_area"]:
            scopes["managed_area"].remove(fish_id)
    return {"title": payload.get("title", draft.title), "species": payload["species_id"],
            "land_type": payload["land_type_id"], "scopes": scopes,
            "coverage": payload["coverage"], "reviewed": publication is not None}


def supplemental_scopes(snapshot, existing):
    """Advertise newly supported dated imports without widening curated scopes."""
    if not snapshot:
        return []
    records = snapshot["records"]
    existing_pairs = {(row["species"], row["land_type"]) for row in existing if row["reviewed"]}
    species_names = {row["id"]: row["common_name"] for row in records["species"]}
    periods = {}
    for row in records["seasonperiod"]:
        periods.setdefault(row["season"], []).append(row)
    grouped = {}
    for row in records["huntingseason"]:
        dates = periods.get(row["id"], [])
        if not row.get("is_active", True) or not dates or (row["species"], row["land_type"]) in existing_pairs:
            continue
        scopes = {field: row[field] for field in ("zone", "dmu", "regulatory_area", "managed_area") if row.get(field) is not None}
        key = (row["species"], row["land_type"], tuple(scopes.items()))
        first = min(p["start_date"] for p in dates)
        last = max(p["end_date"] for p in dates)
        if key not in grouped:
            grouped[key] = {"title": species_names[row["species"]] + " — verified project seasons",
                            "species": row["species"], "land_type": row["land_type"], "scopes": scopes,
                            "coverage": {"start_date": first, "end_date": last}, "reviewed": True}
        else:
            coverage = grouped[key]["coverage"]
            coverage["start_date"] = min(coverage["start_date"], first)
            coverage["end_date"] = max(coverage["end_date"], last)
    return list(grouped.values())


class PublicReadOnlyView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    http_method_names = ["get", "head", "options"]


class SpeciesView(PublicReadOnlyView):
    def get(self, request):
        snapshot = current_approved_legacy_snapshot()
        publications = list(RegulatoryPublication.objects.filter(is_current=True))
        return Response([species_data(row, snapshot, publications=[publication for publication in publications
                         if publication.snapshot["species_id"] == row.pk])
                         for row in Species.objects.filter(is_active=True)])


class CatalogView(PublicReadOnlyView):
    def get(self, request):
        scopes = [supported_scope(row) for row in RegulationDraft.objects.select_related("species").prefetch_related(
            Prefetch("publications", queryset=RegulatoryPublication.objects.filter(is_current=True),
                     to_attr="current_publications"))]
        scopes.extend(supplemental_scopes(current_approved_legacy_snapshot(), scopes))
        return Response({
            "land_types": [{"id": row.pk, "name": row.name, "is_private": is_private(row),
                            "requires_managed_area": not is_private(row)} for row in LandType.objects.order_by("pk")],
            "zones": list(HuntingZone.objects.order_by("code").values("id", "code", "name")),
            "dmus": list(DeerManagementUnit.objects.order_by("code").values("id", "code", "zone_id")),
            "regulatory_areas": list(RegulatoryArea.objects.order_by("code").values("id", "code", "name")),
            "managed_areas": list(ManagedArea.objects.filter(is_active=True).order_by("name").values(
                "id", "name", "area_type", "brochure_url", "map_url", "county", "region", "description")),
            "license_permits": list(LicensePermit.objects.filter(is_active=True).order_by("name").values("id", "name")),
            "supported_scopes": scopes,
        })


class RegulationSearchView(PublicReadOnlyView):
    def get(self, request):
        serializer = SearchInputSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        return Response(ComplianceEngine(serializer.validated_data).search())
