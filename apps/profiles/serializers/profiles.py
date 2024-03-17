from rest_framework import serializers

from apps.profiles.models import User
from apps.core.utils import delete_image_if_exists
from apps.profiles.serializers.cities import CityRetrieveSerializer, CityUpdateSerializer


class ProfileRetrieveSerializer(serializers.ModelSerializer):
    city = CityRetrieveSerializer(many=False)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "city",
            "image_url",
            "is_email_verified",
            "is_private",
        )


class ProfileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
        )


class ProfileUpdateSerializer(serializers.ModelSerializer):
    city = CityUpdateSerializer(many=False)

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "image_url",
            "is_email_verified",
            "city",
            "is_private",
        )

    def update(self, instance, validated_data):
        if 'image_url' in validated_data and not validated_data['image_url']:
            delete_image_if_exists(instance)

        return super().update(instance, validated_data)
