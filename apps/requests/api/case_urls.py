"""Versioned URLs for operational Case list endpoints."""

from django.urls import path

from .views import CaseListAPIView

app_name = "cases"

urlpatterns = [
    path(
        "",
        CaseListAPIView.as_view(),
        name="case-list",
    ),
]
