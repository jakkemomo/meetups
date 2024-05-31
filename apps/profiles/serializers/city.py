from django.contrib.gis.geos import Point
from django.db import transaction
from rest_framework import serializers

from apps.events.serializers.events import LocationSerializer
from apps.profiles.models import CityLocation


class LocationCitySerializer(LocationSerializer):
    class Meta:
        model = CityLocation
        fields = ["latitude", "longitude"]

    def to_representation(self, value):
        return {
            "latitude": value.y,
            "longitude": value.x
        }


class CityLocationSerializer(serializers.ModelSerializer):
    location = LocationCitySerializer(required=True, many=False)
    city_south_west_point = LocationCitySerializer(required=True, many=False)
    city_north_east_point = LocationCitySerializer(required=True, many=False)

    class Meta:
        model = CityLocation
        fields = ["id", "location", "city_south_west_point", "city_north_east_point", ]

    @transaction.atomic
    def create(self, validated_data):
        validated_data["location"] = Point(
            (
                validated_data["location"]["longitude"],
                validated_data["location"]["latitude"]
            )
        )
        validated_data["city_south_west_point"] = Point(
            (
                validated_data["city_south_west_point"]["longitude"],
                validated_data["city_south_west_point"]["latitude"]
            )

        )
        validated_data["city_north_east_point"] = Point(
            (
                validated_data["city_north_east_point"]["longitude"],
                validated_data["city_north_east_point"]["latitude"]
            )
        )
        city_location = CityLocation(**validated_data)
        city_location.save()
        return city_location
