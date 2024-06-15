import pytest
from rest_framework.reverse import reverse

from apps.profiles.tests.utils import get_tokens
from apps.events.tests.events.constants import EVENTS_LIST_URL
from config import settings


@pytest.mark.django_db
def test_event_list_unauthorised_valid(
        api_client,
        event,
        event_private,
):
    response = api_client.get(reverse(EVENTS_LIST_URL))

    # assertions
    assert response.status_code == 200
    assert response.data.get("count") == 1
    assert response.data.get("next") is None
    assert response.data.get("previous") is None
    results = response.data.get("results")
    assert results[0].get("id") == event.id


@pytest.mark.django_db
def test_event_list_authorised_valid(
        api_client,
        event,
        user_2,
        event_user_2_is_participant,
        event_private,
):
    token = get_tokens(user_2)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.get(reverse(EVENTS_LIST_URL))

    # assertions
    assert response.status_code == 200
    assert response.data.get("count") == 1
    assert response.data.get("next") is None
    assert response.data.get("previous") is None
    results = response.data.get("results")
    assert results[0].get("id") == event.id


@pytest.mark.django_db
def test_event_list_authorised_with_private_valid(
        api_client,
        user_2,
        event_private,
        event_private_user_2_is_participant,
):
    token = get_tokens(user_2)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.get(reverse(EVENTS_LIST_URL))

    # assertions
    assert response.status_code == 200
    assert response.data.get("count") == 1
    assert response.data.get("next") is None
    assert response.data.get("previous") is None
    results = response.data.get("results")
    assert results[0].get("id") == event_private.id


@pytest.mark.django_db
def test_event_list_authorised_hundred_valid(
        api_client,
        user,
        hundred_events,
):
    token = get_tokens(user)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.get(reverse(EVENTS_LIST_URL))

    pagination = settings.REST_FRAMEWORK.get("PAGE_SIZE")

    # assertions
    assert response.status_code == 200
    assert response.data.get("count") == 100
    assert response.data.get("next")
    assert response.data.get("previous") is None
    results = response.data.get("results")
    assert len(results) == pagination

    last_events = hundred_events[pagination:][::-1]

    for i in range(pagination):
        result = results[i]
        event = last_events[i]
        assert result.get("id") == event.id

        if i > 0:
            assert results[i]["start_date"] <= results[i - 1]["start_date"]


@pytest.mark.django_db
def test_event_get_unauthorised_empty(api_client, event_private):
    response = api_client.get(reverse(EVENTS_LIST_URL))

    # assertions
    assert response.status_code == 200
    assert response.data.get("count") == 0
    assert response.data.get("next") is None
    assert response.data.get("previous") is None
    assert response.data.get("results") == []


@pytest.mark.django_db
def test_event_get_authorised_not_found(api_client, user, event_private):
    token = get_tokens(user)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.get(reverse(EVENTS_LIST_URL))

    # assertions
    assert response.status_code == 200
    assert response.data.get("count") == 0
    assert response.data.get("next") is None
    assert response.data.get("previous") is None
    assert response.data.get("results") == []


@pytest.mark.django_db
def test_event_get_filtered_by_geo(api_client, hundred_events):
    response_minsk = api_client.get(
        reverse(EVENTS_LIST_URL), data={'min_lat': '53.829', 'max_lat': '53.973', 'min_lng': '27.401',
                                        'max_lng': '27.703', })
    response_moscow = api_client.get(
        reverse(EVENTS_LIST_URL), data={'min_lat': '55.569', 'max_lat': '55.916', 'min_lng': '37.360',
                                        'max_lng': '37.859', }
    )
    assert response_minsk.status_code == 200
    assert response_moscow.status_code == 200
    assert response_minsk.data.get('count') == 100
    assert response_moscow.data.get('count') == 0
