import pytest
from channels.db import database_sync_to_async
from rest_framework.reverse import reverse

from apps.profiles.models.followers import Follower
from apps.profiles.tests.followers.constants import ACCEPT_URL
from apps.profiles.tests.utils import async_get_tokens
from apps.websockets.models import Notification
from apps.websockets.tests.utils import (
    async_follower,
    get_communicator,
)


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_accept_valid(
        application,
        async_client,
        async_user_private,
        async_user_2_private,
):
    # create follow request
    await async_follower(
        user=async_user_2_private,
        follower=async_user_private,
        status=Follower.Status.PENDING
    )

    # user connecting to ws
    communicator = get_communicator(application, async_user_private)
    connected, subprotocol = await communicator.connect()
    assert connected

    # user_2 log_in and accept user's request
    token = await async_get_tokens(async_user_2_private)
    header = {"Authorization": "Bearer " + token}
    await async_client.post(
        reverse(ACCEPT_URL, args=[async_user_private.id]),
        headers=header,
    )

    # notification check
    response_ws = await communicator.receive_json_from()
    assert response_ws.get("type") == "accept_follow_request_notification"
    assert response_ws.get("data") == {
        'to_user_id': async_user_private.id,
        'to_username': async_user_private.username,
        'from_user_id': async_user_2_private.id,
        'from_username': async_user_2_private.username,
        'from_user_image_url': async_user_2_private.image_url,
        'follower_status': 'ACCEPTED',
    }

    notification_object = await database_sync_to_async(Notification.objects.filter)(
        created_by=async_user_2_private,
        recipient=async_user_private,
        type=Notification.Type.ACCEPT,
    )
    assert database_sync_to_async(notification_object.first)

    await communicator.disconnect()
