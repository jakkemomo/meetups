# Generated by Django 4.2.3 on 2024-06-14 22:32

from django.conf import settings
import django.contrib.gis.db.models.fields
import django.contrib.gis.geos.point
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0038_alter_event_end_date_alter_event_start_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='city_north_east_point',
        ),
        migrations.RemoveField(
            model_name='event',
            name='city_south_west_point',
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, null=True, verbose_name='Updated at')),
                ('place_id', models.CharField(blank=True, default='ChIJ02oeW9PP20YR2XC13VO4YQs', max_length=255, null=True, unique=True)),
                ('location', django.contrib.gis.db.models.fields.PointField(default=django.contrib.gis.geos.point.Point(27.561831, 53.902284), srid=4326, unique=True)),
                ('south_west_point', django.contrib.gis.db.models.fields.PointField(default=django.contrib.gis.geos.point.Point(27.38909, 53.82427), srid=4326)),
                ('north_east_point', django.contrib.gis.db.models.fields.PointField(default=django.contrib.gis.geos.point.Point(27.76125, 53.978), srid=4326)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created', to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_updated', to=settings.AUTH_USER_MODEL, verbose_name='Updated by')),
            ],
            options={
                'verbose_name': 'City',
                'verbose_name_plural': 'Cities',
                'db_table': 'city_location',
            },
        ),
        migrations.AddField(
            model_name='event',
            name='city_location',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='events.city'),
        ),
        migrations.AddConstraint(
            model_name='city',
            constraint=models.UniqueConstraint(fields=('place_id', 'location'), name='unique_location'),
        ),
    ]
