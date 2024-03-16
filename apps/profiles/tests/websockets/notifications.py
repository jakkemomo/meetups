import os
import django
import pytest

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from channels.testing import WebsocketCommunicator
from channels.routing import URLRouter

from apps.profiles.routers import websocket_urlpatterns
from apps.profiles.tests.fixtures import *


@pytest.mark.django_db
@pytest.mark.asyncio
async def test_receive(
        user,
):
    application = URLRouter(websocket_urlpatterns)
    communicator = WebsocketCommunicator(application, f"ws/notifications/{user.id}/")
    communicator.scope["user"] = user

    connected, subprotocol = await communicator.connect()
    assert connected

    data = {"message": "Hello!"}
    await communicator.send_json_to(data)
    response = await communicator.receive_json_from()
    assert response == data
    await communicator.disconnect()
