# Generated by Django 4.2.7 on 2023-11-19 02:15

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("crawler", "0004_alter_offermetadata_features"),
    ]

    operations = [
        migrations.AlterField(
            model_name="offer",
            name="id",
            field=models.SlugField(max_length=512, primary_key=True, serialize=False),
        ),
    ]