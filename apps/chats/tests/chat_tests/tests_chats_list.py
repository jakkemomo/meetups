from collections import OrderedDict
import pytest
from rest_framework.reverse import reverse

from apps.chats.models import Chat
from apps.chats.tests.constants import CHATS_LIST_URL
from apps.profiles.tests.utils import async_get_tokens


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_chats_list_valid(
    async_client,
    async_user,
    async_user_2,
    event,
    chat_event_add_user,
    chat_direct_user_user_2,
    chat_event_add_message,
):
    # User log in
    token = await async_get_tokens(async_user)
    header = {"Authorization": "Bearer " + token}

    # User chats_list
    response = await async_client.get(reverse(CHATS_LIST_URL), headers=header)

    # Assertions
    assert response.status_code == 200
    assert response.data.get("count") == 2
    assert response.data.get("next") is None
    assert response.data.get("previous") is None

    results = response.data.get("results")

    assert results[0]["id"] == event.chat.id
    assert results[0]["name"] == event.name
    assert results[0]["image_url"] == event.image_url
    assert results[0]["type"] == Chat.Type.EVENT
    assert results[0]["last_message_text"] == chat_event_add_message.message_text
    assert results[0]["last_message_is_owner"] is True
    assert results[0]["last_message_created_at"] is not None  # Check that the value is not None

    assert results[1]["id"] == chat_direct_user_user_2.id
    assert results[1]["name"] == async_user_2.username
    assert results[1]["image_url"] == async_user_2.image_url
    assert results[1]["type"] == Chat.Type.DIRECT
    assert results[1]["last_message_text"] is None
    assert results[1]["last_message_is_owner"] is False
    assert results[1]["last_message_created_at"] is None  # Should be None for this chat


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_chats_list_unauthorized(async_client, async_user, event, chat_event_add_user):
    # User chats_list
    response = await async_client.get(reverse(CHATS_LIST_URL))

    # Assertions
    assert response.status_code == 401


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_chats_list_empty(
    async_client, async_user, async_user_2, event, chat_event_add_user_2
):
    # User log in
    token = await async_get_tokens(async_user)
    header = {"Authorization": "Bearer " + token}

    # User chats_list
    response = await async_client.get(reverse(CHATS_LIST_URL), headers=header)

    # Assertions
    assert response.status_code == 200
    assert response.data.get("count") == 0
    assert response.data.get("next") is None
    assert response.data.get("previous") is None
    assert response.data.get("results") == []
