import asyncio

import pytest
from channels.db import database_sync_to_async
from rest_framework.reverse import reverse

from apps.chats.models import Message
from apps.chats.tests.constants import CHATS_SEND_MESSAGE_URL
from apps.notifications.models import Notification
from apps.profiles.tests.utils import async_get_tokens
from apps.notifications.tests.utils import (
    get_chat_communicator,
    get_wrong_chat_communicator,
    get_communicator,
)


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_send_message_valid(
        application,
        async_client,
        async_user,
        async_user_2,
        event_chat_with_users,
):
    # user log_in
    token = await async_get_tokens(async_user)
    header = {"Authorization": "Bearer " + token}

    # user connects to ws
    message_communicator = get_chat_communicator(
        application,
        async_user,
        event_chat_with_users
    )
    connected, subprotocol = await message_communicator.connect()
    assert connected

    # user_2 connects to ws
    message_communicator_2 = get_chat_communicator(
        application,
        async_user_2,
        event_chat_with_users
    )
    connected, subprotocol = await message_communicator_2.connect()
    assert connected

    notification_communicator_2 = get_communicator(
        application,
        async_user_2
    )
    connected, subprotocol = await notification_communicator_2.connect()
    assert connected

    # user sends message to chat
    data = {"message_text": "Hello, World!"}
    await async_client.post(
        reverse(CHATS_SEND_MESSAGE_URL, args=[event_chat_with_users.id]),
        headers=header,
        data=data,
    )

    # both users checks message
    response_ws_1 = await message_communicator.receive_json_from()
    response_ws_2 = await message_communicator_2.receive_json_from()
    assert response_ws_1 == response_ws_2
    assert response_ws_1.get("type") == "chat_message"
    assert response_ws_1.get("data") == {
        "to_chat_id": event_chat_with_users.id,
        "from_user_id": async_user.id,
        "message_text": data.get("message_text"),
    }
    message_object = await database_sync_to_async(Message.objects.filter)(
        created_by=async_user,
        chat=event_chat_with_users,
        message_text=data.get("message_text"),
    )
    message_object = await database_sync_to_async(message_object.first)()
    assert message_object

    # notifications check
    notifications_response_ws_2 = await notification_communicator_2.receive_json_from()
    assert notifications_response_ws_2.get("data") == {
        'additional_data': {'message_text': message_object.message_text},
        'from_user_id': async_user.id,
        'from_user_image_url': async_user.image_url,
        'from_username': async_user.username,
        'notification_type': Notification.Type.NEW_MESSAGE,
        'to_user_id': async_user_2.id,
        'to_username': async_user_2.username
    }

    await asyncio.gather(
        message_communicator.disconnect(),
        message_communicator_2.disconnect(),
    )


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_send_message_twice_valid(
        application,
        async_client,
        async_user,
        async_user_2,
        event_chat_with_users,
):
    # user log_in
    token = await async_get_tokens(async_user)
    header = {"Authorization": "Bearer " + token}

    # user_2 log_in
    token_2 = await async_get_tokens(async_user_2)
    header_2 = {"Authorization": "Bearer " + token_2}

    # user connects to ws
    message_communicator_1 = get_chat_communicator(application, async_user,
                                                   event_chat_with_users)
    connected, subprotocol = await message_communicator_1.connect()
    assert connected

    notification_communicator_1 = get_communicator(
        application,
        async_user
    )
    connected, subprotocol = await notification_communicator_1.connect()
    assert connected

    # user_2 connects to ws
    message_communicator_2 = get_chat_communicator(application, async_user_2,
                                                   event_chat_with_users)
    connected, subprotocol = await message_communicator_2.connect()
    assert connected

    notification_communicator_2 = get_communicator(
        application,
        async_user_2
    )
    connected, subprotocol = await notification_communicator_2.connect()
    assert connected

    # user sends message to chat
    data_1 = {"message_text": "First message"}
    await async_client.post(
        reverse(CHATS_SEND_MESSAGE_URL, args=[event_chat_with_users.id]),
        headers=header,
        data=data_1,
    )

    # user_2 sends message to chat
    data_2 = {"message_text": "Second message"}
    await async_client.post(
        reverse(CHATS_SEND_MESSAGE_URL, args=[event_chat_with_users.id]),
        headers=header_2,
        data=data_2,
    )

    # user_2 checks notification of the first message
    notifications_response_ws_2 = await notification_communicator_2.receive_json_from()
    assert notifications_response_ws_2.get("data") == {
        'additional_data': {'message_text': data_1.get("message_text")},
        'from_user_id': async_user.id,
        'from_user_image_url': async_user.image_url,
        'from_username': async_user.username,
        'notification_type': Notification.Type.NEW_MESSAGE,
        'to_user_id': async_user_2.id,
        'to_username': async_user_2.username
    }

    # user checks notification of the second message
    notifications_response_ws = await notification_communicator_1.receive_json_from()
    assert notifications_response_ws.get("data") == {
        'additional_data': {'message_text': data_2.get("message_text")},
        'from_user_id': async_user_2.id,
        'from_user_image_url': async_user_2.image_url,
        'from_username': async_user_2.username,
        'notification_type': Notification.Type.NEW_MESSAGE,
        'to_user_id': async_user.id,
        'to_username': async_user.username
    }

    # both users check the first message
    response_ws = await message_communicator_1.receive_json_from()
    response_ws_2 = await message_communicator_2.receive_json_from()
    assert response_ws == response_ws_2
    assert response_ws.get("type") == "chat_message"
    assert response_ws.get("data") == {
        "to_chat_id": event_chat_with_users.id,
        "from_user_id": async_user.id,
        "message_text": data_1.get("message_text"),
    }
    message_object = await database_sync_to_async(Message.objects.filter)(
        created_by=async_user,
        chat=event_chat_with_users,
        message_text=data_1.get("message_text"),
    )
    message_object = await database_sync_to_async(message_object.first)()
    assert message_object

    # both users checks the second message
    response_ws = await message_communicator_1.receive_json_from()
    response_ws_2 = await message_communicator_2.receive_json_from()
    assert response_ws == response_ws_2
    assert response_ws.get("type") == "chat_message"
    assert response_ws.get("data") == {
        "to_chat_id": event_chat_with_users.id,
        "from_user_id": async_user_2.id,
        "message_text": data_2.get("message_text"),
    }
    message_object_2 = await database_sync_to_async(Message.objects.filter)(
        created_by=async_user_2,
        chat=event_chat_with_users,
        message_text=data_2.get("message_text"),
    )
    message_object_2 = await database_sync_to_async(message_object_2.first)()
    assert message_object_2

    assert message_object.id < message_object_2.id
    assert message_object.created_at < message_object_2.created_at

    await asyncio.gather(
        message_communicator_1.disconnect(),
        message_communicator_2.disconnect(),
    )


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_send_message_chat_not_found(
        application,
        async_client,
        async_user,
):
    # user connects to ws
    communicator = get_wrong_chat_communicator(application, async_user)
    connected, subprotocol = await communicator.connect()
    assert not connected


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_send_message_not_participant(
        application,
        async_client,
        async_user,
        event,
):
    # user connects to ws
    communicator = get_chat_communicator(application, async_user, event)
    connected, subprotocol = await communicator.connect()
    assert not connected


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_send_message_too_long(
        application,
        async_client,
        async_user,
        event_chat_with_users,
):
    # user log_in
    token = await async_get_tokens(async_user)
    header = {"Authorization": "Bearer " + token}

    # user connects to ws
    communicator = get_chat_communicator(application, async_user,
                                         event_chat_with_users)
    connected, subprotocol = await communicator.connect()
    assert connected

    # user sends a too long message to chat
    data = {"message_text": "A" * 1000}
    response = await async_client.post(
        reverse(CHATS_SEND_MESSAGE_URL, args=[event_chat_with_users.id]),
        headers=header,
        data=data,
    )

    # Check the HTTP response
    assert response.status_code == 400
    assert response.json() == {
        'message_text': ['Ensure this field has no more than 528 characters.']}

    await communicator.disconnect()


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_concurrent_connections(
        application,
        async_client,
        async_user,
        async_user_2,
        event_chat_with_users,
):
    # user log_in
    token = await async_get_tokens(async_user)
    header = {"Authorization": "Bearer " + token}

    # user_2 log_in
    token_2 = await async_get_tokens(async_user_2)
    header_2 = {"Authorization": "Bearer " + token_2}

    # user and user_2 connect to ws concurrently
    message_communicator_1 = get_chat_communicator(application, async_user,
                                                   event_chat_with_users)
    notification_communicator_1 = get_communicator(
        application,
        async_user
    )
    message_communicator_2 = get_chat_communicator(application, async_user_2,
                                                   event_chat_with_users)
    notification_communicator_2 = get_communicator(
        application,
        async_user_2
    )
    connected, connected_2, connected_3, connected_4 = await asyncio.gather(
        message_communicator_1.connect(),
        message_communicator_2.connect(),
        notification_communicator_1.connect(),
        notification_communicator_2.connect(),
    )
    assert all((connected[0], connected_2[0], connected_3[0], connected_4[0]))

    # user and user_2 send messages to chat concurrently
    data_1 = {"message_text": "First message"}
    data_2 = {"message_text": "Second message"}
    await asyncio.gather(
        async_client.post(
            reverse(CHATS_SEND_MESSAGE_URL, args=[event_chat_with_users.id]),
            headers=header, data=data_1),
        async_client.post(
            reverse(CHATS_SEND_MESSAGE_URL, args=[event_chat_with_users.id]),
            headers=header_2, data=data_2),
    )

    # both users check notifications concurrently
    notifications_response_ws_1, notifications_response_ws_2 = await asyncio.gather(
        notification_communicator_1.receive_json_from(),
        notification_communicator_2.receive_json_from(),
    )

    assert notifications_response_ws_1.get("data") == {
        'additional_data': {'message_text': data_2.get("message_text")},
        'from_user_id': async_user_2.id,
        'from_user_image_url': async_user_2.image_url,
        'from_username': async_user_2.username,
        'notification_type': Notification.Type.NEW_MESSAGE,
        'to_user_id': async_user.id,
        'to_username': async_user.username
    }

    assert notifications_response_ws_2.get("data") == {
        'additional_data': {'message_text': data_1.get("message_text")},
        'from_user_id': async_user.id,
        'from_user_image_url': async_user.image_url,
        'from_username': async_user.username,
        'notification_type': Notification.Type.NEW_MESSAGE,
        'to_user_id': async_user_2.id,
        'to_username': async_user_2.username
    }

    # both users check the first message concurrently
    response_ws, response_ws_2 = await asyncio.gather(
        message_communicator_1.receive_json_from(),
        message_communicator_2.receive_json_from(),
    )
    assert response_ws.get("type") == response_ws_2.get(
        "type") == "chat_message"
    assert response_ws.get("data") == response_ws_2.get("data") == {
        "to_chat_id": event_chat_with_users.id,
        "from_user_id": async_user.id,
        "message_text": data_1.get("message_text"),
    }

    message_object = await database_sync_to_async(Message.objects.filter)(
        created_by=async_user,
        chat=event_chat_with_users,
        message_text=data_1.get("message_text"),
    )
    message_object = await database_sync_to_async(message_object.first)()
    assert message_object

    # both users check the second message concurrently
    response_ws, response_ws_2 = await asyncio.gather(
        message_communicator_1.receive_json_from(),
        message_communicator_2.receive_json_from(),
    )
    assert response_ws.get("type") == response_ws_2.get(
        "type") == "chat_message"
    assert response_ws.get("data") == response_ws_2.get("data") == {
        "to_chat_id": event_chat_with_users.id,
        "from_user_id": async_user_2.id,
        "message_text": data_2.get("message_text"),
    }

    message_object_2 = await database_sync_to_async(Message.objects.filter)(
        created_by=async_user_2,
        chat=event_chat_with_users,
        message_text=data_2.get("message_text"),
    )
    message_object_2 = await database_sync_to_async(message_object_2.first)()
    assert message_object_2

    assert message_object.id < message_object_2.id
    assert message_object.created_at < message_object_2.created_at

    await asyncio.gather(
        message_communicator_1.disconnect(),
        message_communicator_2.disconnect(),
    )


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_send_message_false_preferences(
        application,
        async_client,
        async_user,
        async_user_2,
        event_chat_with_users,
        async_user_2_false_all_preferences,
):
    # user log_in
    token = await async_get_tokens(async_user)
    header = {"Authorization": "Bearer " + token}

    # user connects to ws
    message_communicator = get_chat_communicator(
        application,
        async_user,
        event_chat_with_users
    )
    connected, subprotocol = await message_communicator.connect()
    assert connected

    # user_2 connects to ws
    message_communicator_2 = get_chat_communicator(
        application,
        async_user_2,
        event_chat_with_users
    )
    connected, subprotocol = await message_communicator_2.connect()
    assert connected

    notification_communicator_2 = get_communicator(
        application,
        async_user_2
    )
    connected, subprotocol = await notification_communicator_2.connect()
    assert connected

    # user sends message to chat
    data = {"message_text": "Hello, World!"}
    await async_client.post(
        reverse(CHATS_SEND_MESSAGE_URL, args=[event_chat_with_users.id]),
        headers=header,
        data=data,
    )

    # both users checks message
    response_ws_1 = await message_communicator.receive_json_from()
    response_ws_2 = await message_communicator_2.receive_json_from()
    assert response_ws_1 == response_ws_2
    assert response_ws_1.get("type") == "chat_message"
    assert response_ws_1.get("data") == {
        "to_chat_id": event_chat_with_users.id,
        "from_user_id": async_user.id,
        "message_text": data.get("message_text"),
    }
    message_object = await database_sync_to_async(Message.objects.filter)(
        created_by=async_user,
        chat=event_chat_with_users,
        message_text=data.get("message_text"),
    )
    message_object = await database_sync_to_async(message_object.first)()
    assert message_object

    # notifications check
    try:
        await notification_communicator_2.receive_json_from()
    except Exception as exc:
        assert isinstance(exc, TimeoutError)

    await asyncio.gather(
        message_communicator.disconnect(),
        message_communicator_2.disconnect(),
    )
