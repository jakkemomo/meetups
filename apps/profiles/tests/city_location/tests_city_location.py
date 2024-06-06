import pytest
from django.contrib.gis.geos import Point
from rest_framework.reverse import reverse

from apps.profiles.models import CityLocation
from apps.profiles.tests.city_location.constants import CITY_LIST_URL, CITY_GET_URL
from apps.profiles.tests.utils import get_tokens
from rest_framework.test import APIClient


@pytest.fixture()
def authenticated_user(api_client, user) -> APIClient:
    token = get_tokens(user)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    return api_client


@pytest.mark.django_db
def test_create_city_valid_user(city_location_minsk_google_data, authenticated_user):
    response = authenticated_user.post(reverse(CITY_LIST_URL), data=city_location_minsk_google_data, format="json")
    assert response.status_code == 201
    assert CityLocation.objects.all().first
    assert CityLocation.objects.filter(
        location=Point(city_location_minsk_google_data["location"]["longitude"],
                       city_location_minsk_google_data["location"]["latitude"]),
        place_id=city_location_minsk_google_data["place_id"])


@pytest.mark.django_db
@pytest.mark.usefixtures('city_location_default')
def test_create_default_city(city_location_default_data):
    assert CityLocation.objects.all().first
    assert CityLocation.objects.filter(location=Point(city_location_default_data["location"]["longitude"],
                                                      city_location_default_data["location"]["latitude"]),
                                       place_id=city_location_default_data["place_id"]).first


@pytest.mark.django_db
def test_create_google_city_when_google_city_exist(city_location_minsk_google_data, authenticated_user):
    authenticated_user.post(reverse(CITY_LIST_URL), data=city_location_minsk_google_data, format="json")
    response = authenticated_user.post(reverse(CITY_LIST_URL), data=city_location_minsk_google_data, format="json")
    assert response.status_code == 409
    assert response.data == ["This city already exist"]


@pytest.mark.django_db
def test_create_google_city_when_yandex_city_exist(city_location_minsk_google_data, city_location_minsk_yandex_data,
                                                   authenticated_user):
    authenticated_user.post(reverse(CITY_LIST_URL), data=city_location_minsk_yandex_data, format="json")
    response = authenticated_user.post(reverse(CITY_LIST_URL), data=city_location_minsk_google_data, format="json")
    assert response.status_code == 409
    assert response.data == ["This city already exist"]


@pytest.mark.django_db
def test_delete_city(authenticated_user, city_location_default):
    city_id = city_location_default.id
    response_1 = authenticated_user.delete(reverse(CITY_GET_URL, args=[city_id]))
    response_2 = authenticated_user.get(reverse(CITY_GET_URL, args=[city_id]))
    assert response_1.status_code == 204
    assert not CityLocation.objects.filter(id=city_id).first()
    assert response_2.status_code == 404


@pytest.mark.django_db
def test_get_city(authenticated_user, city_location_default, city_location_minsk_google_data):
    city_id = city_location_default.id
    response = authenticated_user.get(reverse(CITY_GET_URL, args=[city_id]))
    assert response.status_code == 200
    assert response.data.get('location') == city_location_minsk_google_data.get('location')
    assert response.data.get('city_south_west_point') == city_location_minsk_google_data.get('city_south_west_point')
    assert response.data.get('city_north_east_point') == city_location_minsk_google_data.get('city_north_east_point')


@pytest.mark.django_db
@pytest.mark.usefixtures('city_location_default')
def test_get_city_list(authenticated_user, city_location_default, city_location_minsk_google_data):
    response = authenticated_user.get(reverse(CITY_LIST_URL))
    assert response.status_code == 200
    assert response.data.get('count') == 1
