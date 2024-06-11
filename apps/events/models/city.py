from django.contrib.gis.db.models import PointField
from django.contrib.gis.geos import Point
from django.db import models
from rest_framework.utils import json

from apps.core.models import AbstractBaseModel


class City(AbstractBaseModel):
    place_id = models.CharField(max_length=255, unique=True, default="ChIJ02oeW9PP20YR2XC13VO4YQs", null=True,
                                blank=True)
    location = PointField(default=Point(27.561831, 53.902284), unique=True)
    # Yandex : response.GeoObjectCollection.featureMember[0].GeoObject.boundedBy.Envelope.lowerCorner
    # Google : viewport.low.latitude&longitude
    south_west_point = PointField(default=Point(27.38909, 53.82427))  # "low" or "lowerCorner"
    # Yandex : response.GeoObjectCollection.featureMember[0].GeoObject.boundedBy.Envelope.upperCorner
    # Google : viewport.high.latitude&longitude
    north_east_point = PointField(default=Point(27.76125, 53.97800))

    class Meta:
        constraints = [models.UniqueConstraint(fields=['place_id', 'location'], name='unique_location')]
        verbose_name = "City"
        verbose_name_plural = "Cities"
        db_table = "city_location"
