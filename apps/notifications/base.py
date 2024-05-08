import logging
from abc import abstractmethod

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer

from apps.chats.exceptions import ConsumerWithoutGroupNameException


logger = logging.getLogger("chats_base")


class BaseConsumer(AsyncWebsocketConsumer):
    @abstractmethod
    async def connect(self):
        """
        This method needs a defined self.group_name in each subclass.

        For example, NotificationConsumer works with user's own groups:
             async def connect(self):
                self.group_name = str(self.scope.get("user").pk)
                await super().connect()
        """
        try:
            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name
            )
        except ConsumerWithoutGroupNameException as exc:
            logger.exception(
                f"Consumer {self.__name__} hasn't got a group_name",
                exc_info=exc,
            )
            return

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
