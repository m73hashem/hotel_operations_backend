from types import SimpleNamespace
from unittest.mock import Mock, patch

from django.test import SimpleTestCase
from rest_framework_simplejwt.exceptions import TokenError

from apps.users.exceptions import (
    EmployeeAccountNotFound,
    InactiveEmployee,
    InvalidCredentials,
    InvalidRefreshToken,
)
from apps.users.services import EmployeeAuthenticationService, TokenManagementService


class EmployeeAuthenticationServiceTests(SimpleTestCase):
    """Unit tests for employee login validation."""

    @patch("apps.users.services.authentication_service.RefreshToken.for_user")
    @patch(
        "apps.users.services.authentication_service."
        "EmployeeSelector.get_by_user_id_for_authentication",
    )
    @patch("apps.users.services.authentication_service.authenticate")
    def test_authenticate_employee_returns_active_employee_and_tokens(
        self,
        authenticate,
        get_employee,
        refresh_for_user,
    ):
        """An authenticated active Employee receives a JWT pair."""

        user = SimpleNamespace(id=1)
        employee = SimpleNamespace(status="ACTIVE")
        refresh = Mock()
        refresh.access_token = "access-token"
        authenticate.return_value = user
        get_employee.return_value = employee
        refresh_for_user.return_value = refresh
        refresh.__str__ = Mock(return_value="refresh-token")

        result = EmployeeAuthenticationService.authenticate_employee("employee", "password")

        self.assertEqual(result, (employee, "access-token", "refresh-token"))
        get_employee.assert_called_once_with(1)

    @patch("apps.users.services.authentication_service.authenticate", return_value=None)
    def test_authenticate_employee_rejects_invalid_credentials(self, authenticate):
        """Django authentication failure becomes a domain exception."""

        with self.assertRaises(InvalidCredentials):
            EmployeeAuthenticationService.authenticate_employee("employee", "wrong")

        authenticate.assert_called_once_with(username="employee", password="wrong")

    @patch(
        "apps.users.services.authentication_service."
        "EmployeeSelector.get_by_user_id_for_authentication",
        return_value=None,
    )
    def test_get_current_employee_rejects_user_without_employee(self, get_employee):
        """Guests and other non-employees cannot use employee endpoints."""

        with self.assertRaises(EmployeeAccountNotFound):
            EmployeeAuthenticationService.get_current_employee(1)

        get_employee.assert_called_once_with(1)

    @patch(
        "apps.users.services.authentication_service."
        "EmployeeSelector.get_by_user_id_for_authentication",
        return_value=SimpleNamespace(status="INACTIVE"),
    )
    def test_get_current_employee_rejects_inactive_employee(self, get_employee):
        """Inactive Employee profiles are denied access."""

        with self.assertRaises(InactiveEmployee):
            EmployeeAuthenticationService.get_current_employee(1)

        get_employee.assert_called_once_with(1)


class TokenManagementServiceTests(SimpleTestCase):
    """Unit tests for Simple JWT refresh and blacklist delegation."""

    @patch("apps.users.services.token_management_service.RefreshToken")
    def test_refresh_returns_new_access_token(self, refresh_token):
        """A valid refresh token produces its access token."""

        token = Mock()
        token.access_token = "new-access"
        refresh_token.return_value = token

        self.assertEqual(TokenManagementService.refresh_access_token("refresh"), "new-access")

    @patch("apps.users.services.token_management_service.RefreshToken")
    def test_logout_blacklists_valid_refresh_token(self, refresh_token):
        """Logout delegates blacklisting to Simple JWT."""

        token = Mock()
        refresh_token.return_value = token

        TokenManagementService.blacklist_refresh_token("refresh")

        token.blacklist.assert_called_once_with()

    @patch(
        "apps.users.services.token_management_service.RefreshToken",
        side_effect=TokenError("invalid"),
    )
    def test_token_operations_reject_invalid_refresh_token(self, refresh_token):
        """Simple JWT token failures become domain exceptions."""

        with self.assertRaises(InvalidRefreshToken):
            TokenManagementService.refresh_access_token("invalid")

        refresh_token.assert_called_once_with("invalid")
