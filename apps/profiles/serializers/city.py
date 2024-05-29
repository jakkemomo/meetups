from rest_framework import serializers

from apps.profiles.models import City


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ["city_name", "place_id", "location", "city_south_west_point", "city_north_east_point",]
