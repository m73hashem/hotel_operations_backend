"""Versioned URLs for operational Room endpoints."""

from django.urls import path

from .views import RoomListAPIView

app_name = "rooms"

urlpatterns = [
    path("", RoomListAPIView.as_view(), name="room-list"),
]
