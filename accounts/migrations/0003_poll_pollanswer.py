# Generated by Django 4.2.7 on 2023-12-03 15:45

import django.contrib.postgres.fields
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0002_user_phone_number"),
    ]

    operations = [
        migrations.CreateModel(
            name="Poll",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("label", models.CharField(verbose_name="label")),
                (
                    "default_answers",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(blank=True, max_length=256),
                        size=None,
                    ),
                ),
                (
                    "allow_custom_answer",
                    models.BooleanField(default=True, max_length=512),
                ),
                ("use_ratings", models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name="PollAnswer",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("answer", models.CharField()),
                (
                    "poll",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="answer",
                        to="accounts.poll",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="poll",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
