"""Business capability for an Employee's assignment list."""

from apps.dashboard.selectors import MyAssignmentsSelector
from apps.employees.services import EmployeeAccessService


class MyAssignmentsService:
    """Validate Employee access and obtain its assignment history."""

    @staticmethod
    def get_my_assignments(user_id: int, **query_params):
        """Return assignments that belong only to the active authenticated Employee."""

        employee = EmployeeAccessService.get_active_employee(user_id)
        return list(MyAssignmentsSelector.list_for_employee(employee.id, **query_params))
