# Generated by Django 4.2.3 on 2024-04-15 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("events", "0030_alter_event_address_and_more")]

    operations = [
        migrations.AlterField(
            model_name="event",
            name="end_date",
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name="event",
            name="end_time",
            field=models.TimeField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name="event",
            name="start_date",
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name="event",
            name="start_time",
            field=models.TimeField(blank=True, default=None, null=True),
        ),
    ]
