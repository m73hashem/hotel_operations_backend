"""Shared active Employee access capability."""

from apps.employees.constants import EMPLOYEE_STATUS_ACTIVE
from apps.employees.selectors import EmployeeSelector
from apps.users.exceptions import EmployeeAccountNotFound, InactiveEmployee


class EmployeeAccessService:
    """Resolve the active Employee associated with an authenticated User."""

    @staticmethod
    def get_active_employee(user_id: int):
        """Return the active Employee profile or raise a domain exception."""

        employee = EmployeeSelector.get_by_user_id_for_authentication(user_id)
        if employee is None:
            raise EmployeeAccountNotFound
        if employee.status != EMPLOYEE_STATUS_ACTIVE:
            raise InactiveEmployee
        return employee
