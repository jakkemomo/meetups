from django.contrib import admin
from .models import Chat, Message, Notification


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'created_at')
    list_filter = ('type', 'created_at')
    search_fields = ('id', 'type')
    filter_horizontal = ('participants',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_by', 'chat', 'created_at')
    list_filter = ('created_by', 'chat', 'created_at')
    search_fields = ('id', 'created_by__username', 'chat__id')
    readonly_fields = ('created_at',)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_by', 'recipient', 'type', 'created_at')
    list_filter = ('type', 'created_at')
    search_fields = ('id', 'created_by__username', 'recipient__username')
    readonly_fields = ('created_at',)

