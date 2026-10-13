"""Validate personal records without accepting a caller-selected owner."""
from copy import copy
from collections.abc import Mapping

from django.core.exceptions import ValidationError as ModelValidationError
from rest_framework import serializers

from integration.serializers import SearchInputSerializer
from integration.services import species_data
from regulations.models import (
    DeerManagementUnit, HuntingZone, LandType, LicensePermit, ManagedArea,
    RegulatoryArea, Species,
)

from .models import Harvest, SavedSearch, UserLicense, UserPreference


class OwnerInputMixin:
    def to_internal_value(self, data):
        if isinstance(data, Mapping) and ("user" in data or "user_id" in data):
            raise serializers.ValidationError({"user": "The owner is assigned from your signed-in account."})
        return super().to_internal_value(data)


class OwnedSerializer(OwnerInputMixin, serializers.ModelSerializer):
    pass


class ResetSerializer(OwnerInputMixin, serializers.Serializer):
    preferences = serializers.BooleanField()
    saved_searches = serializers.BooleanField()
    licenses = serializers.BooleanField()
    harvests = serializers.ChoiceField(choices=["archive", "keep"])
    confirmation = serializers.CharField()

    def validate_confirmation(self, value):
        if value != "RESET MY DATA":
            raise serializers.ValidationError("Type RESET MY DATA to confirm this reset.")
        return value


class ValidatedSerializer(OwnedSerializer):
    def validate(self, attrs):
        candidate = copy(self.instance) if self.instance else self.Meta.model()
        candidate.user = self.context["request"].user
        for field, value in attrs.items():
            setattr(candidate, field, value)
        try:
            candidate.full_clean(validate_unique=False)
        except ModelValidationError as exc:
            errors = exc.message_dict if hasattr(exc, "message_dict") else {"non_field_errors": exc.messages}
            if "__all__" in errors:
                errors["non_field_errors"] = errors.pop("__all__")
            raise serializers.ValidationError(errors)
        return attrs


class PreferenceSerializer(OwnedSerializer):
    species = serializers.PrimaryKeyRelatedField(queryset=Species.objects.filter(is_active=True), many=True)
    managed_areas = serializers.PrimaryKeyRelatedField(queryset=ManagedArea.objects.filter(is_active=True), many=True)
    zones = serializers.PrimaryKeyRelatedField(queryset=HuntingZone.objects.all(), many=True)

    class Meta:
        model = UserPreference
        fields = ["species", "managed_areas", "zones"]


class LicenseSerializer(ValidatedSerializer):
    permit = serializers.PrimaryKeyRelatedField(queryset=LicensePermit.objects.filter(is_active=True), allow_null=True, required=False)

    class Meta:
        model = UserLicense
        fields = ["id", "permit", "name", "status", "valid_from", "expires_on", "notes"]
        read_only_fields = ["id"]


class HarvestSerializer(ValidatedSerializer):
    species = serializers.PrimaryKeyRelatedField(queryset=Species.objects.filter(is_active=True))
    managed_area = serializers.PrimaryKeyRelatedField(queryset=ManagedArea.objects.filter(is_active=True), allow_null=True, required=False)
    species_name = serializers.CharField(source="species.common_name", read_only=True)
    species_image = serializers.SerializerMethodField()
    managed_area_name = serializers.CharField(source="managed_area.name", read_only=True, default=None)

    class Meta:
        model = Harvest
        fields = [
            "id", "species", "species_name", "species_image", "harvest_date",
            "managed_area", "managed_area_name", "location", "quantity", "notes",
            "archived_at",
        ]
        read_only_fields = ["id", "archived_at"]

    def get_species_image(self, obj):
        return species_data(obj.species)["image"]


class SavedSearchSerializer(ValidatedSerializer):
    species = serializers.PrimaryKeyRelatedField(queryset=Species.objects.filter(is_active=True))
    land_type = serializers.PrimaryKeyRelatedField(queryset=LandType.objects.all())
    zone = serializers.PrimaryKeyRelatedField(queryset=HuntingZone.objects.all(), allow_null=True, required=False)
    dmu = serializers.PrimaryKeyRelatedField(queryset=DeerManagementUnit.objects.select_related("zone"), allow_null=True, required=False)
    regulatory_area = serializers.PrimaryKeyRelatedField(queryset=RegulatoryArea.objects.all(), allow_null=True, required=False)
    managed_area = serializers.PrimaryKeyRelatedField(queryset=ManagedArea.objects.filter(is_active=True), allow_null=True, required=False)

    class Meta:
        model = SavedSearch
        fields = [
            "id", "title", "species", "land_type", "hunting_date", "zone", "dmu",
            "regulatory_area", "managed_area", "landowner_permission",
        ]
        read_only_fields = ["id"]

    def validate(self, attrs):
        # Apply the same geography and active-catalog validation as a live search,
        # including inferring a DMU's zone when the caller omits it.
        values = {name: attrs.get(name, getattr(self.instance, name, None)) for name in self.Meta.fields if name != "id"}
        search_input = {
            "species": values["species"].pk, "land_type": values["land_type"].pk,
            "date": values["hunting_date"].isoformat(),
            "landowner_permission": values.get("landowner_permission") or False,
        }
        for field in ["zone", "dmu", "regulatory_area", "managed_area"]:
            if values[field] is not None:
                search_input[field] = values[field].pk
        serializer = SearchInputSerializer(data=search_input)
        serializer.is_valid(raise_exception=True)
        if "zone" in serializer.validated_data:
            attrs["zone"] = serializer.validated_data["zone"]
        return super().validate(attrs)
