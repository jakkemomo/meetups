from rest_framework import serializers

from apps.profiles.models.city import City


class CityUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ["name", "country"]


class CityRetrieveSerializer(serializers.ModelSerializer):
    center = serializers.SerializerMethodField("get_center")

    def get_center(self, obj):
        if not obj.center:
            return None
        return obj.center.coords

    class Meta:
        model = City
        fields = ["id", "name", "country", "center", "timezone"]
