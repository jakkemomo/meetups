import logging
from rest_framework import serializers
from django.core.files.storage import default_storage

from apps.profiles.models import City

logger = logging.getLogger(__name__)


def delete_image_if_exists(instance):
    image_url = instance.image_url
    if image_url:
        try:
            if default_storage.exists(image_url):
                default_storage.delete(image_url)
        except Exception as exc:
            logger.error(
                f"An error occurred while deleting a file: {image_url}.\n{exc}"
            )
            raise


def validate_city(data: dict[str, str | None]):
    new_city_name, new_city_country = data.get("name"), data.get("country")
    if new_city_name and new_city_country:
        try:
            new_location = City.objects.get(name=new_city_name, country=new_city_country)
            return new_location
        except City.DoesNotExist as _:
            raise serializers.ValidationError(
                {"location": f"There are no city with name: `{new_city_name}` and country: `{new_city_country}`"}
            )
