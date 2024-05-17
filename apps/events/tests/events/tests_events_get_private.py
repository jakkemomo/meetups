import pytest
from rest_framework.reverse import reverse

from apps.profiles.tests.utils import get_tokens
from apps.events.tests.events.constants import (
    EVENTS_PRIVATE_GET_URL,
    EVENTS_GET_URL,
)


@pytest.mark.django_db
def test_event_get_private_authorized_authenticated_valid(api_client, event_private, user):
    token = get_tokens(user)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.get(reverse(EVENTS_PRIVATE_GET_URL, args=[event_private.private_token]))
    assert response.status_code == 200
    assert response.data['id'] == event_private.id


@pytest.mark.usefixtures(
    "event_private_user_is_participant",
)
@pytest.mark.django_db
def test_event_get_private_participant_valid(api_client, event_private, user):
    token = get_tokens(user)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.get(reverse(EVENTS_GET_URL, args=[event_private.id]))
    assert response.status_code == 200
    assert response.data['id'] == event_private.id


@pytest.mark.usefixtures(
    "event_private_user_is_participant",
)
@pytest.mark.django_db
def test_event_get_private_participant_token_valid(api_client, event_private, user):
    token = get_tokens(user)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.get(reverse(EVENTS_PRIVATE_GET_URL, args=[event_private.private_token]))
    assert response.status_code == 200
    assert response.data['id'] == event_private.id


@pytest.mark.django_db
def test_event_get_private_authorized_authenticated_invalid_token(api_client, event_private, user):
    token = get_tokens(user)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.get(reverse(EVENTS_PRIVATE_GET_URL, args=[123]))
    assert response.status_code == 404


@pytest.mark.django_db
def test_event_get_private_unauthorized_unauthenticated(api_client, event_private):
    response = api_client.get(reverse(EVENTS_GET_URL, args=[event_private.id]))
    assert response.status_code == 401


@pytest.mark.django_db
def test_event_get_private_unauthorized_authenticated(api_client, event_private, user):
    token = get_tokens(user)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.get(reverse(EVENTS_GET_URL, args=[event_private.id]))
    assert response.status_code == 403


@pytest.mark.django_db
def test_event_get_private_unauthorized_unauthenticated_token(api_client, event_private, user):
    response = api_client.get(reverse(EVENTS_PRIVATE_GET_URL, args=[event_private.private_token]))
    assert response.status_code == 401
