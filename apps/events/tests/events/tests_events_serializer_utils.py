import pytest

from apps.events.models import Event
from apps.events.serializers import utils
from apps.events.tests.events.constants import EVENTS_GET_URL
from rest_framework.reverse import reverse

from apps.profiles.tests.utils import get_tokens


def test_area_bbox(city_location_default_data):
    location = city_location_default_data["location"]
    bbox = utils.area_bbox(location)
    bbox_str = 'POLYGON ((27.551831 53.892284000000004, 27.551831 53.912284, 27.571831000000003 53.912284, 27.571831000000003 53.892284000000004, 27.551831 53.892284000000004))'

    assert bbox == bbox_str


@pytest.mark.django_db
def test_data_update_city_not_exist(event_created_by_user_2, event_data,
                                    city_location_default_data,
                                    api_client,
                                    user_2):
    token = get_tokens(user_2)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)

    response = api_client.put(
        reverse(EVENTS_GET_URL, args=[event_created_by_user_2.id]),
        data=event_data,
        format='json',
    )

    assert response.data['city_location'] is not None
    assert response.data['city_location']['place_id'] == city_location_default_data['place_id']
    assert response.data['city_location']['location'] == city_location_default_data['location']


@pytest.mark.django_db
def test_data_update_city_exist_place_id_not_empty(event_created_by_user_2, event_data,
                                                   event_yandex_city_location_data,
                                                   api_client,
                                                   user_2):
    token = get_tokens(user_2)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)

    response_1 = api_client.put(
        reverse(EVENTS_GET_URL, args=[event_created_by_user_2.id]),
        data=event_data,
        format='json',
    )
    response_2 = api_client.put(
        reverse(EVENTS_GET_URL, args=[event_created_by_user_2.id]),
        data=event_yandex_city_location_data,
        format='json',
    )

    assert response_2.data['city_location']['place_id'] == response_1.data['city_location']['place_id']
    assert response_2.data['city_location']['location'] == response_1.data['city_location']['location']


@pytest.mark.django_db
def tests_update_city_exist_place_id_is_empty(event_created_by_user_2, event_data,
                                              event_yandex_city_location_data,
                                              api_client,
                                              user_2):
    token = get_tokens(user_2)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response_1 = api_client.put(
        reverse(EVENTS_GET_URL, args=[event_created_by_user_2.id]),
        data=event_yandex_city_location_data,
        format='json',
    )
    response_2 = api_client.put(
        reverse(EVENTS_GET_URL, args=[event_created_by_user_2.id]),
        data=event_data,
        format='json',
    )

    assert response_1.data['city_location']['place_id'] == ''
    assert response_2.data['city_location']['place_id'] != response_1.data['city_location']['place_id']
    assert response_2.data['city_location']['place_id'] != ''
