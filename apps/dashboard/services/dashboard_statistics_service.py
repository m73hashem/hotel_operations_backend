"""Business capability for operational dashboard statistics."""

from django.utils import timezone

from apps.dashboard.selectors import DashboardStatisticsSelector
from apps.employees.services import EmployeeAccessService


class DashboardStatisticsService:
    """Validate Employee access and obtain department-scoped aggregates."""

    @staticmethod
    def get_statistics(user_id: int) -> dict[str, int]:
        """Return operational statistics for one active Employee."""

        employee = EmployeeAccessService.get_active_employee(user_id)
        return DashboardStatisticsSelector.get_statistics(
            employee.department_id,
            employee.id,
            timezone.localdate(),
        )
