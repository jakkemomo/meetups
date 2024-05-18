import pytest
from rest_framework.reverse import reverse

from apps.profiles.tests.utils import get_tokens
from apps.events.tests.events.constants import EVENTS_GET_URL


@pytest.mark.django_db
def test_event_get_unauthorised_valid(
        api_client,
        event,
):
    response = api_client.get(
        reverse(EVENTS_GET_URL, args=[event.id])
    )

    # assertions
    assert response.status_code == 200
    assert response.data == {
        'id': event.id,
        'tags': list(event.tags.all()),
        'category': event.category,
        'created_by': event.created_by,
        'location': (event.location.x, event.location.y),
        'participants_number': event.participants.count(),
        'average_rating': sum(event.ratings.values_list("value", flat=True))/len(event.ratings.all()) if len(event.ratings.all()) else 0.0,
        'currency': event.currency,
        'schedule': list(event.schedule.all()),
        'is_favorite': False,
        'is_participant': False,
        'created_at': event.created_at.strftime('%Y-%m-%dT%H:%M:%S.%f') + 'Z',
        'updated_at': event.updated_at.strftime('%Y-%m-%dT%H:%M:%S.%f') + 'Z',
        'name': event.name,
        'address': event.address,
        'city': event.city,
        'country': event.country,
        'image_url': event.image_url,
        'type': event.type,
        'description': event.description,
        'participants_age': event.participants_age,
        'desired_participants_number': event.desired_participants_number,
        'cost': event.cost,
        'start_date': event.start_date,
        'end_date': event.end_date,
        'start_time': event.start_time,
        'end_time': event.end_time,
        'private_token': event.private_token,
        'is_finished': event.is_finished,
        'is_visible': event.is_visible,
        'any_participant_number': event.any_participant_number,
        'repeatable': event.repeatable,
        'free': event.free,
        'gallery': event.gallery,
        'chat': event.chat.id,
        'favorites': list(event.favorites.all()),
    }


@pytest.mark.django_db
def test_event_get_authorised_valid(
        api_client,
        event,
        user_2,
        event_user_2_is_participant,
):
    token = get_tokens(user_2)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.get(
        reverse(EVENTS_GET_URL, args=[event.id])
    )

    # assertions
    assert response.status_code == 200
    assert response.data == {
        'id': event.id,
        'tags': list(event.tags.all()),
        'category': event.category,
        'created_by': event.created_by,
        'location': (event.location.x, event.location.y),
        'participants_number': event.participants.count(),
        'average_rating': sum(event.ratings.values_list("value", flat=True))/len(event.ratings.all()) if len(event.ratings.all()) else 0.0,
        'currency': event.currency,
        'schedule': list(event.schedule.all()),
        'is_favorite': False,
        'is_participant': True,
        'created_at': event.created_at.strftime('%Y-%m-%dT%H:%M:%S.%f') + 'Z',
        'updated_at': event.updated_at.strftime('%Y-%m-%dT%H:%M:%S.%f') + 'Z',
        'name': event.name,
        'address': event.address,
        'city': event.city,
        'country': event.country,
        'image_url': event.image_url,
        'type': event.type,
        'description': event.description,
        'participants_age': event.participants_age,
        'desired_participants_number': event.desired_participants_number,
        'cost': event.cost,
        'start_date': event.start_date,
        'end_date': event.end_date,
        'start_time': event.start_time,
        'end_time': event.end_time,
        'private_token': event.private_token,
        'is_finished': event.is_finished,
        'is_visible': event.is_visible,
        'any_participant_number': event.any_participant_number,
        'repeatable': event.repeatable,
        'free': event.free,
        'gallery': event.gallery,
        'chat': event.chat.id,
        'favorites': list(event.favorites.all()),
    }


@pytest.mark.django_db
def test_event_get_unauthorised_not_found(api_client):
    response = api_client.get(reverse(EVENTS_GET_URL, args=[999]))

    # assertions
    assert response.status_code == 404


@pytest.mark.django_db
def test_event_get_authorised_not_found(api_client, user):
    token = get_tokens(user)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.get(reverse(EVENTS_GET_URL, args=[999]))

    # assertions
    assert response.status_code == 404
