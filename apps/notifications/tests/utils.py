from channels.db import database_sync_to_async
from channels.testing import WebsocketCommunicator

from apps.profiles.models.followers import Follower


async def async_follower(user, follower, status):
    data = {
        'user': user,
        'follower': follower,
        'status': status,
    }
    return await database_sync_to_async(Follower.objects.create)(**data)


def get_communicator(app, user) -> WebsocketCommunicator:
    communicator = WebsocketCommunicator(
        app,
        f"ws/notifications/{user.id}/",
    )
    communicator.scope["user"] = user
    return communicator


def get_chat_communicator(app, user, chat) -> WebsocketCommunicator:
    communicator = WebsocketCommunicator(
        app,
        f"ws/chats/{chat.id}/",
    )
    communicator.scope["user"] = user
    return communicator


def get_wrong_chat_communicator(app, user) -> WebsocketCommunicator:
    communicator = WebsocketCommunicator(
        app,
        f"ws/chats/1",
    )
    communicator.scope["user"] = user
    return communicator
