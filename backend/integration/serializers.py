from rest_framework import serializers

from regulations.models import (
    DeerManagementUnit, HuntingZone, LandType, ManagedArea, RegulatoryArea, Species,
)


def is_private(land_type):
    return "private" in land_type.name.casefold()


class SearchInputSerializer(serializers.Serializer):
    species = serializers.PrimaryKeyRelatedField(queryset=Species.objects.filter(is_active=True))
    land_type = serializers.PrimaryKeyRelatedField(queryset=LandType.objects.all())
    date = serializers.DateField(input_formats=["%Y-%m-%d"])
    zone = serializers.PrimaryKeyRelatedField(queryset=HuntingZone.objects.all(), required=False)
    dmu = serializers.PrimaryKeyRelatedField(queryset=DeerManagementUnit.objects.select_related("zone"), required=False)
    regulatory_area = serializers.PrimaryKeyRelatedField(queryset=RegulatoryArea.objects.all(), required=False)
    managed_area = serializers.PrimaryKeyRelatedField(queryset=ManagedArea.objects.filter(is_active=True), required=False)
    landowner_permission = serializers.BooleanField(default=False)

    def validate(self, attrs):
        zone, dmu = attrs.get("zone"), attrs.get("dmu")
        if dmu:
            if zone and zone.pk != dmu.zone_id:
                raise serializers.ValidationError({"dmu": "The selected DMU does not belong to this zone."})
            attrs["zone"] = dmu.zone
        if not is_private(attrs["land_type"]) and not attrs.get("managed_area"):
            raise serializers.ValidationError({"managed_area": "Select a managed hunting area for public land."})
        if is_private(attrs["land_type"]) and attrs.get("managed_area"):
            raise serializers.ValidationError({"managed_area": "Managed public areas cannot be selected for private land."})
        return attrs
