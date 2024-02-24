import pytz

from django.db import models
from django.contrib.gis.db.models import PointField
from django.contrib.gis.geos import Point

from apps.core.models import AbstractBaseModel


class City(AbstractBaseModel):
    TIMEZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))

    name = models.CharField(max_length=255, default="Minsk")
    country = models.CharField(max_length=255, default="BY")
    center = PointField(geography=True, default=Point(27.561831, 53.902284))
    timezone = models.CharField(max_length=32, choices=TIMEZONES, default='Europe/Minsk')

    class Meta:
        ordering = ["-name"]
        verbose_name = "City"
        verbose_name_plural = "Cities"
        db_table = 'city'

    def __str__(self):
        return f"{self.name} ({self.country})"
