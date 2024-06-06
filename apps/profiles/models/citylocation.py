from django.contrib.gis.db.models import PointField
from django.contrib.gis.geos import Point
from django.db import models

from apps.core.models import AbstractBaseModel


class CityLocation(AbstractBaseModel):
    place_id = models.CharField(max_length=255, unique=True)
    location = PointField(default=Point(27.561831, 53.902284), unique=True)
    # Yandex : response.GeoObjectCollection.featureMember[0].GeoObject.boundedBy.Envelope.lowerCorner
    # Google : viewport.low.latitude&longitude
    city_south_west_point = PointField(default=Point(27.38909, 53.82427))  # "low" or "lowerCorner"
    # Yandex : response.GeoObjectCollection.featureMember[0].GeoObject.boundedBy.Envelope.upperCorner
    # Google : viewport.high.latitude&longitude
    city_north_east_point = PointField(default=Point(27.76125, 53.97800))

    class Meta:
        verbose_name = "City"
        verbose_name_plural = "Cities"
        db_table = "city_location"
