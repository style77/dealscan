from typing import Any, Optional
from django.core.management import BaseCommand


class InsertModels(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> str | None:
        i = 0
        self.stdout.write(self.style.SUCCESS + f"Inserted {i} models to database")
