"""Authenticated, owner-scoped personal data; no personal inputs are logged."""
from django.db import transaction
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.views.decorators.debug import sensitive_post_parameters
from rest_framework import generics, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.viewsets import ModelViewSet

from integration.serializers import SearchInputSerializer
from integration.engine import ComplianceEngine

from .models import Harvest, SavedSearch, UserLicense, UserPreference
from .serializers import HarvestSerializer, LicenseSerializer, PreferenceSerializer, ResetSerializer, SavedSearchSerializer


@method_decorator(sensitive_post_parameters(), name="dispatch")
class PreferencesView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PreferenceSerializer

    def get(self, request):
        preference = UserPreference.objects.filter(user=request.user).first()
        if preference is None:
            return Response({"species": [], "managed_areas": [], "zones": []})
        return Response(self.get_serializer(preference).data)

    @transaction.atomic
    def put(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # The unique owner relation and get_or_create's atomic insertion handle
        # a competing first save without creating duplicate preference records.
        preference, _ = UserPreference.objects.get_or_create(user=request.user)
        serializer.instance = preference
        serializer.save(user=request.user)
        return Response(serializer.data)


@method_decorator(sensitive_post_parameters(), name="dispatch")
class OwnedViewSet(ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None
    http_method_names = ["get", "post", "patch", "delete", "head", "options"]

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class LicenseViewSet(OwnedViewSet):
    queryset = UserLicense.objects.select_related("permit")
    serializer_class = LicenseSerializer


class HarvestViewSet(OwnedViewSet):
    queryset = Harvest.objects.select_related("species", "managed_area")
    serializer_class = HarvestSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action == "list":
            archived = self.request.query_params.get("archived", "false").casefold()
            if archived not in {"true", "false"}:
                raise ValidationError({"archived": "Use true or false for the archive filter."})
            queryset = queryset.filter(archived_at__isnull=archived != "true")
        return queryset

    @action(detail=True, methods=["post"])
    def archive(self, request, pk=None):
        harvest = self.get_object()
        if harvest.archived_at is None:
            harvest.archived_at = timezone.now()
            harvest.save(update_fields=["archived_at", "updated_at"])
        return Response(self.get_serializer(harvest).data)

    @action(detail=True, methods=["post"])
    def restore(self, request, pk=None):
        harvest = self.get_object()
        if harvest.archived_at is not None:
            harvest.archived_at = None
            harvest.save(update_fields=["archived_at", "updated_at"])
        return Response(self.get_serializer(harvest).data)


class SavedSearchViewSet(OwnedViewSet):
    queryset = SavedSearch.objects.select_related("species", "land_type", "zone", "dmu", "regulatory_area", "managed_area")
    serializer_class = SavedSearchSerializer

    @action(detail=True, methods=["get"])
    def run(self, request, pk=None):
        saved = self.get_object()
        data = {
            "species": saved.species_id, "land_type": saved.land_type_id,
            "date": saved.hunting_date.isoformat(), "landowner_permission": saved.landowner_permission,
        }
        for field in ["zone", "dmu", "regulatory_area", "managed_area"]:
            value = getattr(saved, field + "_id")
            if value is not None:
                data[field] = value
        serializer = SearchInputSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        return Response(ComplianceEngine(serializer.validated_data).search(), status=status.HTTP_200_OK)


@method_decorator(sensitive_post_parameters(), name="dispatch")
class ExportView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get", "head", "options"]

    def get(self, request):
        preference = UserPreference.objects.filter(user=request.user).first()
        context = {"request": request}
        payload = {
            "version": 1, "exported_at": timezone.now().isoformat(),
            "preferences": PreferenceSerializer(preference, context=context).data if preference else {"species": [], "managed_areas": [], "zones": []},
            "licenses": LicenseSerializer(UserLicense.objects.filter(user=request.user), many=True, context=context).data,
            "saved_searches": SavedSearchSerializer(SavedSearch.objects.filter(user=request.user), many=True, context=context).data,
            "harvests": HarvestSerializer(Harvest.objects.filter(user=request.user).select_related("species", "managed_area"), many=True, context=context).data,
        }
        response = Response(payload)
        response["Content-Disposition"] = 'attachment; filename="HuntIt-personal-data.json"'
        return response


@method_decorator(sensitive_post_parameters(), name="dispatch")
class ResetView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ResetSerializer
    http_method_names = ["post", "options"]

    @transaction.atomic
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        choices = serializer.validated_data
        counts = {"preferences": 0, "saved_searches": 0, "licenses": 0, "harvests_archived": 0}
        for field, model in [("preferences", UserPreference), ("saved_searches", SavedSearch), ("licenses", UserLicense)]:
            if choices[field]:
                queryset = model.objects.filter(user=request.user)
                counts[field] = queryset.count()
                queryset.delete()
        if choices["harvests"] == "archive":
            now = timezone.now()
            counts["harvests_archived"] = Harvest.objects.filter(user=request.user, archived_at__isnull=True).update(archived_at=now, updated_at=now)
        return Response(counts)
