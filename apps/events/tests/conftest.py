import datetime
import random
import string
from random import choices
from typing import List

import pytest
from django.utils import timezone

from apps.events.models import Event, Category, Tag, Currency
from apps.events.models.city import City
from apps.profiles.tests.utils import get_tokens


@pytest.fixture
def hundred_events() -> List:
    events = []
    for i in range(100):
        name = ''.join(choices(string.ascii_uppercase + string.digits, k=20))

        start_date = timezone.now() + datetime.timedelta(days=i)
        end_date = start_date + datetime.timedelta(hours=random.randint(1, 5))
        start_time = (datetime.datetime.combine(datetime.date.today(), datetime.time()) + datetime.timedelta(
            minutes=random.randint(1, 1440))).time()
        end_time = (datetime.datetime.combine(datetime.date.today(), start_time) + datetime.timedelta(
            hours=random.randint(1, 5))).time()

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
def category() -> Category:
    return Category.objects.create(name="test_category")


@pytest.fixture
def tag() -> Tag:
    return Tag.objects.create(name="test_tag")


@pytest.fixture
def currency() -> Currency:
    return Currency.objects.create(name="USD")


@pytest.fixture
def city_location(city_location_default_data) -> City:
    return City.objects.create(city_location_default_data)


@pytest.fixture
def event_data(currency, tag, category, city_location) -> dict:
    return {
        "name": "Test Event",
        "address": "123 Test St",
        "city": "Test City",
        "country": "Test Country",
        "type": "open",
        "description": "This is an example event.",
        "city_location": city_location,
        "place_id": "ChIJ02oeW9PP20YR2XC13VO4YQs",
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
        "end_time": "18:00:00"
    }


@pytest.fixture
def event_from_data_created_by_user_2(event_data, user_2):
    return Event.objects.create(**event_data, created_by=user_2)


@pytest.fixture
def city_location_minsk_google_data() -> dict:
    return {
        "place_id": "ChIJ02oeW9PP20YR2XC13VO4YQs",
        "location": {
            "latitude": 53.902284,
            "longitude": 27.561831
        },
        "city_south_west_point": {
            "latitude": 53.82427,
            "longitude": 27.38909
        },
        "city_north_east_point": {
            "latitude": 53.97800,
            "longitude": 27.76125
        },
    }


@pytest.fixture
def city_location_minsk_yandex_data() -> dict:
    return {
        "place_id": "",
        "location": {
            "latitude": 53.906284,
            "longitude": 27.556831
        },
        "city_south_west_point": {
            "latitude": 53.82427,
            "longitude": 27.38909
        },
        "city_north_east_point": {
            "latitude": 53.97800,
            "longitude": 27.76125
        },
    }


@pytest.fixture
def city_location_default_data() -> dict:
    return {
        "place_id": "ChIJ02oeW9PP20YR2XC13VO4YQs",
        "location": {
            "latitude": 53.902284,
            "longitude": 27.561831
        },
        "city_south_west_point": {
            "latitude": 53.82427,
            "longitude": 27.38909
        },
        "city_north_east_point": {
            "latitude": 53.97800,
            "longitude": 27.76125
        },
    }


@pytest.fixture()
def authenticated_user(api_client, user):
    token = get_tokens(user)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    return api_client
