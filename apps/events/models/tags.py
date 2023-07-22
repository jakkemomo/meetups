from django.db.models import fields

from apps.core.models import AbstractBaseModel


class Tag(AbstractBaseModel):
    name = fields.CharField(max_length=250, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"
