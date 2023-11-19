from abc import ABC, abstractmethod
from typing import List

import feedparser

from crawler.models import Offer, Source


class FeedFormatter:
    def __init__(self, source: Source):
        try:
            self.crawler = __import__(
                f"crawler.formatters.__{source.name.lower()}", fromlist=["Crawler"]
            ).Crawler(source)
        except ImportError:
            raise ImportError(
                f'Couldn\'t find formatter "{source.name}"'
            )  # it's going to run in command, so raising an exception is safe

    def get_offers(self) -> List[Offer]:
        offers = self.crawler.crawl_offers()
        return offers


class BaseCrawler(ABC):
    def __init__(self, source: Source):
        self.source = source

    def _parse_feed(self):
        d = feedparser.parse(self.source.feed_url)
        return d

    @abstractmethod
    def crawl_offers(self) -> List[Offer]:
        raise NotImplementedError("This method is not implemented for BaseCrawler.")
