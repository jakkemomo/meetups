import asyncio

import pytest

from channels.routing import URLRouter
from channels.db import database_sync_to_async
from django.test import AsyncClient

from apps.profiles.models import User, City
from apps.profiles.routers import websocket_urlpatterns


@pytest.fixture
def application() -> URLRouter:
    return URLRouter(websocket_urlpatterns)


@pytest.fixture
async def async_client() -> AsyncClient:
    return AsyncClient()


@pytest.fixture
async def async_user(city) -> User:
    data = {
        "email": "user@example.com",
        "password": "test",
    }
    return await database_sync_to_async(User.objects.create)(**data)


@pytest.fixture
async def async_user_2(city) -> User:
    data = {
        "email": "user2@example.com",
        "password": "test",
    }
    return await database_sync_to_async(User.objects.create)(**data)


@pytest.fixture
async def async_user_private(city) -> User:
    data = {
        "email": "user_private@example.com",
        "password": "test",
        "is_private": True
    }
    return await database_sync_to_async(User.objects.create)(**data)


@pytest.fixture
async def async_user_2_private(city) -> User:
    data = {
        "email": "user2_private@example.com",
        "password": "test",
        "is_private": True
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
