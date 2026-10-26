"""Builder for dashboard metrics DTOs."""

from apps.dashboard.dto import DashboardMetricsDTO


class DashboardMetricsBuilder:
    """Map aggregate metrics into an immutable transport DTO."""

    @staticmethod
    def build(metrics: dict[str, int]) -> DashboardMetricsDTO:
        """Build a metrics DTO without executing ORM operations."""

        return DashboardMetricsDTO(
            open_cases=metrics["open_cases"],
            in_progress_cases=metrics["in_progress_cases"],
            closed_cases=metrics["closed_cases"],
            active_assignments=metrics["active_assignments"],
            occupied_rooms=metrics["occupied_rooms"],
            available_rooms=metrics["available_rooms"],
            out_of_service_rooms=metrics["out_of_service_rooms"],
            active_stays=metrics["active_stays"],
        )
