from django.conf import settings
from django.db import models
from django.db.models import fields

from apps.core.models import AbstractBaseModel
from apps.events.utils import events_image_upload_path
from common.mixins import ResizeImageMixin

user_model = settings.AUTH_USER_MODEL


class Categories(AbstractBaseModel):
    name = fields.CharField(max_length=250)

    def __str__(self):
        return self.name


class Event(AbstractBaseModel, ResizeImageMixin):
    category = models.ForeignKey(
        Categories, on_delete=models.CASCADE, related_name="category_events", null=True, blank=True
    )
    name = fields.CharField(max_length=250, unique=True, null=True, blank=True)
    address = fields.CharField(max_length=250, null=True, blank=True)
    description = fields.TextField(max_length=250, null=True, blank=True)
    image = models.ImageField(upload_to=events_image_upload_path, null=True, blank=True,
                              default='events/image/default-event.jpeg')
    start_date = fields.DateTimeField(null=True, blank=True)
    end_date = fields.DateTimeField(null=True, blank=True)

    is_finished = fields.BooleanField(null=False, blank=False, default=False)
    is_visible = fields.BooleanField(null=False, blank=False, default=True)

    participants = models.ManyToManyField(user_model, blank=True)

    class Meta:
        ordering = ["start_date"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f"/events/{self.id}/"

    def save(self, *args, **kwargs):
        if self.pk is None or self.objects.get(pk=self.pk) != self.image:
            self.resize(self.image, (400, 500))
        super().save(*args, **kwargs)
