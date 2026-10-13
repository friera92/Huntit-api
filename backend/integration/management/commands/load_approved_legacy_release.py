from django.core.management.base import BaseCommand

from integration.legacy_release import LEGACY_RELEASE_ID, install_approved_legacy_release


class Command(BaseCommand):
    help = "Install the exact previously user-approved teammate information; never approve mutable imports."

    def handle(self, *args, **options):
        result = install_approved_legacy_release()
        self.stdout.write(self.style.SUCCESS(
            f"Approved teammate release {LEGACY_RELEASE_ID}: added {result['added']} snapshot; "
            f"already installed={result['already_installed']}."))
