"""Versioned URLs for operational Request endpoints."""

from django.urls import path

from .views import CreateCaseAPIView, RequestListAPIView

app_name = "requests"

urlpatterns = [
    path(
        "",
        RequestListAPIView.as_view(),
        name="request-list",
    ),
    path(
        "create-case/",
        CreateCaseAPIView.as_view(),
        name="create-case",
    ),
]
