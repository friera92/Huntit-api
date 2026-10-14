"""User-owned storage linked to the existing regulatory catalog.

Personal-data endpoints scope every query to the authenticated user. Saved
searches store inputs, never a cached regulatory answer.
"""

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import F, Q
from django.utils import timezone

from regulations.models import DeerManagementUnit, LandType


PRIVATE_LAND_NAME = "Private Land"
MANAGED_LAND_NAMES = {"Wildlife Management Area (WMA)", "Commission-Managed Land"}


class ValidatedModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


class UserPreference(ValidatedModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="preferences")
    species = models.ManyToManyField("regulations.Species", blank=True, related_name="preferred_by")
    managed_areas = models.ManyToManyField("regulations.ManagedArea", blank=True, related_name="preferred_by")
    zones = models.ManyToManyField("regulations.HuntingZone", blank=True, related_name="preferred_by")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Preferences for user {self.user_id}"


class UserLicense(ValidatedModel):
    """A hunter's own statement, never a verification of a government license."""

    class Status(models.TextChoices):
        UNKNOWN = "unknown", "Unknown"
        HELD = "held", "Reported as held"
        NOT_HELD = "not_held", "Reported as not held"
        EXPIRED = "expired", "Reported as expired"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reported_licenses")
    permit = models.ForeignKey("regulations.LicensePermit", on_delete=models.SET_NULL, null=True, blank=True, related_name="user_reports")
    name = models.CharField(max_length=150)
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.UNKNOWN)
    valid_from = models.DateField(null=True, blank=True)
    expires_on = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name", "pk"]
        constraints = [
            models.CheckConstraint(
                condition=Q(status__in=["unknown", "held", "not_held", "expired"]),
                name="personal_license_status_valid",
            ),
            models.CheckConstraint(
                condition=Q(valid_from__isnull=True) | Q(expires_on__isnull=True) | Q(expires_on__gte=F("valid_from")),
                name="personal_license_dates_ordered",
            ),
        ]

    def __str__(self):
        return f"{self.name} (self-reported by user {self.user_id})"


class SavedSearch(ValidatedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="saved_searches")
    title = models.CharField(max_length=120, blank=True)
    species = models.ForeignKey("regulations.Species", on_delete=models.PROTECT, related_name="saved_searches")
    land_type = models.ForeignKey("regulations.LandType", on_delete=models.PROTECT, related_name="saved_searches")
    hunting_date = models.DateField()
    zone = models.ForeignKey("regulations.HuntingZone", on_delete=models.PROTECT, null=True, blank=True, related_name="saved_searches")
    dmu = models.ForeignKey("regulations.DeerManagementUnit", on_delete=models.PROTECT, null=True, blank=True, related_name="saved_searches")
    regulatory_area = models.ForeignKey("regulations.RegulatoryArea", on_delete=models.PROTECT, null=True, blank=True, related_name="saved_searches")
    managed_area = models.ForeignKey("regulations.ManagedArea", on_delete=models.PROTECT, null=True, blank=True, related_name="saved_searches")
    landowner_permission = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at", "-pk"]
        indexes = [models.Index(fields=["user", "hunting_date"], name="personal_search_user_date")]

    def clean(self):
        super().clean()
        errors = {}
        land_type = LandType.objects.filter(pk=self.land_type_id).first() if self.land_type_id else None
        if land_type:
            if land_type.name == PRIVATE_LAND_NAME:
                if self.managed_area_id:
                    errors["managed_area"] = "Choose a public land type when selecting a managed area."
            elif land_type.name in MANAGED_LAND_NAMES:
                if not self.managed_area_id:
                    errors["managed_area"] = "A public-land search must select a managed area."
            else:
                errors["land_type"] = "This land type is not supported for saved searches yet."
        dmu = DeerManagementUnit.objects.filter(pk=self.dmu_id).first() if self.dmu_id else None
        if dmu and dmu.zone_id != self.zone_id:
            errors["dmu"] = "Select the hunting zone that contains this deer management unit."
        if errors:
            raise ValidationError(errors)

    def __str__(self):
        return self.title or f"Search {self.pk or '(new)'} for user {self.user_id}"


class Harvest(ValidatedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="harvests")
    species = models.ForeignKey("regulations.Species", on_delete=models.PROTECT, related_name="user_harvests")
    harvest_date = models.DateField()
    managed_area = models.ForeignKey("regulations.ManagedArea", on_delete=models.PROTECT, null=True, blank=True, related_name="user_harvests")
    location = models.CharField(max_length=200, blank=True, help_text="Location description for private land or an area outside the catalog.")
    quantity = models.PositiveIntegerField(default=1)
    notes = models.TextField(blank=True)
    archived_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-harvest_date", "-pk"]
        indexes = [models.Index(fields=["user", "harvest_date"], name="personal_harvest_user_date")]
        constraints = [
            models.CheckConstraint(condition=Q(quantity__gte=1), name="personal_harvest_quantity_positive"),
            models.CheckConstraint(condition=Q(managed_area__isnull=False) | ~Q(location=""), name="personal_harvest_has_location"),
        ]

    def clean(self):
        super().clean()
        errors = {}
        if self.harvest_date and self.harvest_date > timezone.localdate():
            errors["harvest_date"] = "A completed harvest cannot have a future date."
        if not self.managed_area_id and not self.location.strip():
            errors["location"] = "Select a managed area or describe the hunting location."
        if errors:
            raise ValidationError(errors)

    def __str__(self):
        return f"Harvest {self.pk or '(new)'} by user {self.user_id}"
