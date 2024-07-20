from django.contrib.gis.geos import Point, Polygon
from django.db import transaction
from rest_framework import serializers

from apps.events.models.city import City


class LocationSerializer(serializers.ModelSerializer):
    latitude = serializers.DecimalField(
        max_value=180, min_value=-180,
        write_only=True, max_digits=18,
        decimal_places=15,
    )
    longitude = serializers.DecimalField(
        max_value=180, min_value=-180,
        write_only=True, max_digits=18,
        decimal_places=15,
    )

    class Meta:
        model = City
        fields = ["latitude", "longitude"]

    def to_representation(self, value):
        return {
            "latitude": value.y,
            "longitude": value.x
        }


class CitySerializer(serializers.ModelSerializer):
    place_id = serializers.CharField(max_length=255, allow_null=True, allow_blank=True)
    location = LocationSerializer(required=True, many=False)
    south_west_point = LocationSerializer(required=True, many=False)
    north_east_point = LocationSerializer(required=True, many=False)

    class Meta:
        model = City
        fields = ["id", "place_id", "location", "south_west_point", "north_east_point"]

    @transaction.atomic
    def create(self, validated_data):
        validated_data["location"] = Point(
            (
                validated_data["location"]["longitude"],
                validated_data["location"]["latitude"]
            )
        )
        validated_data["south_west_point"] = Point(
            (
                validated_data["south_west_point"]["longitude"],
                validated_data["south_west_point"]["latitude"]
            )

        )
        validated_data["north_east_point"] = Point(
            (
                validated_data["north_east_point"]["longitude"],
                validated_data["north_east_point"]["latitude"]
            )
        )
        city_location = City(**validated_data)
        city_location.save()
        return city_location


class CityListSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ["place_id"]
