from django.contrib.gis.db.models import PointField
from django.contrib.gis.geos import Point
from django.db import models

from apps.core.models import AbstractBaseModel


class CityLocation(AbstractBaseModel):
    """
    Object for storing place data.
    REST Resources of places from Google MAPS Platform Places API. Response JSON-represented:
        {
            "id" : "ChIJ02oeW9PP20YR2XC13VO4YQs"
            "location" : {
                "latitude" : 53.902284
                "longitude" : 27.561831
            }
            "viewport" : {
                "low" : {
                    "latitude" : 53.82427
                    "longitude" : 27.38909
                }
                "high" : {
                    "latitude" : 53.97800
                    "longitude" : 27.76125
                }
            }
        }
    Resources of places from Yandex Maps Geocode API. Response JSON-represented:
        {
          "response": {
            "GeoObjectCollection": {
              "featureMember": [
                {
                  "GeoObject": {
                    "metaDataProperty": {...},
                    "boundedBy": {
                      "Envelope": {
                        "lowerCorner": "27.38909, 53.82427",
                        "upperCorner": "27.76125 53.97800"
                      }
                    },
                    "Point": {
                      "pos": "27.561831 53.902284"
                    }
                  }
                }
              ]
            }
          }
        }
    """
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
