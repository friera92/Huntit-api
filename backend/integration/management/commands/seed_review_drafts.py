from django.core.management.base import BaseCommand
from django.db import transaction

from integration.starter import seed_review_drafts


class Command(BaseCommand):
    help = "Add source-checked 2026/2026-2027 starter drafts without changing or publishing existing data."

    @transaction.atomic
    def handle(self, *args, **options):
        count = seed_review_drafts()
        self.stdout.write(self.style.SUCCESS(
            f"Added {count} review drafts. No regulatory answers were approved or published. Review each in Django admin."
        ))
