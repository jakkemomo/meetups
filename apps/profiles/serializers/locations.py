from rest_framework import serializers

from apps.profiles.models.location import Location


class UserLocationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['name', 'country']


class UserLocationRetrieveSerializer(serializers.ModelSerializer):
    center = serializers.SerializerMethodField("get_center")

    def get_center(self, obj):
        if not obj.center:
            return None
        return obj.center.coords

    class Meta:
        model = Location
        fields = ['name', 'country', 'center', "timezone"]
