from django.core.management.base import BaseCommand

from integration.approved_release import RELEASE_ID, install_approved_release


class Command(BaseCommand):
    help = "Install the exact hash-pinned, previously human-approved starter release once; never approve current imports."

    def handle(self, *args, **options):
        result = install_approved_release()
        self.stdout.write(self.style.SUCCESS(
            f"Approved release {RELEASE_ID}: added {result['added']} snapshots; "
            f"preserved {result['preserved']} existing histories; already installed={result['already_installed']}."
        ))
