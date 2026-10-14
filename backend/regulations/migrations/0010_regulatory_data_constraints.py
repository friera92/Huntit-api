from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("regulations", "0009_managedarea_remove_huntingseason_wma_and_more"),
    ]

    operations = [
        migrations.AddConstraint(
            model_name="seasonperiod",
            constraint=models.CheckConstraint(
                condition=models.Q(end_date__gte=models.F("start_date")),
                name="regulations_period_dates_ordered",
            ),
        ),
        migrations.AddConstraint(
            model_name="baglimitrule",
            constraint=models.CheckConstraint(
                condition=models.Q(is_unlimited=False) | models.Q(limit__isnull=True),
                name="regulations_unlimited_has_no_number",
            ),
        ),
        migrations.AddConstraint(
            model_name="baglimitrule",
            constraint=models.CheckConstraint(
                condition=models.Q(limit_type__in=["GENERAL", "DAILY", "POSSESSION", "SEASON", "ANNUAL"]),
                name="regulations_limit_type_valid",
            ),
        ),
    ]
