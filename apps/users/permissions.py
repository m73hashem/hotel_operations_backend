"""DRF permissions backed by the application authorization service."""

from rest_framework.permissions import SAFE_METHODS, BasePermission

from apps.users.constants import (
    PERMISSION_ASSIGNMENTS_ACCEPT,
    PERMISSION_CASES_ASSIGN,
    PERMISSION_CASES_CLOSE,
    PERMISSION_CASES_CREATE,
    PERMISSION_DASHBOARD_VIEW,
    PERMISSION_GUESTS_MANAGE,
    PERMISSION_WORK_COMPLETE,
    PERMISSION_WORK_START,
)
from apps.users.services import AuthorizationService


class RequiredPermission(BasePermission):
    """Require one declared platform permission through the domain service."""

    required_permission: str | None = None

    def has_permission(self, request, view):
        AuthorizationService.check_permission(request.user.id, self.required_permission)
        return True


class AssignmentPermission(RequiredPermission):
    """Require a permission and ownership of the submitted Assignment."""

    def has_permission(self, request, view):
        assignment_id = request.data.get("assignment_id")
        if not isinstance(assignment_id, int) or assignment_id < 1:
            return True

        AuthorizationService.check_assignment_access(
            request.user.id,
            assignment_id,
            self.required_permission,
        )
        return True


class CasePermission(RequiredPermission):
    """Require a permission and access to the submitted Case."""

    check_permission_without_case = False

    def has_permission(self, request, view):
        case_id = getattr(view, "kwargs", {}).get("case_id", request.data.get("case_id"))
        if not isinstance(case_id, int) or case_id < 1:
            if self.check_permission_without_case:
                return super().has_permission(request, view)
            return True

        AuthorizationService.check_case_access(
            request.user.id,
            case_id,
            self.required_permission,
        )
        return True


class CanManageGuests(RequiredPermission):
    """Permit guest CRUD operations."""

    required_permission = PERMISSION_GUESTS_MANAGE


class CanListOrManageGuests(BasePermission):
    """Apply operational list access without changing Guest management access."""

    def has_permission(self, request, view):
        """Delegate GET and write requests to their established permissions."""

        permission = CanViewDashboard if request.method in SAFE_METHODS else CanManageGuests
        return permission().has_permission(request, view)


class CanCreateCases(RequiredPermission):
    """Permit Case creation from Requests."""

    required_permission = PERMISSION_CASES_CREATE


class CanViewDashboard(CasePermission):
    """Permit Employee operational dashboard access."""

    required_permission = PERMISSION_DASHBOARD_VIEW
    check_permission_without_case = True


class CanAssignCases(RequiredPermission):
    """Permit assigning Employees to Cases."""

    required_permission = PERMISSION_CASES_ASSIGN


class CanCloseCases(CasePermission):
    """Permit closing completed Cases."""

    required_permission = PERMISSION_CASES_CLOSE


class CanAcceptAssignments(AssignmentPermission):
    """Permit accepting the authenticated Employee's Assignment."""

    required_permission = PERMISSION_ASSIGNMENTS_ACCEPT


class CanStartWork(AssignmentPermission):
    """Permit starting work on the authenticated Employee's Assignment."""

    required_permission = PERMISSION_WORK_START


class CanCompleteWork(AssignmentPermission):
    """Permit completing the authenticated Employee's Assignment."""

    required_permission = PERMISSION_WORK_COMPLETE
