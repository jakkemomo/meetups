import pytest
from rest_framework.reverse import reverse

from apps.events.models import Event
from apps.events.tests.events.constants import EVENTS_GET_URL
from apps.profiles.tests.utils import get_tokens


@pytest.mark.django_db
def test_event_delete_valid(api_client, user_2, event_created_by_user_2):
    token = get_tokens(user_2)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.delete(reverse(EVENTS_GET_URL, args=[event_created_by_user_2.id]))

    # assertions
    assert response.status_code == 204
    assert not Event.objects.filter(created_by=user_2).first()


@pytest.mark.django_db
def test_event_delete_unauthorised_unauthenticated(api_client, user_2, event_created_by_user_2):
    response = api_client.delete(reverse(EVENTS_GET_URL, args=[event_created_by_user_2.id]))

    # assertions
    assert response.status_code == 401
    assert Event.objects.filter(created_by=user_2).first()


@pytest.mark.django_db
def test_event_delete_unauthorised_not_verified(api_client, user_2, event_created_by_user_2):
    # unverified email
    user_2.is_email_verified = False
    user_2.save()

    token = get_tokens(user_2)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.delete(reverse(EVENTS_GET_URL, args=[event_created_by_user_2.id]))

    # assertions
    assert response.status_code == 403
    assert Event.objects.filter(created_by=user_2).first()


@pytest.mark.django_db
def test_event_delete_unauthorised_not_creator(api_client, user, event):
    token = get_tokens(user)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.delete(reverse(EVENTS_GET_URL, args=[event.id]))

    # assertions
    assert response.status_code == 403
    assert Event.objects.filter(name=event.name).first()


@pytest.mark.usefixtures("event_user_is_participant")
@pytest.mark.django_db
def test_event_delete_unauthorised_participant_not_creator(api_client, user, event):
    token = get_tokens(user)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.delete(reverse(EVENTS_GET_URL, args=[event.id]))

    # assertions
    assert response.status_code == 403
    assert Event.objects.filter(name=event.name).first()
