import logging
from rest_framework import serializers
from django.core.files.storage import default_storage

from apps.profiles.models import Location

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


def validate_location(data: dict[str, str | None]):
    new_loc_name, new_loc_country = data.get("name"), data.get("country")
    if new_loc_name and new_loc_country:
        try:
            new_location = Location.objects.get(name=new_loc_name, country=new_loc_country)
            return new_location
        except Location.DoesNotExist as exc:
            logger.error(
                f"An error occurred while updating current user location: .\n{exc}"
            )
            raise serializers.ValidationError(
                {"location": f"There are no location with name: `{new_loc_name}` and country: `{new_loc_country}`"}
            )
