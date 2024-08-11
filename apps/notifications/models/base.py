from django.db import models

from config import settings

user_model = settings.AUTH_USER_MODEL


class AbstractNotificationsPreferences(models.Model):
    """
    This model provides every user it's notifications preferences fields.

    Use this class as a base for any notifications sending method preferences,
    for example In-App, Email.
    Also model must be added into PREFERENCES field in settings.

    THE NAME OF ANY PREFERENCE FIELD MUST MATCH ITS TYPE FROM Notification.Type.
    """

    user = models.OneToOneField(to=user_model, on_delete=models.CASCADE)

    class Meta:
        abstract = True
