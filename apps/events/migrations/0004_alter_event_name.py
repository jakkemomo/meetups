# Generated by Django 4.2.3 on 2023-07-08 11:35

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("events", "0003_alter_event_end_date_alter_event_start_date")]

    operations = [
        migrations.AlterField(
            model_name="event",
            name="name",
            field=models.CharField(blank=True, max_length=250, null=True, unique=True),
        )
    ]