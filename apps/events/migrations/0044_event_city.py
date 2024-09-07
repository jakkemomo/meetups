# Generated by Django 4.2.3 on 2024-09-07 08:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [("core", "0001_initial"), ("events", "0043_remove_event_city")]

    operations = [
        migrations.AddField(
            model_name="event",
            name="city",
            field=models.ForeignKey(
                blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to="core.city"
            ),
        )
    ]
