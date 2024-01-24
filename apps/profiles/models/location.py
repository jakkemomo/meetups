import pytz

from django.db import models
from django.contrib.gis.db.models import PointField
from django.contrib.gis.geos import Point

from apps.core.models import AbstractBaseModel


class Location(AbstractBaseModel):
    TIMEZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))

    name = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    center = PointField(default=Point(27.561831, 53.902284))
    timezone = models.CharField(max_length=32, choices=TIMEZONES, default='Europe/Minsk')

    class Meta:
        ordering = ["-name"]
        verbose_name = "Location"
        verbose_name_plural = "Locations"
        db_table = 'location'
        unique_together = ('name', 'country',)

    def __str__(self):
        return f"{self.name} ({self.country})"
