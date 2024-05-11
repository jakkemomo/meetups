import pytest
from rest_framework.reverse import reverse

from apps.chats.tests.constants import MESSAGES_GET_URL
from apps.profiles.tests.utils import async_get_tokens


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_messages_get_valid(
        async_client,
        async_user,
        event,
        chat_event_add_user,
        chat_event_add_message,
):
    # user log_in
    token = await async_get_tokens(async_user)
    header = {"Authorization": "Bearer " + token}

    # user gets messages list
    response = await async_client.get(
        reverse(MESSAGES_GET_URL, kwargs={"message_id": chat_event_add_message.id}),
        headers=header,
    )

    assert response.status_code == 200
    assert response.data.get("id") == chat_event_add_message.id
    assert response.data.get("created_by") == async_user.id
    assert response.data.get("chat") == event.chat.id
    assert response.data.get("message_text") == chat_event_add_message.message_text
    assert response.data.get("image_url") == event.image_url


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_messages_get_not_participant(
        async_client,
        async_user,
        event,
        chat_event_add_message,
):
    # user log_in
    token = await async_get_tokens(async_user)
    header = {"Authorization": "Bearer " + token}

    # user gets messages list
    response = await async_client.get(
        reverse(MESSAGES_GET_URL, kwargs={"message_id": chat_event_add_message.id}),
        headers=header,
    )

    assert response.status_code == 403


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_messages_get_unauthorized(
        async_client,
        async_user,
        event,
        chat_event_add_message,
):
    # user gets messages list
    response = await async_client.get(
        reverse(MESSAGES_GET_URL, kwargs={"message_id": chat_event_add_message.id}),
    )

    assert response.status_code == 401


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_messages_get_nonexistent_message(
        async_client,
        async_user,
):
    # user log_in
    token = await async_get_tokens(async_user)
    header = {"Authorization": "Bearer " + token}

    # user gets messages list
    response = await async_client.get(
        reverse(MESSAGES_GET_URL, kwargs={"message_id": 9999999}),
        headers=header,
    )

    assert response.status_code == 404
