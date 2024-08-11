import pytest
from rest_framework.reverse import reverse

from apps.chats.tests.constants import CHATS_GET_PARTICIPANTS_URL
from apps.profiles.tests.utils import async_get_tokens


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_chats_chat_event_participants_valid(
    async_client, async_user, event, chat_event_add_user, chat_event_add_message
):
    # user log_in
    token = await async_get_tokens(async_user)
    header = {"Authorization": "Bearer " + token}

    response = await async_client.get(
        reverse(CHATS_GET_PARTICIPANTS_URL, kwargs={"chat_id": event.chat.id}), headers=header
    )

    # assertions
    assert response.status_code == 200
    assert response.data.get("count") == 1
    assert response.data.get("next") is None
    assert response.data.get("previous") is None
    result = response.data.get("results")[0]
    assert result.get("id") == async_user.id
    assert result.get("username") == async_user.username
    assert result.get("image_url") == async_user.image_url


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_chats_chat_event_participants_unauthorized(async_client, async_user, event):
    response = await async_client.get(
        reverse(CHATS_GET_PARTICIPANTS_URL, kwargs={"chat_id": event.chat.id})
    )

    # assertions
    assert response.status_code == 401


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_chats_chat_event_participants_not_participants(async_client, async_user, event):
    # user log_in
    token = await async_get_tokens(async_user)
    header = {"Authorization": "Bearer " + token}

    response = await async_client.get(
        reverse(CHATS_GET_PARTICIPANTS_URL, kwargs={"chat_id": event.chat.id}), headers=header
    )

    # assertions
    assert response.status_code == 403
