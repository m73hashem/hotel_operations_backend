from types import SimpleNamespace
from unittest.mock import patch

from django.test import SimpleTestCase

from apps.users.constants import (
    PERMISSION_ASSIGNMENTS_ACCEPT,
    PERMISSION_CASES_CREATE,
    ROLE_HOUSEKEEPING,
    ROLE_RECEPTION,
)
from apps.users.exceptions import (
    AssignmentAccessDenied,
    DepartmentAccessDenied,
    PermissionDenied,
)
from apps.users.services import AuthorizationService


class AuthorizationServiceTests(SimpleTestCase):
    """Tests for role and ownership authorization business rules."""

    def employee(self, *, department_id=1, is_superuser=False):
        """Return a loaded Employee-shaped object for selector mocks."""

        return SimpleNamespace(
            id=10,
            user_id=20,
            department_id=department_id,
            user=SimpleNamespace(is_superuser=is_superuser),
        )

    @patch("apps.users.services.authorization_service.AuthorizationSelector.get_employee_and_roles")
    def test_check_permission_accepts_permission_from_role_matrix(self, get_employee):
        """Reception can create Cases under the declared permission matrix."""

        get_employee.return_value = (self.employee(), (ROLE_RECEPTION,))

        AuthorizationService.check_permission(20, PERMISSION_CASES_CREATE)

        get_employee.assert_called_once_with(20)

    @patch("apps.users.services.authorization_service.AuthorizationSelector.get_employee_and_roles")
    def test_check_permission_rejects_missing_permission(self, get_employee):
        """A role cannot perform operations absent from its permission matrix."""

        get_employee.return_value = (self.employee(), (ROLE_RECEPTION,))

        with self.assertRaises(PermissionDenied):
            AuthorizationService.check_permission(20, PERMISSION_ASSIGNMENTS_ACCEPT)

    @patch("apps.users.services.authorization_service.AuthorizationSelector.get_employee_and_roles")
    def test_check_department_access_rejects_cross_department_employee(self, get_employee):
        """Non-management Employees cannot access another department."""

        get_employee.return_value = (self.employee(department_id=1), (ROLE_HOUSEKEEPING,))

        with self.assertRaises(DepartmentAccessDenied):
            AuthorizationService.check_department_access(20, 2)

    @patch("apps.users.services.authorization_service.AuthorizationSelector.get_assignment_for_access")
    @patch("apps.users.services.authorization_service.AuthorizationSelector.get_employee_and_roles")
    def test_check_assignment_access_requires_assigned_employee(
        self,
        get_employee,
        get_assignment,
    ):
        """Department colleagues cannot operate another Employee's Assignment."""

        get_employee.return_value = (self.employee(), (ROLE_HOUSEKEEPING,))
        get_assignment.return_value = SimpleNamespace(
            employee=SimpleNamespace(user_id=99, department_id=1),
        )

        with self.assertRaises(AssignmentAccessDenied):
            AuthorizationService.check_assignment_access(
                20,
                30,
                PERMISSION_ASSIGNMENTS_ACCEPT,
            )

    @patch("apps.users.services.authorization_service.AuthorizationSelector.get_assignment_for_access")
    @patch("apps.users.services.authorization_service.AuthorizationSelector.get_employee_and_roles")
    def test_check_assignment_access_accepts_owned_department_assignment(
        self,
        get_employee,
        get_assignment,
    ):
        """An assigned Employee can operate their own department Assignment."""

        get_employee.return_value = (self.employee(), (ROLE_HOUSEKEEPING,))
        get_assignment.return_value = SimpleNamespace(
            employee=SimpleNamespace(user_id=20, department_id=1),
        )

        AuthorizationService.check_assignment_access(
            20,
            30,
            PERMISSION_ASSIGNMENTS_ACCEPT,
        )
