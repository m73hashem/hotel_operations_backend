"""DTO for the employee dashboard summary."""

from dataclasses import dataclass


@dataclass(frozen=True)
class DashboardSummaryDTO:
    """Immutable summary of the authenticated Employee's workload."""

    employee_id: int
    full_name: str
    department_name: str
    new_cases_count: int
    assigned_cases_count: int
    in_progress_cases_count: int
    completed_today_count: int
    my_active_assignments_count: int
