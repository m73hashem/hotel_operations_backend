from types import SimpleNamespace
from unittest.mock import Mock, patch

from django.test import SimpleTestCase

from apps.users.builders import AuthenticationBuilder
from apps.users.dto import (
    CurrentEmployeeDTO,
    EmployeeLoginDTO,
    LogoutDTO,
    TokenRefreshDTO,
)
from apps.users.exceptions import InvalidCredentials
from apps.users.use_cases.current_employee import CurrentEmployeeUseCase
from apps.users.use_cases.employee_login import EmployeeLoginUseCase
from apps.users.use_cases.logout import LogoutUseCase
from apps.users.use_cases.refresh_token import RefreshTokenUseCase


class AuthenticationUseCaseTests(SimpleTestCase):
    """Unit tests for authentication use-case orchestration."""

    @patch("apps.users.use_cases.employee_login.AuthenticationBuilder.build_login")
    @patch(
        "apps.users.use_cases.employee_login."
        "EmployeeAuthenticationService.authenticate_employee",
    )
    def test_login_coordinates_service_and_builder(self, authenticate_employee, build_login):
        """Login authenticates before building the response DTO."""

        employee = SimpleNamespace()
        dto = Mock(spec=EmployeeLoginDTO)
        authenticate_employee.return_value = (employee, "access", "refresh")
        build_login.return_value = dto

        result = EmployeeLoginUseCase.execute("employee", "password")

        self.assertIs(result, dto)
        authenticate_employee.assert_called_once_with("employee", "password")
        build_login.assert_called_once_with(
            employee,
            access_token="access",
            refresh_token="refresh",
        )

    @patch(
        "apps.users.use_cases.employee_login."
        "EmployeeAuthenticationService.authenticate_employee",
    )
    def test_login_propagates_domain_exception(self, authenticate_employee):
        """Login domain exceptions are handled only by the global handler."""

        error = InvalidCredentials()
        authenticate_employee.side_effect = error

        with self.assertRaises(InvalidCredentials) as raised:
            EmployeeLoginUseCase.execute("employee", "wrong-password")

        self.assertIs(raised.exception, error)

    @patch("apps.users.use_cases.current_employee.AuthenticationBuilder.build_current_employee")
    @patch(
        "apps.users.use_cases.current_employee."
        "EmployeeAuthenticationService.get_current_employee",
    )
    def test_current_employee_coordinates_service_and_builder(self, get_current_employee, build):
        """Current-user retrieval delegates to the authentication service."""

        employee = SimpleNamespace()
        dto = Mock(spec=CurrentEmployeeDTO)
        get_current_employee.return_value = employee
        build.return_value = dto

        self.assertIs(CurrentEmployeeUseCase.execute(1), dto)
        get_current_employee.assert_called_once_with(1)
        build.assert_called_once_with(employee)

    @patch("apps.users.use_cases.refresh_token.AuthenticationBuilder.build_refresh")
    @patch(
        "apps.users.use_cases.refresh_token.TokenManagementService.refresh_access_token",
    )
    def test_refresh_coordinates_service_and_builder(self, refresh_access_token, build):
        """Refresh delegates JWT handling to the token management service."""

        dto = Mock(spec=TokenRefreshDTO)
        refresh_access_token.return_value = "new-access"
        build.return_value = dto

        self.assertIs(RefreshTokenUseCase.execute("refresh"), dto)
        refresh_access_token.assert_called_once_with("refresh")
        build.assert_called_once_with("new-access")

    @patch("apps.users.use_cases.logout.AuthenticationBuilder.build_logout")
    @patch(
        "apps.users.use_cases.logout.TokenManagementService.blacklist_refresh_token",
    )
    def test_logout_coordinates_service_and_builder(self, blacklist_refresh_token, build):
        """Logout blacklists the refresh token before building its confirmation DTO."""

        dto = Mock(spec=LogoutDTO)
        build.return_value = dto

        self.assertIs(LogoutUseCase.execute("refresh"), dto)
        blacklist_refresh_token.assert_called_once_with("refresh")
        build.assert_called_once_with()


class AuthenticationBuilderTests(SimpleTestCase):
    """Unit tests for flat authentication DTO construction."""

    def setUp(self):
        self.employee = SimpleNamespace(
            id=10,
            user_id=20,
            name="Amina Al Saud",
            department_id=30,
            user=SimpleNamespace(email="amina@example.com"),
        )

    def test_build_login_returns_flat_employee_login_dto(self):
        """Login DTO contains identity fields and JWT strings only."""

        dto = AuthenticationBuilder.build_login(
            self.employee,
            access_token="access",
            refresh_token="refresh",
        )

        self.assertEqual(dto, EmployeeLoginDTO(10, 20, "Amina Al Saud", 30, "access", "refresh"))

    def test_build_current_employee_returns_flat_dto(self):
        """Current employee DTO exposes no ORM object."""

        dto = AuthenticationBuilder.build_current_employee(self.employee)

        self.assertEqual(
            dto,
            CurrentEmployeeDTO(10, 20, "Amina Al Saud", 30, "amina@example.com"),
        )

    def test_build_token_dtos_returns_flat_values(self):
        """Token response DTOs contain only client-facing primitive values."""

        self.assertEqual(AuthenticationBuilder.build_refresh("access"), TokenRefreshDTO("access"))
        self.assertEqual(AuthenticationBuilder.build_logout(), LogoutDTO(True))
