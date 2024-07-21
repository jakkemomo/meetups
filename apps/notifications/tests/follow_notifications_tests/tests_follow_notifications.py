import pytest
from channels.db import database_sync_to_async
from rest_framework.reverse import reverse

from apps.profiles.models.followers import Follower
from apps.profiles.tests.followers.constants import FOLLOW_URL
from apps.profiles.tests.utils import async_get_tokens
from apps.notifications.models import Notification
from apps.notifications.tests.utils import get_communicator


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_follow_valid(
        application,
        async_client,
        async_user,
        async_user_2,
):
    # user_2 connects to ws
    communicator = get_communicator(application, async_user_2)
    connected, subprotocol = await communicator.connect()
    assert connected

    # user logs in and follows user_2
    token = await async_get_tokens(async_user)
    header = {"Authorization": "Bearer " + token}
    response = await async_client.post(
        reverse(FOLLOW_URL, args=[async_user_2.id]),
        headers=header,
    )
    assert response.status_code == 201
    assert response.data == {
        'user': async_user_2.id,
        'follower': async_user.id,
        'status': Follower.Status.ACCEPTED,
        'username': async_user.username,
        'image_url': async_user.image_url,
    }

    # notification check
    response_ws = await communicator.receive_json_from()
    assert response_ws.get("type") == "notification"
    assert response_ws.get("data") == {
        "notification_type": Notification.Type.NEW_FOLLOWER,
        'to_user_id': async_user_2.id,
        'to_username': async_user_2.username,
        'from_user_id': async_user.id,
        'from_username': async_user.username,
        'from_user_image_url': async_user.image_url,
        'follower_status': Follower.Status.ACCEPTED,
    }

    notification_object = await database_sync_to_async(
        Notification.objects.filter)(
        created_by=async_user,
        recipient=async_user_2,
        type=Notification.Type.NEW_FOLLOWER,
    )
    assert await database_sync_to_async(notification_object.first)()

    await communicator.disconnect()


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_follow_unauthorized(
        application,
        async_client,
        async_user_2,
):
    # someone follows user_2
    response = await async_client.post(
        reverse(FOLLOW_URL, args=[async_user_2.id]),
    )
    assert response.status_code == 401


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_follow_user_not_found(
        application,
        async_client,
        async_user,
):
    # user logs in and follows someone
    token = await async_get_tokens(async_user)
    header = {"Authorization": "Bearer " + token}
    response = await async_client.post(
        reverse(FOLLOW_URL, args=[1000]),
        headers=header,
    )

    assert response.status_code == 404
