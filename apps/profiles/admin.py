from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models.users import User
from .models.followers import Follower


class FollowerInline(admin.TabularInline):
    model = Follower
    fk_name = "user"
    extra = 1


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "first_name", "last_name", "followers_number_link", "following_number_link", "city", "is_staff", "is_private")
    search_fields = ("username", "email", "first_name", "last_name", "city")
    readonly_fields = ("date_joined",)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "email", "city", "image_url")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "is_email_verified", "is_private")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    inlines = [FollowerInline]

    def followers_number_link(self, obj):
        queryset = Follower.objects.filter(user=obj, status="ACCEPTED")
        count = queryset.count()
        query = "?id__in={}".format(
            ','.join(map(str, queryset.values_list('follower__id', flat=True)))
        )
        link = reverse("admin:profiles_user_changelist") + query
        return format_html(
            "<a href={}>{}</a>",
            link,
            count,
        )

    followers_number_link.short_description = "Followers number" #

    def following_number_link(self, obj):
        queryset = Follower.objects.filter(follower=obj, status="ACCEPTED")
        count = queryset.count()
        query = "?id__in={}".format(
            ','.join(map(str, queryset.values_list('user__id', flat=True)))
        )
        link = reverse("admin:profiles_user_changelist") + query
        return format_html(
            "<a href={}>{}</a>",
            link,
            count,
        )

    following_number_link.short_description = "Following number"


@admin.register(Follower)
class FollowerAdmin(admin.ModelAdmin):
    list_display = ("id", "user_link", "follower_link", "status", "created_at", "updated_at")
    list_filter = ("user", "follower", "status")

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = (queryset.select_related("user").select_related("follower"))
        return queryset

    def user_link(self, obj):
        link = reverse(
            "admin:profiles_user_change",
            args=(obj.user.id,)
        )
        return format_html(
            "<a href={}>{}</a>",
            link,
            obj.user.email,
        )

    user_link.short_description = "User"

    def follower_link(self, obj):
        link = reverse(
            "admin:profiles_user_change",
            args=(obj.follower.id,)
        )
        return format_html(
            "<a href={}>{}</a>",
            link,
            obj.follower.email,
        )

    follower_link.short_description = "Follower"
