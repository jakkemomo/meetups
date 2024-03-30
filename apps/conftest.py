import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

import pytest
from rest_framework.test import APIClient

from apps.profiles.models import User, City
from apps.profiles.models.followers import Follower


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
def follower_user_2_pending_private(user_private, user_2_private) -> Follower:
    data = {
        'user': user_private,
        'follower': user_2_private,
        'status': Follower.Status.PENDING,
    }
    return Follower.objects.create(**data)


@pytest.fixture
def follower_user_2_declined_private(user_private, user_2_private) -> Follower:
    data = {
        'user': user_private,
        'follower': user_2_private,
        'status': Follower.Status.DECLINED,
    }
    return Follower.objects.create(**data)


@pytest.fixture
def city() -> City:
    if not City.objects.filter(id=1):
        return City.objects.create(id=1)
