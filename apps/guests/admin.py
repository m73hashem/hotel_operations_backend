from django.contrib import admin

from .models import Guest, Stay


@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "first_name",
        "last_name",
        "phone",
        "email",
        "language",
    )
    search_fields = (
        "first_name",
        "last_name",
        "phone",
        "email",
    )
    list_filter = ("language",)


@admin.register(Stay)
class StayAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "guest",
        "room",
        "check_in",
        "expected_check_out",
        "actual_check_out",
        "status",
    )
    search_fields = (
        "guest__first_name",
        "guest__last_name",
        "guest__phone",
        "room__room_number",
    )
    list_filter = (
        "status",
        "room__hotel",
    )
    