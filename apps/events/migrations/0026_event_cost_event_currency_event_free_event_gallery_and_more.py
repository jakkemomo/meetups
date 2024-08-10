# Generated by Django 4.2.3 on 2024-03-30 06:44

import django.contrib.postgres.fields
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("events", "0025_review_rating"),
    ]

    operations = [
        migrations.AddField(
            model_name="event",
            name="cost",
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True),
        ),
        migrations.AddField(
            model_name="event",
            name="currency",
            field=models.CharField(
                choices=[
                    ("BYN", "Belarusian ruble"),
                    ("USD", "United States dollar"),
                    ("EUR", "Euro"),
                    ("RUB", "Russian ruble"),
                    ("PLN", "Polish zloty"),
                    ("UAH", "Ukrainian hryvnia"),
                    ("KZT", "Kazakhstani tenge"),
                ],
                default="BYN",
                max_length=3,
            ),
        ),
        migrations.AddField(
            model_name="event", name="free", field=models.BooleanField(default=True)
        ),
        migrations.AddField(
            model_name="event",
            name="gallery",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(blank=True, default="", max_length=250, null=True),
                default=list,
                size=None,
            ),
        ),
        migrations.AddField(
            model_name="event",
            name="participants_age",
            field=models.PositiveSmallIntegerField(default=18),
        ),
        migrations.AddField(
            model_name="event", name="repeatable", field=models.BooleanField(default=False)
        ),
        migrations.CreateModel(
            name="Schedule",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Created at")),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, null=True, verbose_name="Updated at"),
                ),
                (
                    "day_of_week",
                    models.CharField(
                        choices=[
                            ("sun", "Sunday"),
                            ("mon", "Monday"),
                            ("tue", "Tuesday"),
                            ("wed", "Wednesday"),
                            ("thu", "Thursday"),
                            ("fri", "Friday"),
                            ("sat", "Saturday"),
                        ],
                        max_length=3,
                    ),
                ),
                ("time", models.TimeField()),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_created",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Created by",
                    ),
                ),
                (
                    "event",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="schedules",
                        to="events.event",
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_updated",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Updated by",
                    ),
                ),
            ],
            options={
                "verbose_name": "Schedule",
                "verbose_name_plural": "Schedules",
                "db_table": "events_schedule",
                "ordering": ["event", "day_of_week"],
                "unique_together": {("event", "day_of_week")},
            },
        ),
        migrations.AddField(
            model_name="event",
            name="schedule",
            field=models.ManyToManyField(blank=True, related_name="events", to="events.schedule"),
        ),
    ]
