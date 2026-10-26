"""Builder for dashboard summary DTOs."""

from apps.dashboard.dto import DashboardSummaryDTO
from apps.employees.models import Employee


class DashboardSummaryBuilder:
    """Map already-loaded Employee and aggregate values into a DTO."""

    @staticmethod
    def build(employee: Employee, statistics: dict[str, int]) -> DashboardSummaryDTO:
        """Build a summary DTO without executing ORM operations."""

        return DashboardSummaryDTO(
            employee_id=employee.id,
            full_name=employee.name,
            department_name=employee.department.name,
            new_cases_count=statistics["new_cases_count"],
            assigned_cases_count=statistics["assigned_cases_count"],
            in_progress_cases_count=statistics["in_progress_cases_count"],
            completed_today_count=statistics["completed_today_count"],
            my_active_assignments_count=statistics["my_active_assignments_count"],
        )
