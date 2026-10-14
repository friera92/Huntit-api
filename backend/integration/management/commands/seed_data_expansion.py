from django.core.management.base import BaseCommand

from integration.data_expansion import seed_data_expansion


class Command(BaseCommand):
    help = "Add FWC-source-checked data expansion as review drafts; never approve or publish it."

    def handle(self, *args, **options):
        result = seed_data_expansion()
        self.stdout.write(self.style.SUCCESS(f"Prepared working drafts: {result}. This command grants no approval; separately approved frozen releases are installed by their own loader."))
