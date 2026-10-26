"""Builder for employee authentication response DTOs."""

from apps.employees.models import Employee
from apps.users.dto import (
    CurrentEmployeeDTO,
    EmployeeLoginDTO,
    LogoutDTO,
    TokenRefreshDTO,
)


class AuthenticationBuilder:
    """Transform already-loaded authentication objects into flat DTOs."""

    @staticmethod
    def build_login(
        employee: Employee,
        *,
        access_token: str,
        refresh_token: str,
    ) -> EmployeeLoginDTO:
        """Build the login DTO without executing ORM operations."""

        return EmployeeLoginDTO(
            employee_id=employee.id,
            user_id=employee.user_id,
            full_name=employee.name,
            department_id=employee.department_id,
            access_token=access_token,
            refresh_token=refresh_token,
        )

    @staticmethod
    def build_current_employee(employee: Employee) -> CurrentEmployeeDTO:
        """Build the current Employee DTO without executing ORM operations."""

        return CurrentEmployeeDTO(
            employee_id=employee.id,
            user_id=employee.user_id,
            full_name=employee.name,
            department_id=employee.department_id,
            email=employee.user.email,
        )

    @staticmethod
    def build_refresh(access_token: str) -> TokenRefreshDTO:
        """Build the refresh DTO from the newly issued access token."""

        return TokenRefreshDTO(access_token=access_token)

    @staticmethod
    def build_logout() -> LogoutDTO:
        """Build the logout confirmation DTO."""

        return LogoutDTO(logged_out=True)
