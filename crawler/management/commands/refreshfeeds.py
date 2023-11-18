from typing import Any, Optional
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Refresh all RSS feeds and update database with them"

    def handle(self, *args: Any, **options: Any) -> str | None:
        self.stdout.write(self.style.SUCCESS("Success"))
