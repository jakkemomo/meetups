
# Generated by Django 4.2.3 on 2024-03-30 11:21

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    replaces = [('events', '0027_event_end_time_event_start_time_and_more'), ('events', '0028_event_private_url')]

    dependencies = [
        ('events', '0026_event_cost_event_currency_event_free_event_gallery_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='end_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='start_time',
            field=models.TimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='event',
            name='start_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='event',
            name='private_url',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
