import pytest
from rest_framework.reverse import reverse

from apps.notifications.tests.constants import NOTIFICATIONS_LIST_URL
from apps.profiles.tests.utils import async_get_tokens
from config import settings


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_notifications_list_valid(
        async_client,
        async_user,
        async_user_notification,
):
    # user logs in
    token = await async_get_tokens(async_user)
    header = {"Authorization": "Bearer " + token}

    # user gets notifications list
    response = await async_client.get(
        reverse(NOTIFICATIONS_LIST_URL),
        headers=header,
    )

    # assertions
    assert response.status_code == 200
    assert response.data.get("count") == 1
    assert not response.data.get("next")
    assert not response.data.get("previous")
    results = response.data.get("results")[0]
    assert results.get("id") == async_user_notification.id
    assert results.get("created_by") == async_user_notification.created_by
    assert results.get("recipient") == async_user.id
    assert results.get("type") == async_user_notification.type


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_notifications_list_unauthorized(
        async_client,
):
    # User gets notifications list without authorization
    response = await async_client.get(
        reverse(NOTIFICATIONS_LIST_URL),
    )

    # Assertions
    assert response.status_code == 401


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_notifications_list_empty(
        async_client,
        async_user,
):
    # User logs in
    token = await async_get_tokens(async_user)
    header = {"Authorization": "Bearer " + token}

    # User gets notifications list
    response = await async_client.get(
        reverse(NOTIFICATIONS_LIST_URL),
        headers=header,
    )

    # Assertions
    assert response.status_code == 200
    assert response.data.get("count") == 0
    assert not response.data.get("next")
    assert not response.data.get("previous")
    assert response.data.get("results") == []


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_notifications_list_hundred_notifications(
        async_client,
        async_user,
        async_user_hundred_notifications,
):
    # User logs in
    token = await async_get_tokens(async_user)
    header = {"Authorization": "Bearer " + token}

    # User gets notifications list
    response = await async_client.get(
        reverse(NOTIFICATIONS_LIST_URL),
        headers=header,
    )

    # Assertions
    assert response.status_code == 200
    assert response.data.get("count") == 100
    assert response.data.get("next")
    assert not response.data.get("previous")
    results = response.data.get("results")
    pagination = settings.REST_FRAMEWORK.get("PAGE_SIZE")
    assert len(results) == pagination
    last_notifications = async_user_hundred_notifications[-pagination:][::-1]

    for i in range(pagination):
        result = results[i]
        notification = last_notifications[i]

        assert result.get("id") == notification.id
        assert result.get("created_by") == notification.created_by
        assert result.get("recipient") == async_user.id
        assert result.get("type") == notification.type
