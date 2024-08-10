import datetime
import random
import string
from random import choices
from typing import List

import pytest
from cities_light.contrib.restframework3 import City, Region, Country
from django.contrib.gis.geos import Point
from django.utils import timezone

from apps.events.models import Event, Category, Tag, Currency
# from apps.events.models.city import City
from apps.profiles.tests.utils import get_tokens
from rest_framework.test import APIClient


@pytest.fixture
def hundred_events(city_minsk) -> List:
    events = []
    for i in range(100):
        name = ''.join(choices(string.ascii_uppercase + string.digits, k=20))
        start_date = timezone.now() + datetime.timedelta(days=i)
        end_date = start_date + datetime.timedelta(hours=random.randint(1, 5))
        # todo: change time handling to freezegun or mock
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
            city=city_minsk
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


# @pytest.fixture
# def city_location_yandex(city_location_minsk_yandex_data):
#     city = City.objects.create(
#         location=Point(city_location_minsk_yandex_data["location"]["longitude"],
#                        city_location_minsk_yandex_data["location"]["latitude"]),
#         place_id=city_location_minsk_yandex_data["place_id"],
#     )
#     return city
@pytest.fixture
def country_minsk():
    country = Country.objects.create(
        **
  {
    "id": 36,
    "name_ascii": "Belarus",
    "slug": "belarus",
    "geoname_id": 630336,
    "alternate_names": "Belarus’;Republic of Belarus;Respublika Belarus’;Respublika Byelarus’;Беларусь;Белоруссия;Республика Беларусь;Рэспубліка Беларусь",
    "name": "Belarus",
    "code2": "BY",
    "code3": "BLR",
    "continent": "EU",
    "tld": "by",
    "phone": "375"
  })

    return country

@pytest.fixture
def region_minsk(country_minsk):
    region = Region.objects.create(
        **  {
    "id": 457,
    "name_ascii": "Minsk City",
    "slug": "minsk-city",
    "geoname_id": 625143,
    "alternate_names": "Горад Мінск",
    "name": "Minsk City",
    "display_name": "Minsk City, Belarus",
    "geoname_code": "04",
    "country_id": 36
  }
    )
    return region

@pytest.fixture
def city_minsk(region_minsk, country_minsk):
    city = City.objects.create(
        **{
            "id": 2495,
            "name_ascii": "Minsk",
            "slug": "minsk",
            "geoname_id": 625144,
            "alternate_names": "Минск;Мінск",
            "name": "Minsk",
            "display_name": "Minsk, Minsk City, Belarus",
            "search_names": "minskbelarus minskbelorussiia minskgoradminskbelarus minskgoradminskbelorussiia minskgoradminskrepublicofbelarus minskgoradminskrespublikabelarus minskgoradminskrespublikabyelarus minskminskcitybelarus minskminskcitybelorussiia minskminskcityrepublicofbelarus minskminskcityrespublikabelarus minskminskcityrespublikabyelarus minskrepublicofbelarus minskrespublikabelarus minskrespublikabyelarus",
            "latitude": 53.90000,
            "longitude": 27.56667,
            "region_id": 457,
            "country_id": 36,
            "population": 1742124,
            "feature_code": "PPLC",
            "timezone": "Europe/Minsk",
            "subregion_id": None,
            "display_name_ru": "Минск, Минская область, Беларусь",
            "display_name_en": "Minsk, Minsk City, Belarus",
            "name_ru": "Минск",
            "name_en": "Minsk"
        }
    )
    return city


@pytest.fixture
def event_data(currency, tag, category, city_minsk) -> dict:
    return {
        "name": "Test Event",
        "address": "123 Test St",
        "city_id": 2495,
        "country_id": 36,
        "type": "open",
        "description": "This is an example event.",
        "location": {
            "latitude": 53.902284,
            "longitude": 27.561831
        },
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
def event_yandex_city_location_data(currency, tag, category) -> dict:
    return {
        "name": "Test Event",
        "address": "123 Test St",
        "city_id": 2495,
        "country_id": 36,
        "type": "open",
        "description": "This is an example event.",
        "location": {
            "latitude": 53.902284,
            "longitude": 27.561831
        },
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
        "end_time": "18:00:00"
    }


@pytest.fixture
def event_from_data_created_by_user_2(event_data, user_2):
    return Event.objects.create(**event_data, created_by=user_2)


@pytest.fixture()
def authenticated_user(api_client, user) -> APIClient:
    token = get_tokens(user)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    return api_client
