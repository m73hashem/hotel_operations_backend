from types import SimpleNamespace
from unittest.mock import patch

from django.test import SimpleTestCase

from apps.users.permissions import CanAcceptAssignments, CanCloseCases, CanManageGuests


class AuthorizationPermissionTests(SimpleTestCase):
    """Tests for thin DRF permission adapters."""

    @patch("apps.users.permissions.AuthorizationService.check_permission")
    def test_required_permission_delegates_to_authorization_service(self, check_permission):
        """A simple endpoint permission delegates policy to the domain service."""

        request = SimpleNamespace(user=SimpleNamespace(id=1))

        self.assertTrue(CanManageGuests().has_permission(request, SimpleNamespace()))
        check_permission.assert_called_once_with(1, "guests.manage")

    @patch("apps.users.permissions.AuthorizationService.check_assignment_access")
    def test_assignment_permission_delegates_resource_access(self, check_assignment_access):
        """Assignment endpoints include their submitted resource identifier."""

        request = SimpleNamespace(user=SimpleNamespace(id=1), data={"assignment_id": 2})

        self.assertTrue(CanAcceptAssignments().has_permission(request, SimpleNamespace()))
        check_assignment_access.assert_called_once_with(1, 2, "assignments.accept")

    @patch("apps.users.permissions.AuthorizationService.check_assignment_access")
    def test_assignment_permission_leaves_invalid_shape_to_serializer(self, check_access):
        """Permission adapters do not duplicate serializer request validation."""

        request = SimpleNamespace(user=SimpleNamespace(id=1), data={})

        self.assertTrue(CanAcceptAssignments().has_permission(request, SimpleNamespace()))
        check_access.assert_not_called()

    @patch("apps.users.permissions.AuthorizationService.check_case_access")
    def test_case_permission_delegates_resource_access(self, check_case_access):
        """Case endpoints include their submitted resource identifier."""

        request = SimpleNamespace(user=SimpleNamespace(id=1), data={"case_id": 2})

        self.assertTrue(CanCloseCases().has_permission(request, SimpleNamespace()))
        check_case_access.assert_called_once_with(1, 2, "cases.close")
