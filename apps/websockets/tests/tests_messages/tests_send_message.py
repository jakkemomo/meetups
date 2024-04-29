import pytest
from channels.db import database_sync_to_async
from rest_framework.reverse import reverse

from apps.websockets.models import Message
from apps.websockets.tests.constants import SEND_MESSAGE_URL
from apps.profiles.tests.utils import async_get_tokens
from apps.websockets.tests.utils import (
    get_chat_communicator,
    get_wrong_chat_communicator,
)


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_send_message_valid(
        application,
        async_client,
        async_user,
        async_user_2,
        chat_with_users,
):
    # user log_in
    token = await async_get_tokens(async_user)
    header = {"Authorization": "Bearer " + token}

    # user connecting to ws
    communicator = get_chat_communicator(application, async_user, chat_with_users)
    connected, subprotocol = await communicator.connect()
    assert connected

    # user_2 connecting to ws
    communicator_2 = get_chat_communicator(application, async_user_2, chat_with_users)
    connected, subprotocol = await communicator_2.connect()
    assert connected

    # sends message to chat with id = 1
    data = {"message_text": "Hello, World!"}
    await async_client.post(
        reverse(SEND_MESSAGE_URL, args=[chat_with_users.id]),
        headers=header,
        data=data,
    )

    # both users checks message
    response_ws_1 = await communicator.receive_json_from()
    response_ws_2 = await communicator_2.receive_json_from()
    assert response_ws_1 == response_ws_2
    assert response_ws_1.get("type") == "chat_message"
    assert response_ws_1.get("data") == {
        "to_chat_id": chat_with_users.id,
        "from_user_id": async_user.id,
        "message_text": data.get("message_text"),
    }
    message_object = await database_sync_to_async(Message.objects.filter)(
        created_by=async_user,
        chat=chat_with_users,
        message_text=data.get("message_text"),
    )
    assert database_sync_to_async(message_object.first)

    await communicator.disconnect()
    await communicator_2.disconnect()


# @pytest.mark.django_db(transaction=True)
# @pytest.mark.asyncio
# async def test_send_message_chat_not_found(
#         application,
#         async_client,
#         async_user,
# ):
#     # user connecting to ws
#     communicator = get_wrong_chat_communicator(application, async_user)
#     connected, subprotocol = await communicator.connect()
#     assert not connected
#
#
# @pytest.mark.django_db(transaction=True)
# @pytest.mark.asyncio
# async def test_send_message_not_participant(
#         application,
#         async_client,
#         async_user,
#         event,
# ):
#     # user connecting to ws
#     communicator = get_chat_communicator(application, async_user, event)
#     connected, subprotocol = await communicator.connect()
#     assert not connected
