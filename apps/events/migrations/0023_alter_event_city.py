# Generated by Django 4.2.3 on 2024-02-09 09:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0012_city_user_city'),
        ('events', '0022_event_city'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='profiles.city'),
        ),
    ]
