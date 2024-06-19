import pytest
from channels.db import database_sync_to_async
from rest_framework.reverse import reverse

from apps.profiles.models.followers import Follower
from apps.profiles.tests.followers.constants import FOLLOW_URL
from apps.profiles.tests.utils import async_get_tokens
from apps.notifications.models import Notification
from apps.notifications.tests.utils import (
    get_communicator,
)


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_follow_request_valid(
        application,
        async_client,
        async_user,
        async_user_2_private,
):
    # user_2 connects to ws
    communicator = get_communicator(application, async_user_2_private)
    connected, subprotocol = await communicator.connect()
    assert connected

    # user logs in and follows user_2
    token = await async_get_tokens(async_user)
    header = {"Authorization": "Bearer " + token}
    response = await async_client.post(
        reverse(FOLLOW_URL, args=[async_user_2_private.id]),
        headers=header,
    )

    assert response.status_code == 201
    assert response.data == {
        'user': async_user_2_private.id,
        'follower': async_user.id,
        'status': Follower.Status.PENDING
    }

    # notification check
    response_ws = await communicator.receive_json_from()
    assert response_ws.get("type") == "notification"
    assert response_ws.get("data") == {
        "notification_type": Notification.Type.NEW_FOLLOW_REQUEST,
        'to_user_id': async_user_2_private.id,
        'to_username': async_user_2_private.username,
        'from_user_id': async_user.id,
        'from_user_image_url': async_user.image_url,
        'from_username': async_user.username,
        'additional_data': {
            "follower_status": Follower.Status.PENDING,
        }
    }

    notification_object = await database_sync_to_async(
        Notification.objects.filter)(
        created_by=async_user,
        recipient=async_user_2_private,
        type=Notification.Type.NEW_FOLLOW_REQUEST,
    )
    assert await database_sync_to_async(notification_object.first)()

    await communicator.disconnect()


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_follow_request_unauthorized(
        application,
        async_client,
        async_user_2_private,
):
    # someone follows user_2
    response = await async_client.post(
        reverse(FOLLOW_URL, args=[async_user_2_private.id]),
    )

    assert response.status_code == 401


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_follow_request_valid_base(
        application,
        async_client,
        async_user,
        async_user_2_private,
):
    # user logs in and follows someone
    token = await async_get_tokens(async_user)
    header = {"Authorization": "Bearer " + token}
    response = await async_client.post(
        reverse(FOLLOW_URL, args=[1000]),
        headers=header,
    )

    assert response.status_code == 404
