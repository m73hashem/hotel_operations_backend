"""DTO for department-scoped operational dashboard metrics."""

from dataclasses import dataclass


@dataclass(frozen=True)
class DashboardMetricsDTO:
    """Immutable operational metrics for the authenticated Employee."""

    open_cases: int
    in_progress_cases: int
    closed_cases: int
    active_assignments: int
    occupied_rooms: int
    available_rooms: int
    out_of_service_rooms: int
    active_stays: int
