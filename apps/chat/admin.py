from django.contrib import admin

from .models import Conversation, Message


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "stay",
        "case",
        "type",
        "status",
        "created_at",
    )
    search_fields = (
        "stay__guest__first_name",
        "stay__guest__last_name",
        "stay__guest__phone",
    )
    list_filter = (
        "type",
        "status",
    )


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "conversation",
        "sender_type",
        "channel",
        "created_at",
    )
    search_fields = (
        "content",
        "sender_type",
    )
    list_filter = (
        "sender_type",
        "channel",
    )
    