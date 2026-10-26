"""Business capability for operational dashboard metrics."""

from apps.dashboard.selectors import DashboardMetricsSelector
from apps.employees.services import EmployeeAccessService


class DashboardMetricsService:
    """Validate Employee access and obtain department-scoped metrics."""

    @staticmethod
    def get_metrics(user_id: int) -> dict[str, int]:
        """Return operational metrics for one active Employee."""

        employee = EmployeeAccessService.get_active_employee(user_id)
        return DashboardMetricsSelector.get_metrics(employee.department_id)
