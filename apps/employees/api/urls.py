"""Versioned URLs for Employee operations."""

from django.urls import path

from .views import (
    AcceptAssignmentAPIView,
    AssignCaseAPIView,
    CloseCaseAPIView,
    CompleteWorkAPIView,
    StartWorkAPIView,
)

app_name = "operations"

urlpatterns = [
    path(
        "accept-assignment/",
        AcceptAssignmentAPIView.as_view(),
        name="accept-assignment",
    ),
    path(
        "assign-case/",
        AssignCaseAPIView.as_view(),
        name="assign-case",
    ),
    path(
        "start-work/",
        StartWorkAPIView.as_view(),
        name="start-work",
    ),
    path(
        "complete-work/",
        CompleteWorkAPIView.as_view(),
        name="complete-work",
    ),
    path(
        "close-case/",
        CloseCaseAPIView.as_view(),
        name="close-case",
    ),
]
