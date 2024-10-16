# Generated by Django 4.2.3 on 2023-11-26 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    replaces = [
        ("events", "0017_url_field_instead_of_image_field"),
        ("events", "0018_renamed_image_and_avatar_fields"),
        ("events", "0019_imagedields_to_charfields"),
    ]

    dependencies = [("events", "0016_remove_event_place_event_type_alter_event_address")]

    operations = [
        migrations.RenameField(model_name="event", old_name="image", new_name="image_url"),
        migrations.AlterField(
            model_name="event",
            name="image_url",
            field=models.URLField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name="event",
            name="image_url",
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
