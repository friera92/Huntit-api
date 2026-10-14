"""Seed original working tables and separately install frozen approved releases."""
from django.apps import apps
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import transaction

from integration.legacy_release import LegacyCatalogMissingError


class Command(BaseCommand):
    help = "Seed Leduan's original working catalog and install separately approved frozen releases."

    def load_legacy_if_catalog_ready(self):
        try:
            call_command("load_approved_legacy_release", verbosity=0)
        except LegacyCatalogMissingError as exc:
            self.stdout.write(self.style.WARNING(
                f"Supplemental approved teammate information was skipped: {exc} "
                "Existing catalog entries were preserved. Reconcile the missing catalog identity, "
                "then run load_approved_legacy_release explicitly."))

    @transaction.atomic
    def handle(self, *args, **options):
        models = apps.get_app_config("regulations").get_models()
        if any(model.objects.exists() for model in models):
            self.stdout.write("Existing regulatory data found; starter import skipped.")
            call_command("seed_review_drafts", verbosity=0)
            call_command("load_approved_release", verbosity=0)
            self.load_legacy_if_catalog_ready()
            call_command("seed_data_expansion", verbosity=0)
            call_command("load_approved_expansion", verbosity=0)
            return
        call_command("loaddata", "demo_regulations", verbosity=0)
        self.stdout.write(self.style.SUCCESS(
            "Loaded the original working catalog with its source metadata preserved. "
            "Approved frozen releases are installed separately; no accounts or sessions were imported."
        ))
        call_command("seed_review_drafts", verbosity=0)
        call_command("load_approved_release", verbosity=0)
        self.load_legacy_if_catalog_ready()
        call_command("seed_data_expansion", verbosity=0)
        call_command("load_approved_expansion", verbosity=0)
