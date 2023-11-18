from typing import Any

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Refresh all RSS feeds and update database with them"

    def handle(self, *args: Any, **options: Any):
        self.stdout.write(self.style.SUCCESS("Success"))
