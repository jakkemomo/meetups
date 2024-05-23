from abc import ABC, abstractmethod


class AbstractHandler(ABC):
    @abstractmethod
    async def handle(
            self, created_by, recipient,
            notification_type, additional_data
    ):
        """
        This method must have an implementation to notify user in some
        unique way, for example, via InApp notifications or Email.
        """
        ...
