import pytest
from rest_framework.reverse import reverse

from apps.chats.models import Chat
from apps.chats.tests.constants import CHATS_GET_DIRECT_URL
from apps.profiles.tests.utils import async_get_tokens


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_chats_get_chat_direct_create_valid(async_client, async_user, async_user_2):
    # user log_in
    token = await async_get_tokens(async_user)
    header = {"Authorization": "Bearer " + token}

    response = await async_client.post(
        reverse(CHATS_GET_DIRECT_URL, kwargs={"user_id": async_user_2.id}) + "direct/",
        headers=header,
    )

    # assertions
    assert response.status_code == 201
    assert response.data.get("name") == async_user_2.username
    assert response.data.get("image_url") == async_user_2.image_url
    assert response.data.get("type") == Chat.Type.DIRECT


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_chats_get_chat_direct_create_private_valid(
    async_client, async_user, async_user_2_private, async_follower_user_accepted_private
):
    # user log_in
    token = await async_get_tokens(async_user)
    header = {"Authorization": "Bearer " + token}

    response = await async_client.post(
        reverse(CHATS_GET_DIRECT_URL, kwargs={"user_id": async_user_2_private.id}) + "direct/",
        headers=header,
    )

    # assertions
    assert response.status_code == 201
    assert response.data.get("name") == async_user_2_private.username
    assert response.data.get("image_url") == async_user_2_private.image_url
    assert response.data.get("type") == Chat.Type.DIRECT


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_chats_get_chat_direct_create_private_not_followed(
    async_client, async_user, async_user_2_private
):
    # user log_in
    token = await async_get_tokens(async_user)
    header = {"Authorization": "Bearer " + token}

    response = await async_client.post(
        reverse(CHATS_GET_DIRECT_URL, kwargs={"user_id": async_user_2_private.id}) + "direct/",
        headers=header,
    )

    # assertions
    assert response.status_code == 403


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_chats_get_chat_direct_create_current_user(async_client, async_user):
    # user log_in
    token = await async_get_tokens(async_user)
    header = {"Authorization": "Bearer " + token}

    response = await async_client.post(
        reverse(CHATS_GET_DIRECT_URL, kwargs={"user_id": async_user.id}) + "direct/",
        headers=header,
    )

    # assertions
    assert response.status_code == 400
    assert response.data == "You can't chat with yourself"


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_chats_get_chat_direct_exists_valid(
    async_client, async_user, async_user_2, chat_direct_user_user_2
):
    # user log_in
    token = await async_get_tokens(async_user)
    header = {"Authorization": "Bearer " + token}

    response = await async_client.post(
        reverse(CHATS_GET_DIRECT_URL, kwargs={"user_id": async_user_2.id}) + "direct/",
        headers=header,
    )

    # assertions
    assert response.status_code == 200
    assert response.data.get("name") == async_user_2.username
    assert response.data.get("image_url") == async_user_2.image_url
    assert response.data.get("type") == Chat.Type.DIRECT


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_chats_get_chat_direct_exists_private_valid(
    async_client,
    async_user,
    async_user_2_private,
    async_follower_user_accepted_private,
    chat_direct_user_user_2_private,
):
    # user log_in
    token = await async_get_tokens(async_user)
    header = {"Authorization": "Bearer " + token}

    response = await async_client.post(
        reverse(CHATS_GET_DIRECT_URL, kwargs={"user_id": async_user_2_private.id}) + "direct/",
        headers=header,
    )

    # assertions
    assert response.status_code == 200
    assert response.data.get("name") == async_user_2_private.username
    assert response.data.get("image_url") == async_user_2_private.image_url
    assert response.data.get("type") == Chat.Type.DIRECT


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_chats_get_chat_direct_exists_private_not_followed(
    async_client, async_user, async_user_2_private, chat_direct_user_user_2_private
):
    # user log_in
    token = await async_get_tokens(async_user)
    header = {"Authorization": "Bearer " + token}

    response = await async_client.post(
        reverse(CHATS_GET_DIRECT_URL, kwargs={"user_id": async_user_2_private.id}) + "direct/",
        headers=header,
    )

    # assertions
    assert response.status_code == 403
