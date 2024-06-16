from abc import ABC, abstractmethod

from apps.notifications.exceptions import MissingPreferencesObjectException
from apps.notifications.models import Notification

from config import settings

user_model = settings.AUTH_USER_MODEL


class AbstractNotificationsHandler(ABC):
    def __init__(self):
        self.preferences_model = self.get_preferences_model()

    def handle(
            self,
            created_by: user_model,
            recipient: user_model,
            notification_type: Notification.Type,
            additional_data: dict
    ):
        if self.check_preference(
            recipient=recipient,
            notification_type=notification_type
        ):
            self.notify(
                created_by=created_by,
                recipient=recipient,
                notification_type=notification_type,
                additional_data=additional_data
            )

    @abstractmethod
    def notify(
            self,
            created_by: user_model,
            recipient: user_model,
            notification_type: Notification.Type,
            additional_data: dict
    ):
        """
        This method must have an implementation to
        notify user if 'self.check_preference' is true.
        """
        ...

    @abstractmethod
    def get_preferences_model(self):
        """
        Needs for setting the 'self.preference_model'
        field from settings.PREFERENCES.
        """
        ...

    def check_preference(self, recipient, notification_type):
        preferences_object = (self.preferences_model.objects
                              .filter(user=recipient)
                              .first()
                              )
        if not preferences_object:
            try:
                preferences_object = self.preferences_model.objects.create(
                    user=recipient
                )
            except Exception as exc:
                raise MissingPreferencesObjectException(detail=exc)

        return getattr(preferences_object, notification_type, None)
