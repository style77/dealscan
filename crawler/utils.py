from datetime import datetime, timedelta
from typing import List

from django.db.models import Q

from crawler.formatters.formatter import FeedFormatter
from crawler.models import Offer, Source


class BaseLogger:
    def write(self, msg, *args, **kwargs):
        print(msg)


def update_feeds(logger=BaseLogger()) -> List[List[Offer]]:
    sources = Source.objects.filter(Q(active=True))
    logger.write(f"Processing queue with size of: {sources.count()} feeds")

    all_results = []
    for source in sources:
        if (
            source.last_polled
            and source.last_polled + timedelta(seconds=source.interval)
            >= datetime.now()
        ):
            logger.write(f'"{source.name}" is on cooldown.')
            continue
        all_results.append(crawl_feed(source))

    return all_results


def crawl_feed(source: Source):
    formatter = FeedFormatter(source)
    offers = formatter.get_offers()
    return offers
