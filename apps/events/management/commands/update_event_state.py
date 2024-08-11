import datetime

from django.core.management.base import BaseCommand

from apps.events.models import Event
from apps.events.serializers import utils


class Command(BaseCommand):
    help = "Finishes event or updates event time in case it was a repeating event."

    def handle(self, *args, **options):
        events = Event.objects.filter(is_finished=False).all()
        for event in events:
            self.update_event_state(event)

    def update_event_state(self, event):
        if not event.repeatable and self.is_finished(event):
            event.is_finished = True
            event.save()
            self.stdout.write(self.style.SUCCESS('Successfully updated event "%s"' % event.id))
        elif event.repeatable and self.is_finished(event):
            schedules = [
                {"day_of_week": schedule.day_of_week, "time": schedule.time}
                for schedule in event.schedule.all()
            ]
            if schedules:
                schedule_start = utils.get_schedule_start(schedules)
                event.start_date = schedule_start.date()
                event.start_time = schedule_start.time()
                event.save()
                self.stdout.write(
                    self.style.SUCCESS('Successfully updated repeated event "%s"' % event.id)
                )

    @staticmethod
    def is_finished(event):
        now = datetime.datetime.now(tz=datetime.timezone.utc)
        if event.end_date and event.end_time:
            end_datetime = datetime.datetime.combine(
                event.end_date, event.end_time, tzinfo=datetime.timezone.utc
            )
        elif event.end_date and not event.end_time:
            end_datetime = datetime.datetime.combine(
                event.end_date, datetime.time(23, 59, 59), tzinfo=datetime.timezone.utc
            )
        elif not event.end_date and event.end_time:
            end_datetime = datetime.datetime.combine(
                event.start_date, event.end_time, tzinfo=datetime.timezone.utc
            )
        else:
            end_datetime = datetime.datetime.combine(
                event.start_date, datetime.time(23, 59, 59), tzinfo=datetime.timezone.utc
            )
        if now > end_datetime:
            return True
        return False
