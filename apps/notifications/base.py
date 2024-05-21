import logging
from abc import abstractmethod

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer

logger = logging.getLogger("notifications_app")


class BaseConsumer(AsyncWebsocketConsumer):
    @abstractmethod
    async def connect(self):
        """
        This method needs a defined self.group_name in each subclass.

        For example, NotificationConsumer works with user's own group – it's id:
             async def connect(self):
                self.group_name = str(self.scope.get("user").pk)
                await super().connect()
        """
        try:
            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name
            )
        except AttributeError as exc:
            logger.error(exc)
            await self.close()
        except Exception as exc:
            logger.exception(
                f"Connection error in {self.__class__.__name__}: {exc}"
            )
            await self.close()

        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )


class BaseManager:
    @staticmethod
    async def send_data(type, recipient, data, created_at):
        channel_layer = get_channel_layer()
        await channel_layer.group_send(
            group=str(recipient),
            message={
                "type": type,
                "data": data,
                "created_at": created_at.isoformat(),
            }
        )
