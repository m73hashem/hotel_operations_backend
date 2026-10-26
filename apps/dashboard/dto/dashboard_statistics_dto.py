"""DTO for department-scoped operational dashboard statistics."""

from dataclasses import dataclass


@dataclass(frozen=True)
class DashboardStatisticsDTO:
    """Immutable operational statistics for the authenticated Employee."""

    total_open_cases: int
    total_in_progress_cases: int
    total_closed_today: int
    my_active_assignments: int
    my_completed_today: int
    pending_requests: int
    active_stays: int
    occupied_rooms: int
    available_rooms: int
    out_of_service_rooms: int
