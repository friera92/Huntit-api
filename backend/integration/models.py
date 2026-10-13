"""A review boundary between imported working records and public answers."""
from copy import deepcopy
from datetime import date
from urllib.parse import urlparse

from django.conf import settings
from django.core.exceptions import PermissionDenied, ValidationError
from django.db import models, transaction
from django.db.models import Max, Q
from django.utils import timezone

from regulations.models import (
    DeerManagementUnit, HuntingZone, LandType, ManagedArea, RegulatoryArea, Species,
)


SCOPE_MODELS = {"zone": HuntingZone, "dmu": DeerManagementUnit,
                "managed_area": ManagedArea, "regulatory_area": RegulatoryArea}
_REVIEW_TOKEN = object()


def validate_payload(payload):
    """Reject incomplete/ambiguous publications before an administrator reviews them."""
    def fail(message):
        raise ValidationError({"payload": message})

    def day(value):
        if not isinstance(value, str):
            fail("Dates must be ISO YYYY-MM-DD values.")
        try:
            parsed = date.fromisoformat(value)
            if parsed.isoformat() != value:
                fail("Dates must be ISO YYYY-MM-DD values.")
            return parsed
        except (TypeError, ValueError):
            fail("Dates must be ISO YYYY-MM-DD values.")

    if not isinstance(payload, dict) or payload.get("version") != 1:
        fail("A version 1 structured regulation payload is required.")
    for key in ["species_id", "land_type_id"]:
        if type(payload.get(key)) is not int:
            fail(f"{key} must be a catalog identifier.")
    coverage = payload.get("coverage", {})
    if not isinstance(coverage, dict):
        fail("Coverage must be an object with start_date and end_date.")
    start, end = day(coverage.get("start_date")), day(coverage.get("end_date"))
    if start > end:
        fail("Coverage end date must follow its start date.")
    sources = payload.get("sources")
    if not isinstance(sources, list) or not sources:
        fail("At least one official source with a checked date is required.")
    urls = set()
    for source in sources:
        if not isinstance(source, dict) or not isinstance(source.get("url"), str):
            fail("Sources must be objects with a URL.")
        try:
            parsed = urlparse(source["url"])
            official = parsed.hostname == "myfwc.com" or (parsed.hostname or "").endswith(".myfwc.com")
        except ValueError:
            fail("Source URL is invalid.")
        if parsed.scheme != "https" or not official or parsed.username or parsed.password:
            fail("Published sources must use an official HTTPS FWC URL.")
        if not all(isinstance(source.get(key), str) and source[key].strip() for key in ["title", "evidence"]):
            fail("Each source needs a title and a short review evidence note.")
        if day(source.get("checked_on")) > timezone.localdate():
            fail("Source checked dates cannot be in the future.")
        urls.add(source["url"])
    required = payload.get("required_inputs", [])
    if not isinstance(required, list) or any(not isinstance(value, str) or value not in SCOPE_MODELS for value in required):
        fail("Required inputs must be recognized location selectors.")
    if type(payload.get("permission_required", False)) is not bool:
        fail("permission_required must be a boolean.")

    def strings_valid(value, description):
        if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
            fail(f"{description} must be a list of strings.")

    strings_valid(payload.get("alerts", []), "Alerts")
    profile = payload.get("species_information")
    if profile is not None:
        if not isinstance(profile, dict):
            fail("Species information must be an object.")
        fields = {"scientific_name", "description", "habitat", "behavior", "hunting_strategy", "source_urls"}
        if set(profile) - fields:
            fail("Unknown species information field.")
        for field, value in profile.items():
            if field != "source_urls" and (not isinstance(value, str) or not value.strip()):
                fail("Species information fields must be nonempty text.")
        strings_valid(profile.get("source_urls"), "Species information source URLs")
        if not profile["source_urls"] or not set(profile["source_urls"]).issubset(urls):
            fail("Species information must cite sources in this snapshot.")

    def scopes_valid(scopes):
        if not isinstance(scopes, dict):
            fail("Scopes must be an object.")
        for field, value in scopes.items():
            if field not in SCOPE_MODELS:
                fail(f"Unknown scope {field}.")
            values = value if isinstance(value, list) else [value]
            if not values or any(type(item) is not int for item in values):
                fail("Scope identifiers must be nonempty integer values.")
            if SCOPE_MODELS[field].objects.filter(pk__in=values).count() != len(set(values)):
                fail(f"Unknown {field} identifier in the payload.")

    scopes_valid(payload.get("scopes", {}))

    def check_geography(scopes, parent):
        combined = {}
        for field in set(scopes) | set(parent):
            value = scopes.get(field, parent.get(field))
            values = set(value if isinstance(value, list) else [value])
            if field in scopes and field in parent:
                other = parent[field] if isinstance(parent[field], list) else [parent[field]]
                if not values.issubset(set(other)):
                    fail("A rule scope cannot extend outside its parent draft scope.")
            combined[field] = values
        if "dmu" in combined and "zone" in combined:
            if DeerManagementUnit.objects.filter(pk__in=combined["dmu"]).exclude(zone_id__in=combined["zone"]).exists():
                fail("Every selected DMU must belong to the scoped hunting zone.")

    check_geography(payload.get("scopes", {}), {})
    rules = payload.get("rules")
    if not isinstance(rules, list) or not rules:
        fail("At least one explicitly dated rule is required.")
    for rule in rules:
        if not isinstance(rule, dict):
            fail("Rules must be objects.")
        if not all(isinstance(rule.get(key), str) and rule[key].strip()
                   for key in ["name", "code", "category", "bag", "licenses", "methods"]):
            fail("Rules need names, categories, bag, license and method guidance; use an explicit unknown if necessary.")
        scopes_valid(rule.get("scopes", {}))
        check_geography(rule.get("scopes", {}), payload.get("scopes", {}))
        strings_valid(rule.get("alerts", []), "Rule alerts")
        if "prohibited" in rule and type(rule["prohibited"]) is not bool:
            fail("A prohibition must be an explicit boolean.")
        periods = rule.get("periods")
        if not isinstance(periods, list) or not periods:
            fail("Each rule needs explicit date bounds.")
        for period in periods:
            if not isinstance(period, dict):
                fail("Periods must be objects with date bounds.")
            first, last = day(period.get("start_date")), day(period.get("end_date"))
            if first > last or first < start or last > end:
                fail("Rule periods must be ordered and contained in review coverage.")
            if "weekdays" in period:
                weekdays = period["weekdays"]
                if (not isinstance(weekdays, list) or not weekdays
                        or any(type(value) is not int or value not in range(1, 8) for value in weekdays)
                        or len(set(weekdays)) != len(weekdays)):
                    fail("Period weekdays must be distinct ISO weekday numbers (Monday 1 through Sunday 7).")
        strings_valid(rule.get("source_urls"), "Rule source URLs")
        if not rule["source_urls"] or not set(rule["source_urls"]).issubset(urls):
            fail("Every rule must cite sources in this snapshot.")
        if "minimum_age" in rule and (type(rule["minimum_age"]) is not int or rule["minimum_age"] < 0):
            fail("Minimum age must be a nonnegative integer.")
        if "maximum_age" in rule and (type(rule["maximum_age"]) is not int or rule["maximum_age"] < 0):
            fail("Maximum age must be a nonnegative integer.")


class RegulationDraft(models.Model):
    key = models.SlugField(max_length=150, unique=True)
    title = models.CharField(max_length=255)
    species = models.ForeignKey(Species, on_delete=models.PROTECT)
    land_type = models.ForeignKey(LandType, on_delete=models.PROTECT)
    payload = models.JSONField(help_text="Structured source-linked working copy. Saving does not publish it.")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        permissions = [("publish_regulationdraft", "Can review and publish regulatory snapshots")]
        ordering = ["title"]

    def __str__(self):
        return self.title

    def clean(self):
        validate_payload(self.payload)
        if self.payload.get("species_id") != self.species_id or self.payload.get("land_type_id") != self.land_type_id:
            raise ValidationError({"payload": "Payload identifiers must match the draft species and land type."})

    @transaction.atomic
    def publish(self, *, reviewer, sources_checked, review_notes):
        if not (reviewer.is_active and reviewer.is_staff and reviewer.has_perm("integration.publish_regulationdraft")):
            raise PermissionDenied("Only an authorized staff reviewer may publish regulations.")
        if sources_checked is not True or not isinstance(review_notes, str) or not review_notes.strip():
            raise ValidationError("Explicit source acknowledgement and review notes are required.")
        current = RegulationDraft.objects.select_for_update().get(pk=self.pk)
        current.full_clean()
        revision = (current.publications.aggregate(last=Max("revision"))["last"] or 0) + 1
        current.publications.filter(is_current=True).update(is_current=False)
        now = timezone.now()
        snapshot = deepcopy(current.payload)
        snapshot["title"] = current.title
        for source in snapshot["sources"]:
            # A checked date is content provenance; verification belongs to this review.
            source["last_verified_at"] = now.isoformat()
        publication = RegulatoryPublication(
            draft=current, revision=revision, snapshot=snapshot, reviewed_by=reviewer,
            reviewed_at=now, review_notes=review_notes.strip(), is_current=True,
        )
        publication.save(_review_token=_REVIEW_TOKEN)
        return publication


class RegulatoryPublication(models.Model):
    draft = models.ForeignKey(RegulationDraft, on_delete=models.PROTECT, related_name="publications")
    revision = models.PositiveIntegerField()
    snapshot = models.JSONField()
    reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    reviewed_at = models.DateTimeField()
    review_notes = models.TextField()
    is_current = models.BooleanField(default=True)

    class Meta:
        ordering = ["draft_id", "-revision"]
        constraints = [
            models.UniqueConstraint(fields=["draft", "revision"], name="integration_unique_review_revision"),
            models.UniqueConstraint(fields=["draft"], condition=Q(is_current=True), name="integration_one_current_review"),
        ]

    def __str__(self):
        return f"{self.draft} — reviewed revision {self.revision}"

    def save(self, *args, _review_token=None, **kwargs):
        if not self._state.adding:
            raise ValidationError("Reviewed snapshots are immutable. Publish a new draft revision instead.")
        if _review_token is not _REVIEW_TOKEN:
            raise PermissionDenied("Create reviewed snapshots through an authorized draft review.")
        return super().save(*args, **kwargs)


class ApprovedReleaseInstallation(models.Model):
    """Receipt for a previously human-approved, hash-pinned distributable release."""
    release_id = models.CharField(max_length=100, unique=True)
    sha256 = models.CharField(max_length=64)
    installed_at = models.DateTimeField(auto_now_add=True)
    publications_added = models.PositiveIntegerField()
    existing_publications_preserved = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.release_id


class ApprovedImportedPublication(models.Model):
    """Frozen teammate records approved together by the project owner.

    These records retain their own internal IDs. Only public search-selector
    identities are mapped to the local catalog by the trusted release loader.
    """
    release_id = models.CharField(max_length=100, unique=True)
    sha256 = models.CharField(max_length=64)
    snapshot = models.JSONField()
    reviewed_at = models.DateTimeField()
    review_notes = models.TextField()
    is_current = models.BooleanField(default=True)

    def __str__(self):
        return self.release_id

    def save(self, *args, _review_token=None, **kwargs):
        if not self._state.adding:
            raise ValidationError("Approved imported snapshots are immutable. Review a new release instead.")
        if _review_token is not _REVIEW_TOKEN:
            raise PermissionDenied("Create approved imported snapshots through the trusted release loader.")
        return super().save(*args, **kwargs)
