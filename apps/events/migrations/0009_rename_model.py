# Generated by Django 4.2.3 on 2023-07-21 10:30

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [("events", "0008_event_location_event_place_alter_event_start_date")]

    operations = [migrations.RenameModel("Categories", "Category")]
