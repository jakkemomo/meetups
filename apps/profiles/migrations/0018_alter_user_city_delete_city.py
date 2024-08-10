# Generated by Django 4.2.3 on 2024-03-30 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0029_event_any_participant_number_and_more"),
        ("profiles", "0015_user_is_private_squashed_0017_alter_user_is_private"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="city",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.DeleteModel(name="City"),
    ]
