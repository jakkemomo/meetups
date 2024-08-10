from cities_light.contrib.restframework3 import City
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer


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


class CitySerializer(ModelSerializer):
    class Meta:
        model = City
        fields = ["id", "name", "display_name", ]
