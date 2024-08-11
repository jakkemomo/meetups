import pytest
from rest_framework.reverse import reverse

from apps.chats.tests.constants import MESSAGES_LIST_URL
from apps.profiles.tests.utils import async_get_tokens
from config import settings


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_messages_list_valid(
    async_client, async_user, event, chat_event_add_user, chat_event_add_hundred_messages
):
    # user log_in
    token = await async_get_tokens(async_user)
    header = {"Authorization": "Bearer " + token}

    # user gets messages list
    response = await async_client.get(reverse(MESSAGES_LIST_URL), headers=header)

    assert response.status_code == 200
    assert response.data.get("count") == 100
    assert response.data.get("next")
    assert response.data.get("previous") is None
    results = response.data.get("results")
    pagination = settings.REST_FRAMEWORK.get("PAGE_SIZE")
    assert len(results) == pagination
    last_messages = chat_event_add_hundred_messages[-pagination:][::-1]

    for i in range(pagination):
        result = results[i]
        message = last_messages[i]
        assert result.get("id") == message.id


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_messages_list_unauthorized(
    async_client, async_user, event, chat_event_add_user, chat_event_add_hundred_messages
):
    # user gets messages list
    response = await async_client.get(reverse(MESSAGES_LIST_URL))

    assert response.status_code == 401


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_messages_list_empty(async_client, async_user, event, chat_event_add_user):
    # user log_in
    token = await async_get_tokens(async_user)
    header = {"Authorization": "Bearer " + token}

    # user gets messages list
    response = await async_client.get(reverse(MESSAGES_LIST_URL), headers=header)

    # assertions
    assert response.status_code == 200
    assert response.data.get("count") == 0
    assert response.data.get("next") is None
    assert response.data.get("previous") is None
    assert response.data.get("results") == []
