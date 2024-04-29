import json
import logging

from apps.websockets.base import BaseConsumer
from apps.websockets.utils import (
    get_chat_async,
    has_chat_permissions,
)

logger = logging.getLogger("profiles_ws_consumers")


class NotificationConsumer(BaseConsumer):
    async def connect(self):
        user = self.scope.get("user")
        if not user or user.is_anonymous:
            logger.warning(f"Anonymous user request in {__name__}")
            await self.close()

        self.group_name = str(user.id)

        await super().connect()

    async def follow_notification(self, data):
        await self.send(text_data=json.dumps(data))

    async def follow_request_notification(self, data):
        await self.send(text_data=json.dumps(data))

    async def accept_follow_request_notification(self, data):
        await self.send(text_data=json.dumps(data))


class ChatConsumer(BaseConsumer):
    async def connect(self):
        try:
            user = self.scope.get("user")
            if not user or user.is_anonymous:
                logger.warning(f"Anonymous user request in {__name__}")
                await self.close()
                return

            chat_id = self.scope.get("url_route").get("kwargs").get("chat_id")
            chat = await get_chat_async(chat_id)
            if not chat:
                logger.warning(
                    f"Chat not found in {__name__}"
                )
                await self.close()
                return

            if not await has_chat_permissions(user=user, chat=chat):
                logger.warning(
                    f"User not authorised in {__name__}"
                )
                await self.close()
                return

            self.group_name = chat_id
            await super().connect()

        except Exception as exc:
            await self.close()

    async def receive(self, text_data):
        data = json.loads(text_data)
        await self.channel_layer.group_send(self.group_name, data)

    async def chat_message(self, data):
        await self.send(text_data=json.dumps(data))
