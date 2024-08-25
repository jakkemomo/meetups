import string
from random import choices

import pytest
from channels.db import database_sync_to_async

from apps.chats.models import Chat, Message


@pytest.fixture
async def chat_event_add_user(event, async_user) -> Chat:
    await database_sync_to_async(event.chat.participants.add)(async_user)
    return event.chat


@pytest.fixture
async def chat_event_add_user_2(event, async_user_2) -> Chat:
    await database_sync_to_async(event.chat.participants.add)(async_user_2)
    return event.chat


@pytest.fixture
async def chat_event_add_message(event, async_user) -> Message:
    message = await database_sync_to_async(Message.objects.create)(
        created_by=async_user,
        chat=event.chat,
        message_text="Hello, World!",
        created_at="2024-08-25T17:02:05.676522Z",
    )
    return message


@pytest.fixture
async def chat_event_add_hundred_messages(event, async_user) -> list:
    messages = []
    for _ in range(100):
        # Generate a random message
        message_text = "".join(choices(string.ascii_uppercase + string.digits, k=20))

        message = await database_sync_to_async(Message.objects.create)(
            created_by=async_user, chat=event.chat, message_text=message_text
        )
        messages.append(message)
    return messages


@pytest.fixture
async def chat_direct() -> Chat:
    chat = await database_sync_to_async(Chat.objects.create)(type=Chat.Type.DIRECT)
    return chat


@pytest.fixture
async def chat_direct_user_user_2(async_user, async_user_2) -> Chat:
    chat = await database_sync_to_async(Chat.objects.create)(type=Chat.Type.DIRECT)
    await database_sync_to_async(chat.participants.add)(async_user.id, async_user_2.id)
    return chat


@pytest.fixture
async def chat_direct_user_user_2_private(async_user, async_user_2_private) -> Chat:
    chat = await database_sync_to_async(Chat.objects.create)(type=Chat.Type.DIRECT)
    await database_sync_to_async(chat.participants.add)(async_user.id, async_user_2_private.id)
    return chat
