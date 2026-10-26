"""Versioned URLs for dashboard endpoints."""

from django.urls import path

from apps.dashboard.api.views import (
    CaseDetailsAPIView,
    DashboardSummaryAPIView,
    DashboardStatisticsAPIView,
    DashboardMetricsAPIView,
    DashboardWidgetsAPIView,
    DepartmentQueueAPIView,
    MyAssignmentsAPIView,
)

app_name = "dashboard"

urlpatterns = [
    path("cases/<int:case_id>/", CaseDetailsAPIView.as_view(), name="case-details"),
    path("summary/", DashboardSummaryAPIView.as_view(), name="summary"),
    path("statistics/", DashboardStatisticsAPIView.as_view(), name="statistics"),
    path("metrics/", DashboardMetricsAPIView.as_view(), name="metrics"),
    path("widgets/", DashboardWidgetsAPIView.as_view(), name="widgets"),
    path("my-assignments/", MyAssignmentsAPIView.as_view(), name="my-assignments"),
    path("department-queue/", DepartmentQueueAPIView.as_view(), name="department-queue"),
]
