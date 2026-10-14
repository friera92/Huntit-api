from io import StringIO

from django.contrib.auth import get_user_model
from django.contrib.sessions.models import Session
from django.core.management import call_command
from django.test import TestCase

from regulations.models import Source, Species
from .models import ApprovedImportedPublication, RegulationDraft, RegulatoryPublication


class LocalBootstrapTests(TestCase):
    def test_starter_data_installs_approved_releases_without_accounts_or_mutating_original_sources(self):
        call_command("seed_local_data", stdout=StringIO())
        self.assertEqual(Species.objects.count(), 4)
        self.assertEqual(Source.objects.count(), 4)
        self.assertFalse(Source.objects.filter(last_verified_at__isnull=False).exists())
        self.assertEqual(get_user_model().objects.count(), 0)
        self.assertEqual(Session.objects.count(), 0)
        self.assertEqual(RegulationDraft.objects.count(), 58)
        self.assertEqual(RegulatoryPublication.objects.count(), 76)
        self.assertEqual(RegulatoryPublication.objects.filter(is_current=True).count(), 58)
        self.assertEqual(ApprovedImportedPublication.objects.count(), 1)
        self.assertFalse(RegulatoryPublication.objects.filter(reviewed_by__isnull=False).exists())

    def test_existing_catalog_is_never_overwritten(self):
        species = Species.objects.create(common_name="Team-maintained catalog entry")
        # A partial catalog cannot safely map all of the supplemental release.
        # Skip that release with a clear message rather than guess identities.
        output = StringIO()
        call_command("seed_local_data", stdout=output)
        species.refresh_from_db()
        self.assertEqual(species.common_name, "Team-maintained catalog entry")
        self.assertTrue(Species.objects.filter(pk=species.pk).exists())
        self.assertEqual(Species.objects.filter(common_name="Team-maintained catalog entry").count(), 1)
        self.assertFalse(ApprovedImportedPublication.objects.exists())
        self.assertIn("Supplemental approved teammate information was skipped", output.getvalue())

    def test_second_setup_preserves_changes_to_starter_data(self):
        call_command("seed_local_data", stdout=StringIO())
        species = Species.objects.first()
        species.description = "A team member edited this record."
        species.save()
        call_command("seed_local_data", stdout=StringIO())
        species.refresh_from_db()
        self.assertEqual(species.description, "A team member edited this record.")
        self.assertEqual(Species.objects.count(), 4)
