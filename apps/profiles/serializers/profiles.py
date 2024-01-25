from rest_framework import serializers

from apps.profiles.models import User
from apps.core.utils import delete_image_if_exists, validate_location
from apps.profiles.serializers.locations import LocationRetrieveSerializer, LocationUpdateSerializer


class ProfileRetrieveSerializer(serializers.ModelSerializer):
    location = LocationRetrieveSerializer(many=False)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "image_url",
            "is_email_verified",
            "location",
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


class ProfileUpdateLocationSerializer(serializers.ModelSerializer):
    location = LocationUpdateSerializer(many=False)

    class Meta:
        model = User
        fields = ("location", )

    def update(self, instance, validated_data):
        if "location" in validated_data:
            new_location = validate_location(validated_data["location"])
            if instance.location != new_location:
                instance.location = new_location
                instance.save()
        return instance


class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "image_url",
            "is_email_verified",
        )

    def update(self, instance, validated_data):
        if 'image_url' in validated_data and not validated_data['image_url']:
            delete_image_if_exists(instance)

        return super().update(instance, validated_data)
