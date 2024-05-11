from django.contrib import admin
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_by', 'recipient', 'type', 'created_at')
    list_filter = ('type', 'created_at')
    search_fields = ('id', 'created_by__username', 'recipient__username')
    readonly_fields = ('created_at',)
