# Generated by Django 5.0.4 on 2024-04-21 10:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("events", "0031_alter_event_end_date_alter_event_end_time_and_more")]

    operations = [migrations.RemoveField(model_name="event", name="ratings")]
