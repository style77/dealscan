# Generated by Django 4.2.7 on 2023-12-04 18:24

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("crawler", "0008_alter_offer_image_url"),
    ]

    operations = [
        migrations.AlterField(
            model_name="offermetadata",
            name="registration_number",
            field=models.CharField(
                blank=True, max_length=24, null=True, verbose_name="registration number"
            ),
        ),
    ]