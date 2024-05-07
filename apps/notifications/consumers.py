import json
import logging

from apps.notifications.base import BaseConsumer

logger = logging.getLogger("notifications_consumers")


class NotificationConsumer(BaseConsumer):
    async def connect(self):
        user = self.scope.get("user")
        if not user or user.is_anonymous:
            logger.warning(f"Anonymous user request in {__name__}")
            await self.close()

        self.group_name = str(user.id)

        await super().connect()

    async def notification(self, data):
        await self.send(text_data=json.dumps(data))
