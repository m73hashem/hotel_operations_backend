"""Dashboard response DTOs."""

from .case_details_dto import (
    CaseDetailsDTO,
    ConversationMessageDTO,
    RequestInformationDTO,
    TimelineEventDTO,
)
from .dashboard_summary_dto import DashboardSummaryDTO
from .dashboard_statistics_dto import DashboardStatisticsDTO
from .dashboard_metrics_dto import DashboardMetricsDTO
from .dashboard_widgets_dto import (
    DashboardWidgetsDTO,
    OccupiedRoomWidgetDTO,
    RecentCaseWidgetDTO,
    RecentRequestWidgetDTO,
    RecentStayWidgetDTO,
)
from .department_queue_dto import DepartmentQueueDTO, DepartmentQueueItemDTO
from .my_assignments_dto import MyAssignmentDTO, MyAssignmentsDTO

__all__ = [
    "CaseDetailsDTO",
    "ConversationMessageDTO",
    "DashboardSummaryDTO",
    "DashboardStatisticsDTO",
    "DashboardMetricsDTO",
    "DashboardWidgetsDTO",
    "DepartmentQueueDTO",
    "DepartmentQueueItemDTO",
    "MyAssignmentDTO",
    "MyAssignmentsDTO",
    "OccupiedRoomWidgetDTO",
    "RecentCaseWidgetDTO",
    "RecentRequestWidgetDTO",
    "RecentStayWidgetDTO",
    "RequestInformationDTO",
    "TimelineEventDTO",
]
