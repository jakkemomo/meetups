import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

import pytest
import asyncio

from rest_framework.test import APIClient
from django.test import AsyncClient
from channels.routing import URLRouter
from channels.db import database_sync_to_async

from apps.profiles.models import User
from apps.profiles.models.followers import Follower
from apps.events.models import Event
from apps.chats.models import Chat
from config.urls import websocket_urlpatterns


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture
def user() -> User:
    return User.objects.create(
        email="user@example.com",
        password="test",
        is_email_verified=True,
    )


@pytest.fixture()
def user_location_data(city_location_data) -> dict:
    return {
        "city_location": city_location_data,
    }


@pytest.fixture()
def user_location_data_2(city_location_data_2) -> dict:
    return {
        "city_location": city_location_data_2,
    }


@pytest.fixture
def city_location_data() -> dict:
    return {
        "place_id": "ChIJ02oeW9PP20YR2XC13VO4YQs",
        "location": {
            "latitude": 53.902284,
            "longitude": 27.561831
        },
        "south_west_point": {
            "latitude": 53.82427,
            "longitude": 27.38909
        },
        "north_east_point": {
            "latitude": 53.97800,
            "longitude": 27.76125
        },
    }


@pytest.fixture
def city_location_data_2() -> dict:
    return {
        "place_id": "ChIJybDUc_xKtUYRTM9XV8zWRD0",
        "location": {
            "latitude": 53.902284,
            "longitude": 27.561831
        },
        "south_west_point": {
            "latitude": 53.82427,
            "longitude": 27.38909
        },
        "north_east_point": {
            "latitude": 53.97800,
            "longitude": 27.76125
        },
    }


@pytest.fixture
def user_2() -> User:
    return User.objects.create(
        email="user2@example.com",
        password="test2",
        is_email_verified=True,
    )


@pytest.fixture
def user_private() -> User:
    return User.objects.create(
        email="user_private@example.com",
        password="test",
        is_private=True,
    )


@pytest.fixture
def user_2_private() -> User:
    return User.objects.create(
        email="user2_private@example.com",
        password="test2",
        is_private=True,
    )


@pytest.fixture
def follower_user_accepted(user, user_2) -> Follower:
    data = {
        'user': user_2,
        'follower': user,
        'status': Follower.Status.ACCEPTED,
    }
    return Follower.objects.create(**data)


@pytest.fixture
def follower_user_accepted_private(user_private, user_2_private) -> Follower:
    data = {
        'user': user_2_private,
        'follower': user_private,
        'status': Follower.Status.ACCEPTED,
    }
    return Follower.objects.create(**data)


@pytest.fixture
def follower_user_pending_private(user_private, user_2_private) -> Follower:
    data = {
        'user': user_2_private,
        'follower': user_private,
        'status': Follower.Status.PENDING,
    }
    return Follower.objects.create(**data)


@pytest.fixture
def follower_user_declined_private(user_private, user_2_private) -> Follower:
    data = {
        'user': user_2_private,
        'follower': user_private,
        'status': Follower.Status.DECLINED,
    }
    return Follower.objects.create(**data)


@pytest.fixture
def follower_user_2_accepted(user, user_2) -> Follower:
    data = {
        'user': user,
        'follower': user_2,
        'status': Follower.Status.ACCEPTED,
    }
    return Follower.objects.create(**data)


@pytest.fixture
def follower_user_2_accepted_private(user_private, user_2_private) -> Follower:
    data = {
        'user': user_private,
        'follower': user_2_private,
        'status': Follower.Status.ACCEPTED,
    }
    return Follower.objects.create(**data)


@pytest.fixture
async def async_follower_user_accepted_private(async_user, async_user_2_private) -> Follower:
    data = {
        'user': async_user_2_private,
        'follower': async_user,
        'status': Follower.Status.ACCEPTED,
    }
    follower = await database_sync_to_async(Follower.objects.create)(**data)
    return follower


@pytest.fixture
def follower_user_2_pending_private(user_private, user_2_private) -> Follower:
    data = {
        'user': user_private,
        'follower': user_2_private,
        'status': Follower.Status.PENDING,
    }
    return Follower.objects.create(**data)


@pytest.fixture
async def async_follower_user_pending_private(
        async_user_private,
        async_user_2_private
) -> Follower:
    data = {
        'user': async_user_2_private,
        'follower': async_user_private,
        'status': Follower.Status.PENDING,
    }
    follower = await database_sync_to_async(Follower.objects.create)(**data)
    return follower


@pytest.fixture
def follower_user_2_declined_private(user_private, user_2_private) -> Follower:
    data = {
        'user': user_private,
        'follower': user_2_private,
        'status': Follower.Status.DECLINED,
    }
    return Follower.objects.create(**data)


@pytest.fixture
def event() -> Event:
    chat = Chat.objects.create(type=Chat.Type.EVENT)
    return Event.objects.create(
        name="test_event",
        chat=chat,
        image_url="test_image_url",
    )


@pytest.fixture
def event_private() -> Event:
    return Event.objects.create(
        name="private_event",
        type="private",
        private_token="token"
    )


@pytest.fixture
def event_created_by_user_2(user_2) -> Event:
    return Event.objects.create(
        name="test_event",
        created_by=user_2,
    )


@pytest.fixture
def event_private_created_by_user_2(user_2) -> Event:
    return Event.objects.create(
        name="test_event",
        type="private",
        created_by=user_2,
    )


@pytest.fixture
def event_created_by_user_2_private(user_2_private) -> Event:
    return Event.objects.create(
        name="test_event",
        created_by=user_2_private,
    )


@pytest.fixture
def event_private_created_by_user_2_private(user_2_private) -> Event:
    return Event.objects.create(
        name="test_event",
        type="private",
        created_by=user_2_private,
    )


@pytest.fixture
def event_user_is_participant(user, event) -> Event:
    event.participants.add(user.id)
    event.save()
    return event


@pytest.fixture
def event_private_user_is_participant(user, event_private) -> Event:
    event_private.participants.add(user.id)
    event_private.save()
    return event_private


@pytest.fixture
def event_user_2_is_participant(user_2, event) -> Event:
    event.participants.add(user_2.id)
    event.save()
    return event


@pytest.fixture
def event_user_2_is_participant_private(user_2_private, event) -> Event:
    event.participants.add(user_2_private.id)
    event.save()
    return event


@pytest.fixture
def event_private_user_2_is_participant(user_2, event_private) -> Event:
    event_private.participants.add(user_2.id)
    event_private.save()
    return event_private


@pytest.fixture
def event_private_user_2_is_participant_private(user_2_private, event_private) -> Event:
    event_private.participants.add(user_2_private.id)
    event_private.save()
    return event_private


@pytest.fixture
def application() -> URLRouter:
    return URLRouter(websocket_urlpatterns)


@pytest.fixture
async def async_client() -> AsyncClient:
    return AsyncClient()


@pytest.fixture
async def async_user() -> User:
    data = {
        "email": "user@example.com",
        "username": "test_user",
        "password": "test",
        "image_url": "test_image_url",
    }
    return await database_sync_to_async(User.objects.create)(**data)


@pytest.fixture
async def async_user_2() -> User:
    data = {
        "email": "user2@example.com",
        "username": "test_user_2",
        "password": "test",
        "image_url": "test_image_url_2",
    }
    return await database_sync_to_async(User.objects.create)(**data)


@pytest.fixture
async def async_user_private() -> User:
    data = {
        "email": "user_private@example.com",
        "username": "test_user_private",
        "password": "test",
        "is_private": True,
        "image_url": "test_image_url",
    }
    return await database_sync_to_async(User.objects.create)(**data)


@pytest.fixture
async def async_user_2_private() -> User:
    data = {
        "email": "user2_private@example.com",
        "username": "test_user_2_private",
        "password": "test",
        "is_private": True,
        "image_url": "test_image_url_2",
    }
    return await database_sync_to_async(User.objects.create)(**data)


@pytest.fixture(scope="session")
def event_loop():
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def user_in_event(
        async_user,
        event,
):
    database_sync_to_async(event.participants.add)(async_user.id)


@pytest.fixture
async def user_and_user_2_in_event(
        async_user,
        async_user_2,
        event,
):
    await database_sync_to_async(event.participants.add)(async_user.id)
    await database_sync_to_async(event.participants.add)(async_user_2.id)


@pytest.fixture
async def event_chat_with_users(async_user, async_user_2) -> Chat:
    chat = await database_sync_to_async(Chat.objects.create)(type=Chat.Type.EVENT)
    await database_sync_to_async(chat.participants.add)(async_user, async_user_2)
    return chat
