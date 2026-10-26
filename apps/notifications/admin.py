from django.contrib import admin

from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "employee",
        "notification_type",
        "title",
        "read_at",
        "created_at",
    )
    search_fields = (
        "title",
        "message",
        "employee__name",
        "employee__employee_number",
    )
    list_filter = (
        "notification_type",
        "read_at",
    )

    