from django.contrib.gis.geos import Point
from rest_framework import serializers

from apps.events.models.city import City
from apps.events.serializers import CategoryListSerializer, city as city_serializers, utils
from apps.profiles.models import User
from apps.core.utils import delete_image_if_exists
from apps.profiles.utils import change_followers_if_exists


class ProfileRetrieveSerializer(serializers.ModelSerializer):
    category_favorite = CategoryListSerializer(many=True)
    city_location = city_serializers.CitySerializer()

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "city_location",
            "image_url",
            "is_email_verified",
            "is_private",
            "bio",
            "category_favorite",
            "date_of_birth",
            "gender",
            "type",
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
    bio = serializers.CharField(required=False, max_length=410)
    username = serializers.CharField(required=False, max_length=30)
    first_name = serializers.CharField(required=False, max_length=30)
    last_name = serializers.CharField(required=False, max_length=30)
    email = serializers.EmailField(required=False, max_length=40)
    image_url = serializers.CharField(required=False, max_length=100)
    city_location = city_serializers.CitySerializer()
    date_of_birth = serializers.DateField(required=False)
    category_favorite = CategoryListSerializer(many=True)
    gender = serializers.ChoiceField(choices=User.Gender.choices, required=False)
    type = serializers.ChoiceField(choices=User.Type.choices, required=False)

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
            "city_location",
            "is_private",
            "bio",
            "category_favorite",
            "date_of_birth",
            "gender",
            "type",
        )

    def update(self, instance, validated_data):
        if 'image_url' in validated_data and not validated_data['image_url']:
            delete_image_if_exists(instance)

        is_private = validated_data.get("is_private")
        if is_private is False:
            change_followers_if_exists(instance)

        categories = validated_data.pop("category_favorite", [])
        if validated_data.get("city_location"):
            utils.update_city_if_exist(instance=instance, validated_data=validated_data)
        profile: User = super().update(instance, validated_data)

        if categories:
            profile.category_favorite.set([category.get('id') for category in categories])
        else:
            profile.category_favorite.clear()

        return profile
