import pytest
from rest_framework.reverse import reverse

from apps.chats.models import Chat
from apps.chats.tests.constants import CHATS_GET_EVENT_URL
from apps.profiles.tests.utils import async_get_tokens


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_chats_get_chat_event_valid(
        async_client,
        async_user,
        event,
        chat_event_add_user,
):
    # user log_in
    token = await async_get_tokens(async_user)
    header = {"Authorization": "Bearer " + token}

    response = await async_client.get(
        reverse(CHATS_GET_EVENT_URL, kwargs={"chat_id": event.chat.id}),
        headers=header,
    )

    # assertions
    assert response.status_code == 200
    assert response.data.get("id") == event.chat.id
    assert response.data.get("name") == event.name
    assert response.data.get("image_url") == event.image_url
    assert response.data.get("type") == Chat.Type.EVENT


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_chats_get_chat_event_unauthorized(
        async_client,
        async_user,
        event,
        chat_event_add_user,
):
    response = await async_client.get(
        reverse(CHATS_GET_EVENT_URL, kwargs={"chat_id": event.chat.id}),
    )

    # assertions
    assert response.status_code == 401


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_chats_get_chat_event_not_participant(
        async_client,
        async_user,
        event,
):
    # user log_in
    token = await async_get_tokens(async_user)
    header = {"Authorization": "Bearer " + token}

    response = await async_client.get(
        reverse(CHATS_GET_EVENT_URL, kwargs={"chat_id": event.chat.id}),
        headers=header,
    )

    # assertions
    assert response.status_code == 403
