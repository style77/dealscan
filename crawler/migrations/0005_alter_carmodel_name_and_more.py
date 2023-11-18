# Generated by Django 4.2.7 on 2023-11-18 01:50

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("crawler", "0004_alter_carmodel_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="carmodel",
            name="name",
            field=models.CharField(max_length=255),
        ),
        migrations.AddConstraint(
            model_name="carmodel",
            constraint=models.UniqueConstraint(
                fields=("make", "name"), name="unique_car_model_for_make"
            ),
        ),
    ]
