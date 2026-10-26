"""Builder for immutable authorization contexts."""

from apps.employees.models import Employee
from apps.users.dto import AuthorizationContextDTO


class AuthorizationContextBuilder:
    """Map already-loaded authorization facts into an immutable DTO."""

    @staticmethod
    def build(employee: Employee, roles: tuple[str, ...]) -> AuthorizationContextDTO:
        """Build an authorization context without ORM operations."""

        return AuthorizationContextDTO(
            employee_id=employee.id,
            user_id=employee.user_id,
            department_id=employee.department_id,
            roles=roles,
            is_superuser=employee.user.is_superuser,
        )
