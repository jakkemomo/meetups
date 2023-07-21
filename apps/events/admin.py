from django.contrib import admin
from .models import Category, Event, Tag


# Register your models here.

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "category", "address", "description", "start_date", "end_date"]
    list_filter = ["name", "category"]
    search_fields = ["name", "category"]
    ordering = ["start_date", "name"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    list_filter = ["name"]
    search_fields = ["name"]
    ordering = ["name"]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    list_filter = ["name"]
    search_fields = ["name"]
    ordering = ["name"]
