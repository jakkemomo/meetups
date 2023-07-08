from django.db.models import fields
from django.contrib.auth.models import User

from django.db import models

from apps.core.models import BaseModel


class Categories(BaseModel):
    name = fields.CharField(max_length=250)

    def __str__(self):
        return self.name


class Event(BaseModel):
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name="category_events")
    name = fields.CharField(max_length=250)
    address = fields.CharField(max_length=250)
    description = fields.TextField(max_length=250)
    start_date = fields.DateTimeField()
    end_date = fields.DateTimeField()
    users = models.ManyToManyField(User)

    class Meta:
        ordering = ["start_date"]

    def __str__(self):
        return self.name
