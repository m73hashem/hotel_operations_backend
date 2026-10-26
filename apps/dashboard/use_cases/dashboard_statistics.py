"""Application workflow for operational dashboard statistics."""

from apps.dashboard.builders import DashboardStatisticsBuilder
from apps.dashboard.dto import DashboardStatisticsDTO
from apps.dashboard.services import DashboardStatisticsService


class DashboardStatisticsUseCase:
    """Coordinate statistics retrieval and DTO construction."""

    @staticmethod
    def execute(user_id: int) -> DashboardStatisticsDTO:
        """Return immutable dashboard statistics for the authenticated Employee."""

        statistics = DashboardStatisticsService.get_statistics(user_id)
        return DashboardStatisticsBuilder.build(statistics)
