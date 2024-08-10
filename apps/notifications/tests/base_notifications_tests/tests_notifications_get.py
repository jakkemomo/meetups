import pytest
from rest_framework.reverse import reverse

from apps.notifications.tests.constants import NOTIFICATIONS_GET_URL
from apps.profiles.tests.utils import async_get_tokens


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_notifications_get_valid(async_client, async_user, async_user_notification):
    # User logs in
    token = await async_get_tokens(async_user)
    header = {"Authorization": "Bearer " + token}

    # User gets a specific notification
    response = await async_client.get(
        reverse(NOTIFICATIONS_GET_URL, kwargs={"notification_id": async_user_notification.id}),
        headers=header,
    )

    # Assertions
    assert response.status_code == 200
    assert response.data.get("id") == async_user_notification.id
    assert response.data.get("created_by") == async_user_notification.created_by.id
    assert response.data.get("created_by_username") == async_user_notification.created_by.username
    assert response.data.get("recipient") == async_user.id
    assert response.data.get("recipient_username") == async_user.username
    assert response.data.get("type") == async_user_notification.type
    assert response.data.get("text") == async_user_notification.text


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_notifications_get_not_recipient(
    async_client, async_user, async_user_notification, async_user_2
):
    # Another user logs in
    token = await async_get_tokens(async_user_2)
    header = {"Authorization": "Bearer " + token}

    # Another user tries to get the notification not addressed to them
    response = await async_client.get(
        reverse(NOTIFICATIONS_GET_URL, kwargs={"notification_id": async_user_notification.id}),
        headers=header,
    )

    # Assertions
    assert response.status_code == 404


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_notifications_get_unauthorized(async_client, async_user, async_user_notification):
    # User tries to get the notification without authentication
    response = await async_client.get(
        reverse(NOTIFICATIONS_GET_URL, kwargs={"notification_id": async_user_notification.id})
    )

    # Assertions
    assert response.status_code == 401


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_notifications_get_nonexistent_notification(async_client, async_user):
    # User logs in
    token = await async_get_tokens(async_user)
    header = {"Authorization": "Bearer " + token}

    # User tries to get a notification that does not exist
    response = await async_client.get(
        reverse(NOTIFICATIONS_GET_URL, kwargs={"notification_id": 9999999}), headers=header
    )

    # Assertions
    assert response.status_code == 404
