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
    data = {"Authorization": "Bearer " + token}
    await async_client.post(
        reverse(ACCEPT_URL, args=[async_user_private.id]),
        headers=data,
    )

    # notification check
    response_ws = await communicator.receive_json_from()
    assert response_ws == {
        "event": f"User {async_user_2_private.id} accepted follow request of user {async_user_private.id}",
        "from_user": async_user_2_private.id,
        "type": "accept_follow_request"
    }
    await communicator.disconnect()