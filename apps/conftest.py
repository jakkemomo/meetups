import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

import pytest
from rest_framework.test import APIClient
from channels.db import database_sync_to_async

from apps.profiles.models import User
from apps.profiles.models.followers import Follower
from apps.events.models import Event
from apps.websockets.models import Chat


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
def event() -> Event:
    chat = Chat.objects.create(type=Chat.Type.EVENT)
    return Event.objects.create(
        name="test_event",
        chat=chat,
    )


@pytest.fixture
def event_not_visible() -> Event:
    return Event.objects.create(
        name="test_event",
        is_visible=False,
    )


@pytest.fixture
def event_created_by_user_2(user_2) -> Event:
    return Event.objects.create(
        name="test_event",
        created_by=user_2,
    )


@pytest.fixture
def event_not_visible_created_by_user_2(user_2) -> Event:
    return Event.objects.create(
        name="test_event",
        is_visible=False,
        created_by=user_2,
    )


@pytest.fixture
def event_created_by_user_2_private(user_2_private) -> Event:
    return Event.objects.create(
        name="test_event",
        created_by=user_2_private,
    )


@pytest.fixture
def event_not_visible_created_by_user_2_private(user_2_private) -> Event:
    return Event.objects.create(
        name="test_event",
        is_visible=False,
        created_by=user_2_private,
    )


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
def event_not_visible_user_2_is_participant(user_2, event_not_visible) -> Event:
    event_not_visible.participants.add(user_2.id)
    event_not_visible.save()
    return event_not_visible


@pytest.fixture
def event_not_visible_user_2_is_participant_private(user_2_private, event_not_visible) -> Event:
    event_not_visible.participants.add(user_2_private.id)
    event_not_visible.save()
    return event_not_visible


@pytest.fixture
async def chat_with_users(async_user, async_user_2) -> Chat:
    chat = await database_sync_to_async(Chat.objects.create)(type=Chat.Type.EVENT)
    await database_sync_to_async(chat.participants.add)(async_user, async_user_2)
    return chat
