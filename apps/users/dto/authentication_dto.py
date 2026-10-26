"""Flat DTOs returned by employee authentication workflows."""

from dataclasses import dataclass


@dataclass(frozen=True)
class EmployeeLoginDTO:
    """Employee identity and JWT pair returned after login."""

    employee_id: int
    user_id: int
    full_name: str
    department_id: int
    access_token: str
    refresh_token: str


@dataclass(frozen=True)
class CurrentEmployeeDTO:
    """Authenticated Employee identity returned by the current-user endpoint."""

    employee_id: int
    user_id: int
    full_name: str
    department_id: int
    email: str


@dataclass(frozen=True)
class TokenRefreshDTO:
    """Access token returned after a valid refresh-token exchange."""

    access_token: str


@dataclass(frozen=True)
class LogoutDTO:
    """Confirmation returned after blacklisting a refresh token."""

    logged_out: bool
