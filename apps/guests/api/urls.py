from django.urls import path

from .views import (
    GuestListCreateAPIView,
    GuestRetrieveUpdateDestroyAPIView,
)

urlpatterns = [
    path(
        "",
        GuestListCreateAPIView.as_view(),
        name="guest-list",
    ),
    path(
        "<int:pk>/",
        GuestRetrieveUpdateDestroyAPIView.as_view(),
        name="guest-detail",
    ),
]