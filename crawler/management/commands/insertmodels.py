import time
from typing import Any

import pandas as pd
from django.core.management import BaseCommand
from django.db import transaction

from crawler.models import CarMake, CarModel


class Command(BaseCommand):
    help = "inserts makes and models into database"

    def handle(self, *args: Any, **options: Any):
        start_time = time.time()
        df = pd.read_csv("crawler/management/data/car_data.csv")

        models = []

        with transaction.atomic():
            for _, row in df.iterrows():
                make, created = CarMake.objects.get_or_create(
                    name=row["Make"].capitalize()
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Added "{make.name}" make'))
                model = CarModel(make=make, name=row["Model"])
                models.append(model)

            inserted_models = CarModel.objects.bulk_create(
                models, ignore_conflicts=True
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"Inserted {len(inserted_models)}/{len(models)} models to database in {round(time.time() - start_time, 2)}s"
            )
        )
