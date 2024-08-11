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
    # user log_in
    token = await async_get_tokens(async_user)
    header = {"Authorization": "Bearer " + token}

    # user chats_list
    response = await async_client.get(reverse(CHATS_LIST_URL), headers=header)

    # assertions
    assert response.status_code == 200
    assert response.data.get("count") == 2
    assert response.data.get("next") is None
    assert response.data.get("previous") is None
    assert response.data.get("results") == [
        OrderedDict(
            [
                ("id", event.chat.id),
                ("name", event.name),
                ("image_url", event.image_url),
                ("type", Chat.Type.EVENT),
                ("last_message_text", chat_event_add_message.message_text),
                ("last_message_is_owner", True),
            ]
        ),
        OrderedDict(
            [
                ("id", chat_direct_user_user_2.id),
                ("name", async_user_2.username),
                ("image_url", async_user_2.image_url),
                ("type", Chat.Type.DIRECT),
                ("last_message_text", None),
                ("last_message_is_owner", False),
            ]
        ),
    ]


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_chats_list_unauthorized(async_client, async_user, event, chat_event_add_user):
    # user chats_list
    response = await async_client.get(reverse(CHATS_LIST_URL))

    # assertions
    assert response.status_code == 401


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_chats_list_empty(
    async_client, async_user, async_user_2, event, chat_event_add_user_2
):
    # user log_in
    token = await async_get_tokens(async_user)
    header = {"Authorization": "Bearer " + token}

    # user chats_list
    response = await async_client.get(reverse(CHATS_LIST_URL), headers=header)

    # assertions
    assert response.status_code == 200
    assert response.data.get("count") == 0
    assert response.data.get("next") is None
    assert response.data.get("previous") is None
    assert response.data.get("results") == []
