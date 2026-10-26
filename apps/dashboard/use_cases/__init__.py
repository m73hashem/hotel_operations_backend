"""Dashboard application use cases."""

from .case_details import CaseDetailsUseCase
from .dashboard_summary import DashboardSummaryUseCase
from .dashboard_statistics import DashboardStatisticsUseCase
from .dashboard_metrics import DashboardMetricsUseCase
from .dashboard_widgets import DashboardWidgetsUseCase
from .department_queue import DepartmentQueueUseCase
from .my_assignments import MyAssignmentsUseCase

__all__ = [
    "CaseDetailsUseCase",
    "DashboardSummaryUseCase",
    "DashboardStatisticsUseCase",
    "DashboardMetricsUseCase",
    "DashboardWidgetsUseCase",
    "DepartmentQueueUseCase",
    "MyAssignmentsUseCase",
]
