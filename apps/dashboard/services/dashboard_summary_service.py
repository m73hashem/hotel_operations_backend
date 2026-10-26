"""Business capability for an Employee dashboard summary."""

from django.utils import timezone

from apps.dashboard.selectors import DashboardSummarySelector
from apps.dashboard.services.dashboard_employee_access_service import (
    DashboardEmployeeAccessService,
)


class DashboardSummaryService:
    """Validate Employee dashboard access and obtain summary facts."""

    @staticmethod
    def get_summary(user_id: int):
        """Return the active Employee and its current dashboard statistics."""

        employee = DashboardEmployeeAccessService.get_active_employee(user_id)

        statistics = DashboardSummarySelector.get_statistics(
            employee.department_id,
            employee.id,
            timezone.localdate(),
        )
        return employee, statistics
