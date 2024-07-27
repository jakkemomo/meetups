import json
import logging

from apps.core.websockets.base import AbstractConsumer

logger = logging.getLogger("notifications_app")


class NotificationConsumer(AbstractConsumer):
    async def connect(self):
        user = self.scope.get("user")
        if not user or user.is_anonymous:
            logger.warning(
                f"Anonymous user request in {self.__class__.__name__}"
            )
            await self.close()

        self.group_name = f"user_{str(user.id)}"

        await super().connect()

    async def notification(self, data):
        await self.send(text_data=json.dumps(data))
