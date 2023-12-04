from typing import Any

from django.core.management.base import BaseCommand
from django.db import IntegrityError, transaction

from crawler.utils import update_feeds


class Command(BaseCommand):
    help = "Refresh all RSS feeds and update database with them"

    def handle(self, *args: Any, **options: Any):
        results = update_feeds(self.stdout)
        successful_offer_inserts = 0
        successful_metadata_inserts = 0
        success = True

        for result in results:
            self.stdout.write(f"Processing {len(result)} offers.", self.style.NOTICE)
            for offer in result:
                with transaction.atomic():
                    try:
                        offer.metadata.save()
                        successful_metadata_inserts += 1

                        offer.save()
                        successful_offer_inserts += 1
                    except IntegrityError as e:
                        self.stdout.write(
                            f"Skipped insertion due to IntegrityError: {e}",
                            self.style.WARNING,
                        )
                        success = False

                        # Rollback the transaction if any error occurs
                        transaction.set_rollback(True)

        if success:
            total_offers = sum(len(result) for result in results)
            self.stdout.write(
                f"Success. Saved {successful_offer_inserts}/{total_offers} offers and {successful_metadata_inserts}/{total_offers} metadata entries to database.",
                self.style.SUCCESS,
            )
        else:
            self.stdout.write(
                "Failed to insert. Rolled back transaction.",
                self.style.ERROR,
            )
