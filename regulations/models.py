from django.db import models


class Species(models.Model):
    common_name = models.CharField(max_length=100)
    scientific_name = models.CharField(max_length=150, blank=True)

    description = models.TextField(blank=True)
    habitat = models.TextField(blank=True)
    behavior = models.TextField(blank=True)
    hunting_strategy = models.TextField(blank=True)

    image_url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "species"
        ordering = ["common_name"]

    def __str__(self):
        return self.common_name


class HuntingZone(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)

    description = models.TextField(blank=True)
    map_url = models.URLField(blank=True)

    def __str__(self):
        return self.name


class LandType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class RegulatoryArea(models.Model):
    code = models.CharField(
        max_length=50,
        unique=True,
    )

    name = models.CharField(
        max_length=150,
    )

    description = models.TextField(
        blank=True,
    )

    map_url = models.URLField(
        blank=True,
    )

    def __str__(self):
        return self.name


class SeasonType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    code = models.CharField(
        max_length=50,
        unique=True
    )

    description = models.TextField(blank=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "name"]

    def __str__(self):
        return self.name


class Source(models.Model):
    organization = models.CharField(max_length=150)
    title = models.CharField(max_length=255)
    url = models.URLField()

    document_type = models.CharField(max_length=50, blank=True)

    effective_date = models.DateField(null=True, blank=True)
    retrieved_at = models.DateTimeField(null=True, blank=True)
    last_verified_at = models.DateTimeField(null=True, blank=True)

    notes = models.TextField(blank=True)

    def __str__(self):
        return self.title


class ManagedArea(models.Model):
    AREA_TYPE_CHOICES = [
        ("WMA", "Wildlife Management Area"),
        ("WEA", "Wildlife and Environmental Area"),
        ("PSGHA", "Public Small Game Hunting Area"),
        ("SGA", "Small Game Area"),
        ("NWR", "National Wildlife Refuge"),
        ("OTHER", "Other"),
    ]

    name = models.CharField(
        max_length=200,
        unique=True,
    )

    area_type = models.CharField(
        max_length=20,
        choices=AREA_TYPE_CHOICES,
        default="OTHER",
    )

    county = models.CharField(
        max_length=100,
        blank=True,
    )

    region = models.CharField(
        max_length=100,
        blank=True,
    )

    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
    )

    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
    )

    acreage = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
    )

    description = models.TextField(
        blank=True,
    )

    brochure_url = models.URLField(
        blank=True,
    )

    map_url = models.URLField(
        blank=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    def __str__(self):
        return self.name


class LicensePermit(models.Model):
    name = models.CharField(max_length=150)
    permit_type = models.CharField(max_length=100, blank=True)

    description = models.TextField(blank=True)
    requirements = models.TextField(blank=True)

    source = models.ForeignKey(
        Source,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="licenses_permits",
    )

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class LegalMethod(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class DeerManagementUnit(models.Model):
    code = models.CharField(max_length=10, unique=True)

    zone = models.ForeignKey(
        HuntingZone,
        on_delete=models.PROTECT,
        related_name="management_units",
    )

    description = models.TextField(blank=True)

    def __str__(self):
        return self.code

class HarvestCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "harvest categories"

    def __str__(self):
        return self.name

class HuntingSeason(models.Model):
    species = models.ForeignKey(
        Species,
        on_delete=models.CASCADE,
        related_name="hunting_seasons",
    )

    land_type = models.ForeignKey(
        LandType,
        on_delete=models.PROTECT,
        related_name="hunting_seasons",
    )

    regulatory_area = models.ForeignKey(
        RegulatoryArea,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="hunting_seasons",
    )

    zone = models.ForeignKey(
        HuntingZone,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="hunting_seasons",
    )

    managed_area = models.ForeignKey(
        ManagedArea,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="hunting_seasons",
    )

    season_type = models.ForeignKey(
        SeasonType,
        on_delete=models.PROTECT,
        related_name="hunting_seasons",
    )

    season_year = models.CharField(max_length=9)

    daily_bag_limit = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    possession_limit = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    annual_limit = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    permits = models.ManyToManyField(
        LicensePermit,
        blank=True,
        related_name="hunting_seasons",
    )

    legal_methods = models.ManyToManyField(
        LegalMethod,
        blank=True,
        related_name="hunting_seasons",
    )

    source = models.ForeignKey(
        Source,
        on_delete=models.PROTECT,
        related_name="hunting_seasons",
    )

    dmu = models.ForeignKey(
        DeerManagementUnit,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="hunting_seasons",
    )

    harvest_category = models.ForeignKey(
        HarvestCategory,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="hunting_seasons",
    )

    notes = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return (
            f"{self.species} - "
            f"{self.season_type} - "
            f"{self.season_year}"
        )


class SeasonPeriod(models.Model):
    season = models.ForeignKey(
        HuntingSeason,
        on_delete=models.CASCADE,
        related_name="periods",
    )

    start_date = models.DateField()
    end_date = models.DateField()

    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["start_date"]

    def __str__(self):
        return f"{self.start_date} - {self.end_date}"

class BagLimitRule(models.Model):
    LIMIT_TYPE_CHOICES = [
        ("GENERAL", "General"),
        ("DAILY", "Daily"),
        ("POSSESSION", "Possession"),
        ("SEASON", "Season"),
        ("ANNUAL", "Annual"),
    ]

    species = models.ForeignKey(
        Species,
        on_delete=models.CASCADE,
        related_name="bag_limit_rules",
    )

    land_type = models.ForeignKey(
        LandType,
        on_delete=models.PROTECT,
        related_name="bag_limit_rules",
    )

    zone = models.ForeignKey(
        HuntingZone,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="bag_limit_rules",
    )

    regulatory_area = models.ForeignKey(
        RegulatoryArea,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="bag_limit_rules",
    )

    managed_area = models.ForeignKey(
        ManagedArea,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="bag_limit_rules",
    )

    dmu = models.ForeignKey(
        DeerManagementUnit,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="bag_limit_rules",
    )

    season_type = models.ForeignKey(
        SeasonType,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="bag_limit_rules",
    )

    season_year = models.CharField(
        max_length=9
    )

    season_group = models.CharField(
        max_length=50,
        blank=True,
        default="",
    )

    limit_type = models.CharField(
        max_length=20,
        choices=LIMIT_TYPE_CHOICES,
    )

    harvest_category = models.ForeignKey(
        HarvestCategory,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="bag_limit_rules",
    )

    limit = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    is_unlimited = models.BooleanField(
        default=False,
    )

    conditions = models.TextField(
        blank=True
    )

    source = models.ForeignKey(
        Source,
        on_delete=models.PROTECT,
        related_name="bag_limit_rules",
    )

    is_active = models.BooleanField(
        default=True
    )

    def __str__(self):
        category = (
            self.harvest_category.name
            if self.harvest_category
            else "All"
        )
        return (
            f"{self.species} - "
            f"{self.limit_type} - "
            f"{category} - "
            f"{self.limit}"
        )

class RegulationNote(models.Model):
    species = models.ForeignKey(
        Species,
        on_delete=models.CASCADE,
        related_name="regulation_notes",
    )

    land_type = models.ForeignKey(
        LandType,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="regulation_notes",
    )

    season_year = models.CharField(
        max_length=9,
        blank=True,
    )

    title = models.CharField(
        max_length=150,
        blank=True,
    )

    text = models.TextField()

    source = models.ForeignKey(
        Source,
        on_delete=models.PROTECT,
        related_name="regulation_notes",
    )

    is_active = models.BooleanField(
        default=True,
    )

    def __str__(self):
        return (
            f"{self.species} - "
            f"{self.title or 'Regulation Note'}"
        )