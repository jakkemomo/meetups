from django.contrib import admin
from .models import Categories, Event


# Register your models here.

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "category", "address", "description", "start_date", "end_date"]
    list_filter = ["name", "category"]
    search_fields = ["name", "category"]
    ordering = ["start_date", "name"]


@admin.register(Categories)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    list_filter = ["name"]
    search_fields = ["name"]
    ordering = ["name"]
