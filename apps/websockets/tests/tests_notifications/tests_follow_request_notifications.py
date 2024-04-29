import pytest
from channels.db import database_sync_to_async
from rest_framework.reverse import reverse

from apps.profiles.tests.followers.constants import FOLLOW_URL
from apps.profiles.tests.utils import async_get_tokens
from apps.websockets.models import Notification
from apps.websockets.tests.utils import (
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
    # user_2 connecting to ws
    communicator = get_communicator(application, async_user_2_private)
    connected, subprotocol = await communicator.connect()
    assert connected

    # user log_in and follow user_2
    token = await async_get_tokens(async_user)
    header = {"Authorization": "Bearer " + token}
    await async_client.post(
        reverse(FOLLOW_URL, args=[async_user_2_private.id]),
        headers=header,
    )

    # notification check
    response_ws = await communicator.receive_json_from()
    assert response_ws.get("type") == "follow_request_notification"
    assert response_ws.get("data") == {
        'to_user_id': async_user_2_private.id,
        'to_username': async_user_2_private.username,
        'from_user_id': async_user.id,
        'from_user_image_url': async_user.image_url,
        'from_username': async_user.username,
        'follower_status': 'PENDING',
    }

    notification_object = await database_sync_to_async(
        Notification.objects.filter)(
        created_by=async_user,
        recipient=async_user_2_private,
        type=Notification.Type.FOLLOW_REQUEST,
    )
    assert database_sync_to_async(notification_object.first)

    await communicator.disconnect()
