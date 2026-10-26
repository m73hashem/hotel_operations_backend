"""Application workflow for operational dashboard widgets."""

from apps.dashboard.builders import DashboardWidgetsBuilder
from apps.dashboard.dto import DashboardWidgetsDTO
from apps.dashboard.services import DashboardWidgetsService


class DashboardWidgetsUseCase:
    """Coordinate widget retrieval and DTO construction."""

    @staticmethod
    def execute(user_id: int) -> DashboardWidgetsDTO:
        """Return immutable dashboard widgets for the authenticated Employee."""

        widgets = DashboardWidgetsService.get_widgets(user_id)
        return DashboardWidgetsBuilder.build(widgets)
