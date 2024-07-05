import pytest
from rest_framework.reverse import reverse

from apps.events.models.city import City
from apps.profiles.models import User
from apps.profiles.tests.utils import get_tokens
from apps.profiles.tests.followers.constants import UPDATE_URL


@pytest.mark.django_db
def test_profile_location_update(api_client, user, user_location_data):
    token = get_tokens(user)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.patch(
        reverse(UPDATE_URL, args=[user.id]),
        data=user_location_data,
        format="json")

    assert response.status_code == 200
    assert response.data['city_location'] is not None
    city_location_id = User.objects.filter(id=user.id).values("city_location").first()
    city_location = City.objects.filter(id=city_location_id["city_location"]).first()
    assert city_location.place_id == user_location_data["city_location"]["place_id"]


@pytest.mark.django_db
def test_profile_update_by_existing_location_data_change_place_id(api_client, user, user_location_data, user_location_data_2):
    token = get_tokens(user)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    api_client.patch(
        reverse(UPDATE_URL, args=[user.id]),
        data=user_location_data,
        format="json")
    city_location_id = User.objects.filter(id=user.id).values("city_location").first()
    city = City.objects.filter(id=city_location_id["city_location"]).first()
    assert city is not None
    response = api_client.patch(
        reverse(UPDATE_URL, args=[user.id]),
        data=user_location_data_2,
        format="json")
    assert response.status_code == 200
    assert response.data['city_location'] is not None
    city_location_id = User.objects.filter(id=user.id).values("city_location").first()
    city_location = City.objects.filter(id=city_location_id["city_location"]).first()
    assert city_location.place_id == user_location_data_2["city_location"]["place_id"]
    assert city_location.location.x == user_location_data_2["city_location"]["location"]["longitude"]
    assert city_location.location.y == user_location_data_2["city_location"]["location"]["latitude"]
    assert city_location.north_east_point.x == user_location_data_2["city_location"]["north_east_point"]["longitude"]
    assert city_location.north_east_point.y == user_location_data_2["city_location"]["north_east_point"]["latitude"]
    assert city_location.south_west_point.x == user_location_data_2["city_location"]["south_west_point"]["longitude"]
    assert city_location.south_west_point.y == user_location_data_2["city_location"]["south_west_point"]["latitude"]
