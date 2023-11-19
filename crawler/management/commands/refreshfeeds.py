from typing import Any

from django.core.management.base import BaseCommand

from crawler.utils import update_feeds
from crawler.models import Offer, OfferMetadata


class Command(BaseCommand):
    help = "Refresh all RSS feeds and update database with them"

    def handle(self, *args: Any, **options: Any):
        results = update_feeds(self.stdout)
        for result in results:
            _ = OfferMetadata.objects.bulk_create([offer.metadata for offer in result])
            inserted_offers = Offer.objects.bulk_create(result)
            self.stdout.write(
                f"Success. Saved {len(inserted_offers)}/{len(result)} offers to database.", self.style.SUCCESS
            )
