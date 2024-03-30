from django.contrib import admin
from django.utils.html import format_html
from rest_framework.reverse import reverse

from .models import Category, Event, Tag, Rating


class RatingInline(admin.TabularInline):
    model = Event.ratings.through


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "category",
        "created_by",
        "participants_number",
        "address",
        "start_date",
        "end_date",
        "is_visible",
    ]
    inlines = [RatingInline]
    exclude = ("ratings",)
    list_filter = ["name", "category"]
    search_fields = ["name", "category"]
    ordering = ["start_date", "name"]

    def participants_number(self, obj):
        count = obj.participants.count()
        query = "?id__in={}".format(
            ','.join(map(str, obj.participants.values_list('id', flat=True)))
        )
        link = reverse("admin:profiles_user_changelist") + query
        return format_html(
            "<a href={}>{}</a>",
            link,
            count,
        )


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
