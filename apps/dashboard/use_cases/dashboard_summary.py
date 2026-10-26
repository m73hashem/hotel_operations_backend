"""Application workflow for dashboard summary retrieval."""

from apps.dashboard.builders import DashboardSummaryBuilder
from apps.dashboard.dto import DashboardSummaryDTO
from apps.dashboard.services import DashboardSummaryService


class DashboardSummaryUseCase:
    """Coordinate dashboard summary retrieval and DTO construction."""

    @staticmethod
    def execute(user_id: int) -> DashboardSummaryDTO:
        """Return the authenticated Employee's dashboard summary DTO."""

        employee, statistics = DashboardSummaryService.get_summary(user_id)
        return DashboardSummaryBuilder.build(employee, statistics)
