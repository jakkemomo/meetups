from apps.core.models import AbstractBaseModel
from django.db import models


class Schedule(AbstractBaseModel):
    class DayOfWeek(models.TextChoices):
        SUN = "sun", "Sunday"
        MON = "mon", "Monday"
        TUE = "tue", "Tuesday"
        WED = "wed", "Wednesday"
        THU = "thu", "Thursday"
        FRI = "fri", "Friday"
        SAT = "sat", "Saturday"
    """
    "schedules": [
    {
       "day_of_week": "mon",
       "time": "17:30:00"
    },
    {
       "day_of_week": "sun",
       "time": "20:00:00"
    }]

    SELECT * FROM schedules WHERE event_id = 18 and day_of_week = 'sun';
    event_id: foreign key,
    time: time field,
    day_of_week: enum ( 'sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat')
    """

    event = models.ForeignKey("events.Event", on_delete=models.CASCADE, related_name="schedules", blank=False,)
    day_of_week = models.CharField(max_length=3, choices=DayOfWeek.choices, blank=False, null=False)
    time = models.TimeField(blank=False, null=False)

    class Meta:
        verbose_name = "Schedule"
        verbose_name_plural = "Schedules"
        unique_together = ("event", "day_of_week")
        db_table = 'events_schedule'
        ordering = ['event', 'day_of_week']
