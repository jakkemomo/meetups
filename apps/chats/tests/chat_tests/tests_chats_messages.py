import pytest
from rest_framework.reverse import reverse

from apps.chats.tests.constants import CHATS_GET_MESSAGES_URL
from apps.profiles.tests.utils import async_get_tokens
from config import settings


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_chats_chat_event_messages_valid(
    async_client, async_user, event, chat_event_add_user, chat_event_add_hundred_messages
):
    # user log_in
    token = await async_get_tokens(async_user)
    header = {"Authorization": "Bearer " + token}

    # user gets messages list
    response = await async_client.get(
        reverse(CHATS_GET_MESSAGES_URL, kwargs={"chat_id": event.chat.id}), headers=header
    )

    pagination = settings.REST_FRAMEWORK.get("PAGE_SIZE")

    # assertions
    assert response.status_code == 200
    assert response.data.get("count") == 100
    assert response.data.get("next")
    assert response.data.get("previous") is None
    results = response.data.get("results")
    assert len(results) == pagination

    last_messages = chat_event_add_hundred_messages[-pagination:][::-1]

    for i in range(pagination):
        result = results[i]
        message = last_messages[i]
        assert result.get("id") == message.id
        assert result.get("created_by") == async_user.id
        assert result.get("chat") == event.chat.id
        assert result.get("message_text") == message.message_text
        assert result.get("image_url") == async_user.image_url


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_chats_chat_event_messages_empty(
    async_client, async_user, event, chat_event_add_user
):
    # user log_in
    token = await async_get_tokens(async_user)
    header = {"Authorization": "Bearer " + token}

    # user gets messages list
    response = await async_client.get(
        reverse(CHATS_GET_MESSAGES_URL, kwargs={"chat_id": event.chat.id}), headers=header
    )

    # assertions
    assert response.status_code == 200
    assert response.data.get("count") == 0
    assert response.data.get("next") is None
    assert response.data.get("previous") is None
    assert response.data.get("results") == []


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_chats_chat_event_messages_unauthorized(async_client, async_user, event):
    # user gets messages list
    response = await async_client.get(
        reverse(CHATS_GET_MESSAGES_URL, kwargs={"chat_id": event.chat.id})
    )

    # assertions
    assert response.status_code == 401


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_chats_chat_event_messages_not_participants(async_client, async_user, event):
    # user log_in
    token = await async_get_tokens(async_user)
    header = {"Authorization": "Bearer " + token}

    # user gets messages list
    response = await async_client.get(
        reverse(CHATS_GET_MESSAGES_URL, kwargs={"chat_id": event.chat.id}), headers=header
    )

    # assertions
    assert response.status_code == 403
