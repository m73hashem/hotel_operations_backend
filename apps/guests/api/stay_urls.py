"""Versioned URLs for operational Stay list endpoints."""

from django.urls import path

from .views import StayListAPIView

app_name = "stays"

urlpatterns = [
    path("", StayListAPIView.as_view(), name="stay-list"),
]
