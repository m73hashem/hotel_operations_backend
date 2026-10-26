"""Read-only dashboard selectors."""

from .case_details_selector import CaseDetailsSelector
from .dashboard_summary_selector import DashboardSummarySelector
from .dashboard_statistics_selector import DashboardStatisticsSelector
from .dashboard_metrics_selector import DashboardMetricsSelector
from .dashboard_widgets_selector import DashboardWidgetsSelector
from .department_queue_selector import DepartmentQueueSelector
from .my_assignments_selector import MyAssignmentsSelector

__all__ = [
    "CaseDetailsSelector",
    "DashboardSummarySelector",
    "DashboardStatisticsSelector",
    "DashboardMetricsSelector",
    "DashboardWidgetsSelector",
    "DepartmentQueueSelector",
    "MyAssignmentsSelector",
]
