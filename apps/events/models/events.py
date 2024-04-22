from django.conf import settings
from django.contrib.gis.db.models import PointField
from django.contrib.gis.geos import Point
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models import fields
from django.utils import timezone

from apps.core.models import AbstractBaseModel
from apps.events.models.categories import Category
from apps.events.models.rating import Rating
from apps.events.models.schedule import Schedule
from apps.events.models.tags import Tag

user_model = settings.AUTH_USER_MODEL


class Event(AbstractBaseModel):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="category_events", null=True, blank=True
    )
    tags = models.ManyToManyField(to=Tag, related_name="events", blank=True)
    name = fields.CharField(max_length=250, unique=True, null=True, blank=True)
    address = fields.CharField(max_length=250, null=False, blank=False, default="Беларусь, Минск")
    city = fields.CharField(max_length=50, null=False, blank=False, default="Минск")
    country = fields.CharField(max_length=50, null=False, blank=False, default="Беларусь")
    location = PointField(default=Point(27.561831, 53.902284))
    city_south_west_point = PointField(default=Point(27.561831, 53.902284))
    city_north_east_point = PointField(default=Point(27.561831, 53.902284))
    type = fields.CharField(
        max_length=10,
        choices=(("open", "Open"), ("private", "Private")),
        default="open",
        null=False,
        blank=False,
    )
    description = fields.TextField(max_length=250, null=True, blank=True)
    image_url = models.CharField(max_length=250, null=True, blank=True)

    start_date = fields.DateTimeField(null=True, blank=True, default=None)
    end_date = fields.DateTimeField(null=True, blank=True, default=None)
    start_time = fields.TimeField(null=True, blank=True, default=None)
    end_time = fields.TimeField(null=True, blank=True, default=None)

    private_token = fields.CharField(max_length=250, null=True, blank=True)

    is_finished = fields.BooleanField(null=False, blank=False, default=False)
    is_visible = fields.BooleanField(null=False, blank=False, default=True)

    participants = models.ManyToManyField(
        user_model, blank=True, related_name="event_participants"
    )
    desired_participants_number = models.PositiveIntegerField(default=0, null=True, blank=True)
    any_participant_number = fields.BooleanField(default=False)
    ratings = models.ManyToManyField(user_model, through=Rating, through_fields=("event", "user"))
    repeatable = fields.BooleanField(default=False)
    schedule = models.ManyToManyField(Schedule, related_name="events", blank=True)
    participants_age = fields.PositiveSmallIntegerField(default=18, null=False, blank=False)
    cost = fields.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    free = fields.BooleanField(default=True)
    currency = models.ForeignKey("Currency", on_delete=models.SET_NULL, null=True, blank=True)
    gallery = ArrayField(models.CharField(max_length=250, null=True, blank=True, default=""), default=list)

    class Meta:
        ordering = ["start_date"]
        verbose_name = "Event"
        verbose_name_plural = "Events"

    def __str__(self):
        return self.name
