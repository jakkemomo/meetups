from django.db.models import fields


from apps.core.models import AbstractBaseModel


class Category(AbstractBaseModel):
    name = fields.CharField(max_length=250, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
