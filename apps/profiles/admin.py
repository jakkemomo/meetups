from django.contrib import admin

from .models.city import City
from .models.users import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "id", "email", "first_name", "last_name", "city", "is_staff")
    search_fields = ("username", "email", "first_name", "last_name", "city")
    readonly_fields = ("date_joined",)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "email", "city"," image_url")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "is_email_verified",)}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "country", "center", "timezone")
    search_fields = ("name", "country")
