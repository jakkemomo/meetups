# Generated by Django 4.2.3 on 2024-04-25 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("events", "0035_event_favorites")]

    operations = [
        migrations.AddField(
            model_name="review",
            name="response",
            field=models.CharField(blank=True, max_length=1000, null=True),
        )
    ]
