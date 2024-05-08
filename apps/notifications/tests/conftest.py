import pytest
from channels.db import database_sync_to_async

from apps.notifications.models import Notification


@pytest.fixture
async def async_user_notification(async_user) -> Notification:
    data = {
        "recipient": async_user,
        "type": Notification.Type.NEW_FOLLOWER
    }
    return await database_sync_to_async(Notification.objects.create)(**data)


@pytest.fixture
async def async_user_hundred_notifications(async_user) -> list:
    data = {
        "recipient": async_user,
        "type": Notification.Type.NEW_FOLLOWER
    }
    notifications = []
    for _ in range(100):
        notification = await database_sync_to_async(Notification.objects.create)(**data)
        notifications.append(notification)

    return notifications
