"""Business capabilities for employee authentication."""

from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

from apps.employees.constants import EMPLOYEE_STATUS_ACTIVE
from apps.employees.models import Employee
from apps.employees.selectors import EmployeeSelector
from apps.users.exceptions import (
    EmployeeAccountNotFound,
    InactiveEmployee,
    InvalidCredentials,
)


class EmployeeAuthenticationService:
    """Authenticate active Employee accounts and resolve the current Employee."""

    @staticmethod
    def authenticate_employee(
        username: str,
        password: str,
    ) -> tuple[Employee, str, str]:
        """Authenticate an active Employee and issue a JWT pair."""

        user = authenticate(username=username, password=password)
        if user is None:
            raise InvalidCredentials

        employee = EmployeeAuthenticationService._get_active_employee(user.id)
        refresh_token = RefreshToken.for_user(user)

        return employee, str(refresh_token.access_token), str(refresh_token)

    @staticmethod
    def get_current_employee(user_id: int) -> Employee:
        """Return the active Employee associated with the authenticated User."""

        return EmployeeAuthenticationService._get_active_employee(user_id)

    @staticmethod
    def _get_active_employee(user_id: int) -> Employee:
        """Resolve and validate the Employee profile for a User."""

        employee = EmployeeSelector.get_by_user_id_for_authentication(user_id)
        if employee is None:
            raise EmployeeAccountNotFound

        if employee.status != EMPLOYEE_STATUS_ACTIVE:
            raise InactiveEmployee

        return employee
