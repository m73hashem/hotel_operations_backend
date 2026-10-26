"""Business capability for a department's Case queue."""

from apps.dashboard.selectors import DepartmentQueueSelector
from apps.employees.services import EmployeeAccessService


class DepartmentQueueService:
    """Validate Employee access and obtain its department Case queue."""

    @staticmethod
    def get_department_queue(user_id: int, **query_params):
        """Return open and assigned Cases for the active Employee's department."""

        employee = EmployeeAccessService.get_active_employee(user_id)
        return list(
            DepartmentQueueSelector.list_for_department(
                employee.department_id,
                **query_params,
            ),
        )
