# Generated by Django 4.2.3 on 2024-08-10 06:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("profiles", "0025_remove_user_city_location_user_city"),
        ("cities_light", "0011_alter_city_country_alter_city_region_and_more"),
        ("events", "0039_remove_event_city_north_east_point_and_more"),
    ]

    operations = [
        migrations.RemoveField(model_name="event", name="city_location"),
        migrations.RemoveField(
            model_name="event",
            name="city",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.RemoveField(
            model_name="event",
            name="country",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="event",
            name="city",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="cities_light.city",
            ),
        ),
        migrations.AddField(
            model_name="event",
            name="country",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="cities_light.country",
            ),
        ),
        migrations.DeleteModel(name="City"),
    ]
