# Generated by Django 4.2.3 on 2024-04-22 06:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0033_event_ratings'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='private_url',
            new_name='private_token',
        ),
    ]
