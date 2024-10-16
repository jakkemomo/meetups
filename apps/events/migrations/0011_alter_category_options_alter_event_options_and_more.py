# Generated by Django 4.2.3 on 2023-07-22 11:29

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("events", "0010_alter_category_name_tag_event_tags"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="category",
            options={"verbose_name": "Category", "verbose_name_plural": "Categories"},
        ),
        migrations.AlterModelOptions(
            name="event",
            options={
                "ordering": ["start_date"],
                "verbose_name": "Event",
                "verbose_name_plural": "Events",
            },
        ),
        migrations.AlterModelOptions(
            name="tag", options={"verbose_name": "Tag", "verbose_name_plural": "Tags"}
        ),
        migrations.AlterField(
            model_name="event",
            name="participants",
            field=models.ManyToManyField(
                blank=True, related_name="event_participants", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.CreateModel(
            name="Rating",
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
                ("rating", models.IntegerField()),
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
                        on_delete=django.db.models.deletion.CASCADE, to="events.event"
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
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
                    ),
                ),
            ],
            options={
                "verbose_name": "Rating",
                "verbose_name_plural": "Ratings",
                "ordering": ["rating"],
            },
        ),
        migrations.AddField(
            model_name="event",
            name="ratings",
            field=models.ManyToManyField(through="events.Rating", to=settings.AUTH_USER_MODEL),
        ),
    ]
