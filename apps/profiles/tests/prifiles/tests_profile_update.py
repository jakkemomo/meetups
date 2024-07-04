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
def test_profile_update_by_existing_location_data(api_client, user, user_location_data, user_location_data_2):
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
