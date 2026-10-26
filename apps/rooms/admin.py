from django.contrib import admin

from .models import Hotel, Room


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "timezone",
        "status",
    )
    search_fields = ("name",)
    list_filter = ("status",)


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "hotel",
        "room_number",
        "room_type",
        "status",
    )
    search_fields = (
        "room_number",
        "hotel__name",
    )
    list_filter = (
        "hotel",
        "room_type",
        "status",
    )

    