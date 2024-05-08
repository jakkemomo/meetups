import pytest
from channels.db import database_sync_to_async
from rest_framework.reverse import reverse

from apps.chats.models import Message
from apps.chats.tests.constants import MESSAGES_GET_URL
from apps.profiles.tests.utils import async_get_tokens


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_message_delete_valid(
        async_client,
        async_user,
        chat_event_add_user,
        chat_event_add_message,
):
    # user log_in
    token = await async_get_tokens(async_user)
    header = {"Authorization": "Bearer " + token}

    # Delete the message
    response = await async_client.delete(
        reverse(MESSAGES_GET_URL, kwargs={"message_id": chat_event_add_message.id}),
        headers=header,
    )

    assert response.status_code == 204

    # Verify that the message is deleted
    message_object = await database_sync_to_async(Message.objects.filter)(pk=chat_event_add_message.id)
    assert not await database_sync_to_async(message_object.first)()


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_message_delete_not_participant(
        async_client,
        async_user,
        chat_event_add_message,
):
    # user log_in
    token = await async_get_tokens(async_user)
    header = {"Authorization": "Bearer " + token}

    # Delete the message
    response = await async_client.delete(
        reverse(MESSAGES_GET_URL, kwargs={"message_id": chat_event_add_message.id}),
        headers=header,
    )

    assert response.status_code == 403


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_message_delete_unauthorized(
        async_client,
        async_user,
        chat_event_add_message,
):
    # Delete the message
    response = await async_client.delete(
        reverse(MESSAGES_GET_URL, kwargs={"message_id": chat_event_add_message.id}),
    )

    assert response.status_code == 401


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_message_delete_not_found(
        async_client,
        async_user,
        event,
):
    # user log_in
    token = await async_get_tokens(async_user)
    header = {"Authorization": "Bearer " + token}

    # Delete the message
    response = await async_client.delete(
        reverse(MESSAGES_GET_URL, kwargs={"message_id": 100}),
        headers=header,
    )

    assert response.status_code == 404
