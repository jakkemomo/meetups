import pytest
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
async def test_follow_valid(
        application,
        async_client,
        async_user,
        async_user_2,
        city,
):
    async_user_2 = await async_user_2
    async_user = await async_user
    async_client = await async_client

    # user_2 connecting to ws
    communicator = get_communicator(application, async_user_2)
    connected, subprotocol = await communicator.connect()
    assert connected

    # user log_in and follow user_2
    token = await async_get_tokens(async_user)
    data = {"Authorization": "Bearer " + token}
    await async_client.post(
        reverse(FOLLOW_URL, args=[async_user_2.id]),
        headers=data,
    )

    # notification check
    response_ws = await communicator.receive_json_from()
    assert response_ws == {
        "event": f"User {async_user.id} followed user {async_user_2.id}",
        "from_user": async_user.id, "type": "follow",
    }
    await communicator.disconnect()
