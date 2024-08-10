import pytest
from cities_light.contrib.restframework3 import City
from rest_framework.exceptions import ErrorDetail
from rest_framework.reverse import reverse

from apps.events.models import Event
from apps.events.tests.events.constants import EVENTS_LIST_URL
from apps.profiles.tests.utils import get_tokens


@pytest.mark.django_db
def test_event_create_valid(api_client, user, event_data):
    token = get_tokens(user)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.post(reverse(EVENTS_LIST_URL), data=event_data, format="json")

    assert response.status_code == 201
    assert Event.objects.filter(name=event_data.get("name")).first()
    body = response.json()
    body.pop("created_at")
    body.pop("updated_at")
    assert body == {
        "id": 1,
        "desired_participants_number": 0,
        "location": {"latitude": 53.902284, "longitude": 27.561831},
        "city": 2495,
        "cost": "10.99",
        "repeatable": False,
        "participants_age": 25,
        "currency": 1,
        "free": False,
        "gallery": ["image1.jpg", "image2.jpg"],
        "schedule": [],
        "tags": [1],
        "category": 1,
        "is_finished": False,
        "is_visible": True,
        "any_participant_number": True,
        "start_date": "2024-05-15",
        "end_date": "2024-05-20",
        "start_time": "08:00:00",
        "end_time": "18:00:00",
        "name": "Test Event",
        "address": "123 Test St",
        "image_url": None,
        "type": "open",
        "description": "This is an example event.",
        "private_token": None,
        "favorites": [],
    }


@pytest.mark.django_db
def test_event_create_repeatable_valid(api_client, user, event_data):
    event_data["repeatable"] = True
    event_data["schedule"] = [
        {"day_of_week": "mon", "time": "17:30:00"},
        {"day_of_week": "sun", "time": "20:00:00"},
    ]
    event_data.pop("start_date", None)
    event_data.pop("end_date", None)
    event_data.pop("start_time", None)
    event_data.pop("end_time", None)

    token = get_tokens(user)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.post(reverse(EVENTS_LIST_URL), data=event_data, format="json")

    assert response.status_code == 201
    assert Event.objects.filter(name=event_data.get("name")).first()


@pytest.mark.django_db
def test_event_create_free_valid(api_client, user, event_data):
    event_data["free"] = True
    event_data.pop("cost")
    event_data.pop("currency")

    token = get_tokens(user)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.post(reverse(EVENTS_LIST_URL), data=event_data, format="json")

    assert response.status_code == 201
    assert Event.objects.filter(name=event_data.get("name")).first()


@pytest.mark.django_db
def test_event_create_cost_no_currency(api_client, user, event_data):
    event_data["currency"] = None

    token = get_tokens(user)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.post(reverse(EVENTS_LIST_URL), data=event_data, format="json")

    assert response.status_code == 400
    assert response.data == {
        "non_field_errors": [
            ErrorDetail(
                string="Cost and currency must be provided at the same time", code="invalid"
            )
        ]
    }
    assert not Event.objects.filter(name=event_data.get("name")).first()


@pytest.mark.django_db
def test_event_create_unauthenticated(api_client):
    data = {}

    response = api_client.post(reverse(EVENTS_LIST_URL), data=data, format="json")

    assert response.status_code == 401
    assert not Event.objects.all().first()


@pytest.mark.django_db
def test_event_create_not_verified(api_client, user):
    user.is_email_verified = False
    user.save()
    data = {}

    token = get_tokens(user)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.post(reverse(EVENTS_LIST_URL), data=data, format="json")

    assert response.status_code == 403
    assert not Event.objects.all().first()


@pytest.mark.django_db
def test_event_create_repeatable_without_schedule(api_client, user, event_data):
    event_data["repeatable"] = True

    token = get_tokens(user)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.post(reverse(EVENTS_LIST_URL), data=event_data, format="json")

    assert response.status_code == 400
    assert response.data == {
        "non_field_errors": [
            ErrorDetail(string="Repeatable event must have a schedule", code="invalid")
        ]
    }
    assert not Event.objects.filter(name=event_data.get("name")).first()


@pytest.mark.django_db
def test_event_create_free_with_cost(api_client, user, event_data):
    event_data["cost"] = 10.99
    event_data["free"] = True

    token = get_tokens(user)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.post(reverse(EVENTS_LIST_URL), data=event_data, format="json")

    assert response.status_code == 400
    assert response.data == {
        "non_field_errors": [
            ErrorDetail(string="Free and cost cannot be provided at the same time", code="invalid")
        ]
    }
    assert not Event.objects.filter(name=event_data.get("name")).first()


@pytest.mark.django_db
def test_event_create_repeatable_schedule_with_start_time(api_client, user, event_data):
    event_data["repeatable"] = True
    event_data["schedule"] = [
        {"day_of_week": "mon", "time": "17:30:00"},
        {"day_of_week": "sun", "time": "20:00:00"},
    ]

    token = get_tokens(user)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.post(reverse(EVENTS_LIST_URL), data=event_data, format="json")

    assert response.status_code == 400
    assert response.data == {
        "non_field_errors": [
            ErrorDetail(
                string="Start date, start time, and schedule cannot be provided at the same time",
                code="invalid",
            )
        ]
    }
    assert not Event.objects.filter(name=event_data.get("name")).first()


@pytest.mark.django_db
def test_event_create_empty_data(api_client, user):
    data = {}

    token = get_tokens(user)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.post(reverse(EVENTS_LIST_URL), data=data)

    assert response.status_code == 400
    assert not Event.objects.all().first()


@pytest.mark.django_db
def test_event_create_invalid_age(api_client, user, event_data):
    event_data["participants_age"] = 150

    token = get_tokens(user)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.post(reverse(EVENTS_LIST_URL), data=event_data, format="json")

    assert response.status_code == 400
    assert not Event.objects.filter(name=event_data.get("name")).first()


# @pytest.mark.django_db
# def test_event_create_google_city_when_city_exist(
#         api_client,
#         user,
#         event_data,
#         city_minsk):
#     token = get_tokens(user)
#     api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
#     response = api_client.post(reverse(EVENTS_LIST_URL), data=event_data, format="json")
#     count = City.objects.all().count()
#     assert response.status_code == 201
#     assert count == 1
