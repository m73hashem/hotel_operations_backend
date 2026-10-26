"""Application workflow for operational dashboard metrics."""

from apps.dashboard.builders import DashboardMetricsBuilder
from apps.dashboard.dto import DashboardMetricsDTO
from apps.dashboard.services import DashboardMetricsService


class DashboardMetricsUseCase:
    """Coordinate metrics retrieval and DTO construction."""

    @staticmethod
    def execute(user_id: int) -> DashboardMetricsDTO:
        """Return immutable dashboard metrics for the authenticated Employee."""

        metrics = DashboardMetricsService.get_metrics(user_id)
        return DashboardMetricsBuilder.build(metrics)
