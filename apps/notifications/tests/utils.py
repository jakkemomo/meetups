from channels.testing import WebsocketCommunicator


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
