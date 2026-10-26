"""Business capability for operational dashboard widgets."""

from apps.dashboard.selectors import DashboardWidgetsSelector
from apps.employees.services import EmployeeAccessService


class DashboardWidgetsService:
    """Validate Employee access and obtain dashboard widgets."""

    @staticmethod
    def get_widgets(user_id: int) -> dict[str, list]:
        """Return dashboard widgets for one active Employee."""

        employee = EmployeeAccessService.get_active_employee(user_id)
        return DashboardWidgetsSelector.get_widgets(employee.department_id)
