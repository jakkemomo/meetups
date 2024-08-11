import datetime
import random
import string
from random import choices
from typing import List

import pytest
from django.utils import timezone
from rest_framework.test import APIClient

from apps.events.models import Category, Currency, Event, Tag
from apps.profiles.tests.utils import get_tokens


@pytest.fixture
def hundred_events() -> List:
    events = []
    for i in range(100):
        name = "".join(choices(string.ascii_uppercase + string.digits, k=20))
        start_date = timezone.now() + datetime.timedelta(days=i)
        end_date = start_date + datetime.timedelta(hours=random.randint(1, 5))
        # todo: change time handling to freezegun or mock
        start_time = (
            datetime.datetime.combine(datetime.date.today(), datetime.time())
            + datetime.timedelta(minutes=random.randint(1, 1440))
        ).time()
        end_time = (
            datetime.datetime.combine(datetime.date.today(), start_time)
            + datetime.timedelta(hours=random.randint(1, 5))
        ).time()

        event = Event.objects.create(
            name=name,
            start_date=start_date,
            end_date=end_date,
            start_time=start_time,
            end_time=end_time,
        )
        events.append(event)

    return events


@pytest.fixture
def tag() -> Tag:
    return Tag.objects.create(name="test_tag")


@pytest.fixture
def currency() -> Currency:
    return Currency.objects.create(name="USD")


# @pytest.fixture
# def city_location_yandex(city_location_minsk_yandex_data):
#     city = City.objects.create(
#         location=Point(city_location_minsk_yandex_data["location"]["longitude"],
#                        city_location_minsk_yandex_data["location"]["latitude"]),
#         place_id=city_location_minsk_yandex_data["place_id"],
#     )
#     return city


@pytest.fixture
def event_data(currency, tag, category, city_minsk) -> dict:
    return {
        "name": "Test Event",
        "address": "123 Test St",
        "city": 2495,
        # "country_id": 36,
        "type": "open",
        "description": "This is an example event.",
        "location": {"latitude": 53.902284, "longitude": 27.561831},
        "cost": 10.99,
        "repeatable": False,
        "participants_age": 25,
        "currency": currency.id,
        "free": False,
        "gallery": ["image1.jpg", "image2.jpg"],
        "tags": [tag.id],
        "category": category.id,
        "is_finished": False,
        "is_visible": True,
        "any_participant_number": True,
        "start_date": "2024-05-15",
        "end_date": "2024-05-20",
        "start_time": "08:00:00",
        "end_time": "18:00:00",
    }


@pytest.fixture
def event_yandex_city_location_data(currency, tag, category) -> dict:
    return {
        "name": "Test Event",
        "address": "123 Test St",
        "city": 2495,
        # "country_id": 36,
        "type": "open",
        "description": "This is an example event.",
        "location": {"latitude": 53.902284, "longitude": 27.561831},
        # "city_location": city_location_minsk_yandex_data,
        "cost": 10.99,
        "repeatable": False,
        "participants_age": 25,
        "currency": currency.id,
        "free": False,
        "gallery": ["image1.jpg", "image2.jpg"],
        "tags": [tag.id],
        "category": category.id,
        "is_finished": False,
        "is_visible": True,
        "any_participant_number": True,
        "start_date": "2024-05-15",
        "end_date": "2024-05-20",
        "start_time": "08:00:00",
        "end_time": "18:00:00",
    }


@pytest.fixture
def event_from_data_created_by_user_2(event_data, user_2):
    return Event.objects.create(**event_data, created_by=user_2)


@pytest.fixture()
def authenticated_user(api_client, user) -> APIClient:
    token = get_tokens(user)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    return api_client
