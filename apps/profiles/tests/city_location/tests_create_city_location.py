import pytest
from django.contrib.gis.geos import Point
from rest_framework.reverse import reverse
from rest_framework_simplejwt.tokens import RefreshToken

from apps.profiles.models import CityLocation
from apps.profiles.tests.city_location.constants import CITY_LIST_URL
from apps.profiles.tests.utils import get_tokens
from rest_framework.test import APIClient


@pytest.fixture()
def authenticated_user(api_client, user) -> APIClient:
    refresh = RefreshToken.for_user(user)
    token = refresh.access_token
    return api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)


@pytest.mark.django_db
def test_create_city_valid(api_client,
                           user, city_location_data):
    token = get_tokens(user)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.post(reverse(CITY_LIST_URL), data=city_location_data, format="json")
    assert response.status_code == 201
    assert CityLocation.objects.all().first
    assert CityLocation.objects.filter(
        location=Point(city_location_data["location"]["longitude"], city_location_data["location"]["latitude"]))


@pytest.mark.django_db
def test_create_city_not_unic_point(api_client,
                                    user, city_location_data):
    token = get_tokens(user)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    api_client.post(reverse(CITY_LIST_URL), data=city_location_data, format="json")
    response = api_client.post(reverse(CITY_LIST_URL), data=city_location_data, format="json")
    assert response.status_code == 403
