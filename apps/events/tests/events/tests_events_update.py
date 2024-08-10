import pytest
from rest_framework.exceptions import ErrorDetail
from rest_framework.reverse import reverse

from apps.events.models import Event
from apps.profiles.tests.utils import get_tokens
from apps.events.tests.events.constants import EVENTS_GET_URL


@pytest.mark.django_db
def test_event_update_valid(
        api_client,
        user_2,
        event_created_by_user_2,
        event_data,
):
    token = get_tokens(user_2)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.put(
        reverse(EVENTS_GET_URL, args=[event_created_by_user_2.id]),
        data=event_data,
        format="json",
    )

    # assertions

    assert response.status_code == 200
    changed_event = Event.objects.filter(created_by=user_2).first()
    assert changed_event
    assert changed_event.name == event_data.get("name")


@pytest.mark.django_db
def test_event_update_repeatable_valid(
        api_client,
        user_2,
        event_created_by_user_2,
        event_data,
):
    event_data['repeatable'] = True
    event_data['schedule'] = [
        {
            "day_of_week": "mon",
            "time": "17:30:00"
        },
        {
            "day_of_week": "sun",
            "time": "20:00:00"
        }
    ]
    event_data.pop('start_date', None)
    event_data.pop('end_date', None)
    event_data.pop('start_time', None)
    event_data.pop('end_time', None)

    token = get_tokens(user_2)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.put(
        reverse(EVENTS_GET_URL, args=[event_created_by_user_2.id]),
        data=event_data,
        format="json",
    )

    # assertions
    assert response.status_code == 200
    changed_event = Event.objects.filter(created_by=user_2).first()
    assert changed_event
    assert changed_event.repeatable == event_data.get("repeatable")


@pytest.mark.django_db
def test_event_update_free_valid(
        api_client,
        user_2,
        event_created_by_user_2,
        event_data,
):
    event_data['free'] = True
    event_data.pop("cost")
    event_data.pop("currency")

    token = get_tokens(user_2)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.put(
        reverse(EVENTS_GET_URL, args=[event_created_by_user_2.id]),
        data=event_data,
        format="json",
    )

    # assertions
    assert response.status_code == 200
    changed_event = Event.objects.filter(created_by=user_2).first()
    assert changed_event
    assert changed_event.free == event_data.get("free")


@pytest.mark.django_db
def test_event_update_cost_no_currency(
        api_client,
        user_2,
        event_created_by_user_2,
        event_data,
):
    event_data['currency'] = None

    token = get_tokens(user_2)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.put(
        reverse(EVENTS_GET_URL, args=[event_created_by_user_2.id]),
        data=event_data,
        format="json",
    )

    # assertions
    assert response.status_code == 400
    assert response.data == {
        'non_field_errors': [
            ErrorDetail(
                string='Cost and currency must be provided at the same time',
                code='invalid'
            )
        ]
    }
    changed_event = Event.objects.filter(created_by=user_2).first()
    assert changed_event
    assert changed_event.name != event_data.get("name")


@pytest.mark.django_db
def test_event_update_unauthenticated(
        api_client,
        user_2,
        event_created_by_user_2,
        event_data,
):
    response = api_client.put(
        reverse(EVENTS_GET_URL, args=[event_created_by_user_2.id]),
        data=event_data,
        format="json",
    )

    # assertions
    assert response.status_code == 401
    changed_event = Event.objects.filter(created_by=user_2).first()
    assert changed_event
    assert changed_event.name != event_data.get("name")


@pytest.mark.django_db
def test_event_update_not_verified(
        api_client,
        user_2,
        event_created_by_user_2,
        event_data,
):
    # unverified email
    user_2.is_email_verified = False
    user_2.save()

    token = get_tokens(user_2)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.put(
        reverse(EVENTS_GET_URL, args=[event_created_by_user_2.id]),
        data=event_data,
        format="json",
    )

    # assertions
    assert response.status_code == 403
    changed_event = Event.objects.filter(created_by=user_2).first()
    assert changed_event
    assert changed_event.name != event_data.get("name")


@pytest.mark.django_db
def test_event_update_not_creator(
        api_client,
        user,
        user_2,
        event_created_by_user_2,
        event_data,
):
    token = get_tokens(user)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.put(
        reverse(EVENTS_GET_URL, args=[event_created_by_user_2.id]),
        data=event_data,
        format="json",
    )

    # assertions
    assert response.status_code == 403
    changed_event = Event.objects.filter(created_by=user_2).first()
    assert changed_event
    assert changed_event.name != event_data.get("name")


@pytest.mark.usefixtures(
    "event_user_is_participant",
)
@pytest.mark.django_db
def test_event_update_participant_not_creator(
        api_client,
        user,
        event,
        event_data,
):
    token = get_tokens(user)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.put(
        reverse(EVENTS_GET_URL, args=[event.id]),
        data=event_data,
        format="json",
    )

    # assertions
    assert response.status_code == 403
    changed_event = Event.objects.filter(name=event.name).first()
    assert changed_event
    assert changed_event.name != event_data.get("name")
