import json

import pytest
from rest_framework.reverse import reverse

from apps.chats.tests.constants import MESSAGES_GET_URL
from apps.profiles.tests.utils import async_get_tokens


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_message_partial_update_valid(
    async_client, async_user, event, chat_event_add_user, chat_event_add_message
):
    # user log_in
    token = await async_get_tokens(async_user)
    header = {"Authorization": "Bearer " + token}

    # New message data for partial update
    new_message_text = "Updated message text"

    # Partially update the message
    response = await async_client.patch(
        reverse(MESSAGES_GET_URL, kwargs={"message_id": chat_event_add_message.id}),
        data={"message_text": new_message_text},
        headers=header,
        content_type="application/json",
    )

    assert response.status_code == 200
    assert response.data.get("message_text") == new_message_text
    assert response.data.get("id") == chat_event_add_message.id


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_message_change_not_participant(async_client, async_user, chat_event_add_message):
    # user log_in
    token = await async_get_tokens(async_user)
    header = {"Authorization": "Bearer " + token}

    # New message data for partial update
    new_message_text = "Updated message text"

    # Partially update the message
    response = await async_client.patch(
        reverse(MESSAGES_GET_URL, kwargs={"message_id": chat_event_add_message.id}),
        data={"message_text": new_message_text},
        headers=header,
        content_type="application/json",
    )

    assert response.status_code == 403


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_message_change_unauthorized(async_client, async_user, chat_event_add_message):
    # New message data for partial update
    new_message_text = "Updated message text"

    # Partially update the message
    response = await async_client.patch(
        reverse(MESSAGES_GET_URL, kwargs={"message_id": chat_event_add_message.id}),
        data={"message_text": new_message_text},
        content_type="application/json",
    )

    assert response.status_code == 401


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_message_change_not_found(async_client, async_user, event):
    # user log_in
    token = await async_get_tokens(async_user)
    header = {"Authorization": "Bearer " + token}

    # New message data for partial update
    new_message_text = "Updated message text"

    # Partially update the message
    response = await async_client.patch(
        reverse(MESSAGES_GET_URL, kwargs={"message_id": 1000}),
        data={"message_text": new_message_text},
        headers=header,
        content_type="application/json",
    )

    assert response.status_code == 404
