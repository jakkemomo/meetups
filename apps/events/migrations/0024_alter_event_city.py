# Generated by Django 4.2.3 on 2024-02-09 09:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("events", "0023_event_city")]

    operations = [
        migrations.AlterField(
            model_name="event",
            name="city",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="profiles.city",
            ),
        )
    ]
