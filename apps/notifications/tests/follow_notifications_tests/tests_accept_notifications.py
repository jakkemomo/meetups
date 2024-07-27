import pytest
from channels.db import database_sync_to_async
from rest_framework.reverse import reverse

from apps.profiles.models.followers import Follower
from apps.profiles.tests.followers.constants import ACCEPT_URL
from apps.profiles.tests.utils import async_get_tokens
from apps.notifications.models import Notification
from apps.notifications.tests.utils import get_communicator


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_accept_valid(
        application,
        async_client,
        async_user_private,
        async_user_2_private,
        async_follower_user_pending_private,
):
    # user connects to ws
    communicator = get_communicator(application, async_user_private)
    connected, subprotocol = await communicator.connect()
    assert connected

    # user_2 logs in and accepts user's request
    token = await async_get_tokens(async_user_2_private)
    header = {"Authorization": "Bearer " + token}
    response = await async_client.post(
        reverse(ACCEPT_URL, args=[async_user_private.id]),
        headers=header,
    )

    assert response.status_code == 200
    assert response.data == {
        'user': async_user_2_private.id,
        'follower': async_user_private.id,
        'status': Follower.Status.ACCEPTED,
        'username': async_user_private.username,
        'image_url': async_user_private.image_url,
    }

    # notification check
    response_ws = await communicator.receive_json_from()
    assert response_ws.get("type") == "notification"
    assert response_ws.get("data") == {
        "notification_type": Notification.Type.ACCEPTED_FOLLOW_REQUEST,
        'to_user_id': async_user_private.id,
        'to_username': async_user_private.username,
        'from_user_id': async_user_2_private.id,
        'from_username': async_user_2_private.username,
        'from_user_image_url': async_user_2_private.image_url,
        'additional_data': {
            "follower_status": Follower.Status.ACCEPTED,
        }
    }

    notification_object = await database_sync_to_async(Notification.objects.filter)(
        created_by=async_user_2_private,
        recipient=async_user_private,
        type=Notification.Type.ACCEPTED_FOLLOW_REQUEST,
    )
    assert await database_sync_to_async(notification_object.first)()

    await communicator.disconnect()


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_accept_unauthorized(
        application,
        async_client,
        async_user_private,
        async_follower_user_pending_private,
):
    # someone accepts user's request
    response = await async_client.post(
        reverse(ACCEPT_URL, args=[async_user_private.id]),
    )

    assert response.status_code == 401


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_accept_request_not_found(
        application,
        async_client,
        async_user_private,
        async_user_2_private,
):
    # user connects to ws
    communicator = get_communicator(application, async_user_private)
    connected, subprotocol = await communicator.connect()
    assert connected

    # user_2 logs in and accepts user's request (there is no request)
    token = await async_get_tokens(async_user_2_private)
    header = {"Authorization": "Bearer " + token}
    response = await async_client.post(
        reverse(ACCEPT_URL, args=[async_user_private.id]),
        headers=header,
    )

    assert response.status_code == 404

    await communicator.disconnect()


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_accept_user_not_found(
        application,
        async_client,
        async_user,
):
    # user logs in and accepts someone
    token = await async_get_tokens(async_user)
    header = {"Authorization": "Bearer " + token}
    response = await async_client.post(
        reverse(ACCEPT_URL, args=[1000]),
        headers=header,
    )

    assert response.status_code == 404
