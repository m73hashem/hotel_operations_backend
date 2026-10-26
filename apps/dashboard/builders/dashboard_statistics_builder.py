"""Builder for dashboard statistics DTOs."""

from apps.dashboard.dto import DashboardStatisticsDTO


class DashboardStatisticsBuilder:
    """Map aggregate statistics into an immutable transport DTO."""

    @staticmethod
    def build(statistics: dict[str, int]) -> DashboardStatisticsDTO:
        """Build a statistics DTO without executing ORM operations."""

        return DashboardStatisticsDTO(
            total_open_cases=statistics["total_open_cases"],
            total_in_progress_cases=statistics["total_in_progress_cases"],
            total_closed_today=statistics["total_closed_today"],
            my_active_assignments=statistics["my_active_assignments"],
            my_completed_today=statistics["my_completed_today"],
            pending_requests=statistics["pending_requests"],
            active_stays=statistics["active_stays"],
            occupied_rooms=statistics["occupied_rooms"],
            available_rooms=statistics["available_rooms"],
            out_of_service_rooms=statistics["out_of_service_rooms"],
        )
