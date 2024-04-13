import pytest
from channels.testing import WebsocketCommunicator
from rest_framework.reverse import reverse

from apps.profiles.models.followers import Follower
from apps.profiles.tests.followers.constants import FOLLOW_URL, ACCEPT_URL
from apps.profiles.tests.utils import async_get_tokens
from apps.profiles.tests.websockets.utils import (
    async_follower,
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
    data = {"Authorization": "Bearer " + token}
    await async_client.post(
        reverse(FOLLOW_URL, args=[async_user_2_private.id]),
        headers=data,
    )

    # notification check
    response_ws = await communicator.receive_json_from()
    assert response_ws.get("type") == "follow_request"
    assert response_ws.get("data") == {
        'to_user_id': async_user_2_private.id,
        'to_username': async_user_2_private.username,
        'from_user_id': async_user.id,
        'from_user_image_url': async_user.image_url,
        'from_username': async_user.username,
        'follower_status': 'PENDING',
    }

    await communicator.disconnect()
