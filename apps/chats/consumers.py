import json
import logging

from apps.notifications.base import BaseConsumer
from apps.chats.utils import get_chat_async, has_chat_permissions

logger = logging.getLogger("chats_app")


class ChatConsumer(BaseConsumer):
    async def connect(self):
        user = self.scope.get("user")
        if not user or user.is_anonymous:
            logger.warning(
                f"Anonymous user request in {self.__class__.__name__}"
            )
            await self.close()

        chat_id = self.scope.get("url_route").get("kwargs").get("chat_id")
        chat = await get_chat_async(chat_id)
        if not chat:
            logger.warning(
                f"Chat not found in {self.__class__.__name__}"
            )
            await self.close()

        if not await has_chat_permissions(user=user, chat=chat):
            logger.warning(
                f"User not authorised in {self.__class__.__name__}"
            )
            await self.close()

        self.group_name = chat_id
        await super().connect()

    async def receive(self, text_data):
        data = json.loads(text_data)
        await self.channel_layer.group_send(self.group_name, data)

    async def chat_message(self, data):
        await self.send(text_data=json.dumps(data))
