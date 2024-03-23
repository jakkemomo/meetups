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


def get_communicator(app, user):
    communicator = WebsocketCommunicator(
        app,
        f"ws/notifications/{user.id}/",
    )
    communicator.scope["user"] = user
    return communicator