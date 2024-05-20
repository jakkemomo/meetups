import time
from threading import Thread

from django.apps import AppConfig
from django.core.management import call_command

from config import settings


class EventsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.events"

    def ready(self):
        Thread(target=self.update_event_state, daemon=True).start()

    def update_event_state(self):
        time.sleep(60)
        while True:
            call_command("update_event_state")
            time.sleep(settings.EVENTS_UPDATE_INTERVAL)
