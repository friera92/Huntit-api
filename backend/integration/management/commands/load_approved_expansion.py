from django.core.management.base import BaseCommand

from integration.approved_expansion import RELEASE_ID, install_approved_expansion


class Command(BaseCommand):
    help = "Install the owner's exact previously source-reviewed expansion; never approve mutable working data."

    def handle(self, *args, **options):
        result = install_approved_expansion()
        self.stdout.write(self.style.SUCCESS(
            f"Approved expansion {RELEASE_ID}: added {result['added']} publications; preserved {result['preserved']} histories; already installed={result['already_installed']}."))
