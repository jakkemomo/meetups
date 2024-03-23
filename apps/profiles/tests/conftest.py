import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

import pytest
from rest_framework.test import APIClient

from apps.profiles.models import User, City


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture
def user() -> User:
    return User.objects.create(email="user@example.com", password="test")


@pytest.fixture
def user_2() -> User:
    return User.objects.create(email="user2@example.com", password="test2")


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
def city() -> City:
    if not City.objects.filter(id=1):
        return City.objects.create(id=1)
