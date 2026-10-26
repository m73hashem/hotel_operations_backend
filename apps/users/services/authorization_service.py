"""Business capabilities for role-based authorization."""

from apps.users.builders import AuthorizationContextBuilder
from apps.users.constants import ROLE_ADMIN, ROLE_PERMISSION_MATRIX, ROLE_SUPERVISOR
from apps.users.dto import AuthorizationContextDTO
from apps.users.exceptions import (
    AssignmentAccessDenied,
    CaseAccessDenied,
    DepartmentAccessDenied,
    PermissionDenied,
)
from apps.employees.exceptions import CaseNotFound
from apps.requests.selectors import CaseDepartmentScopeSelector
from apps.users.selectors import AuthorizationSelector


class AuthorizationService:
    """Authorize Employees using Django Group roles and loaded domain facts."""

    @staticmethod
    def check_permission(user_id: int, required_permission: str) -> None:
        """Require one platform permission for the authenticated Employee."""

        context = AuthorizationService._get_context(user_id)
        AuthorizationService._require_permission(context, required_permission)

    @staticmethod
    def check_department_access(
        user_id: int,
        department_id: int,
        required_permission: str | None = None,
    ) -> None:
        """Require access to one department, optionally with a permission."""

        context = AuthorizationService._get_context(user_id)
        AuthorizationService._require_permission(context, required_permission)
        AuthorizationService._require_department_access(context, department_id)

    @staticmethod
    def check_case_access(
        user_id: int,
        case_id: int,
        required_permission: str | None = None,
    ) -> None:
        """Require access to one Case and its service department when assigned."""

        case = CaseDepartmentScopeSelector.get_for_access(case_id)
        if case is None:
            raise CaseNotFound

        context = AuthorizationService._get_context(user_id)
        AuthorizationService._require_permission(context, required_permission)
        if AuthorizationService._has_management_access(context):
            return

        if not CaseDepartmentScopeSelector.is_visible_to_department(
            case,
            context.department_id,
        ):
            raise CaseAccessDenied

    @staticmethod
    def check_assignment_access(
        user_id: int,
        assignment_id: int,
        required_permission: str | None = None,
    ) -> None:
        """Require ownership of one Assignment and access to its department."""

        context = AuthorizationService._get_context(user_id)
        AuthorizationService._require_permission(context, required_permission)
        assignment = AuthorizationSelector.get_assignment_for_access(assignment_id)
        if assignment is None:
            raise AssignmentAccessDenied

        if AuthorizationService._has_management_access(context):
            return

        if assignment.employee.user_id != context.user_id:
            raise AssignmentAccessDenied

        AuthorizationService._require_department_access(
            context,
            assignment.employee.department_id,
        )

    @staticmethod
    def _get_context(user_id: int) -> AuthorizationContextDTO:
        """Load and map the authorization facts for one authenticated User."""

        result = AuthorizationSelector.get_employee_and_roles(user_id)
        if result is None:
            raise PermissionDenied

        employee, roles = result
        return AuthorizationContextBuilder.build(employee, roles)

    @staticmethod
    def _require_permission(
        context: AuthorizationContextDTO,
        required_permission: str | None,
    ) -> None:
        """Reject contexts that do not hold a required permission."""

        if required_permission is None or context.is_superuser:
            return

        permissions = {
            permission
            for role in context.roles
            for permission in ROLE_PERMISSION_MATRIX[role]
        }
        if required_permission not in permissions:
            raise PermissionDenied

    @staticmethod
    def _require_department_access(
        context: AuthorizationContextDTO,
        department_id: int,
    ) -> None:
        """Reject cross-department access unless the role has management access."""

        if AuthorizationService._has_management_access(context):
            return

        if context.department_id != department_id:
            raise DepartmentAccessDenied

    @staticmethod
    def _has_management_access(context: AuthorizationContextDTO) -> bool:
        """Return whether the context has global operational access."""

        return context.is_superuser or ROLE_ADMIN in context.roles or ROLE_SUPERVISOR in context.roles
