"""Dashboard DTO builders."""

from .case_details_builder import CaseDetailsBuilder
from .dashboard_summary_builder import DashboardSummaryBuilder
from .dashboard_statistics_builder import DashboardStatisticsBuilder
from .dashboard_metrics_builder import DashboardMetricsBuilder
from .dashboard_widgets_builder import DashboardWidgetsBuilder
from .department_queue_builder import DepartmentQueueBuilder
from .my_assignments_builder import MyAssignmentsBuilder

__all__ = [
    "CaseDetailsBuilder",
    "DashboardSummaryBuilder",
    "DashboardStatisticsBuilder",
    "DashboardMetricsBuilder",
    "DashboardWidgetsBuilder",
    "DepartmentQueueBuilder",
    "MyAssignmentsBuilder",
]
