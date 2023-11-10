from django.contrib import admin
from .models import Category, Event, Tag, Rating


class RatingInline(admin.TabularInline):
    model = Event.ratings.through


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "category",
        "address",
        "location",
        "description",
        "start_date",
        "end_date",
    ]
    inlines = [RatingInline]
    exclude = ("ratings",)
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


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ["id", "value", "user", "event"]
    list_filter = ["value", "user", "event"]
    search_fields = ["value", "user", "event"]
    ordering = ["value"]
