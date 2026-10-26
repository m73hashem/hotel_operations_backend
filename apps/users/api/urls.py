"""Versioned URLs for employee authentication."""

from django.urls import path

from .views import (
    CurrentEmployeeAPIView,
    EmployeeLoginAPIView,
    LogoutAPIView,
    RefreshTokenAPIView,
)

app_name = "auth"

urlpatterns = [
    path("login/", EmployeeLoginAPIView.as_view(), name="login"),
    path("me/", CurrentEmployeeAPIView.as_view(), name="me"),
    path("refresh/", RefreshTokenAPIView.as_view(), name="refresh"),
    path("logout/", LogoutAPIView.as_view(), name="logout"),
]
