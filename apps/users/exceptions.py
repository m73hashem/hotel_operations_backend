"""Domain exceptions raised by employee authentication workflows."""

from core.exceptions import DomainException


class InvalidCredentials(DomainException):
    """Raised when login credentials cannot authenticate a User."""

    default_message = "Invalid username or password."
    default_http_status = 401


class EmployeeAccountNotFound(DomainException):
    """Raised when an authenticated User has no related Employee profile."""

    default_message = "Employee account not found."
    default_http_status = 404


class InactiveEmployee(DomainException):
    """Raised when an Employee profile is not active."""

    default_message = "Employee account is inactive."
    default_http_status = 403


class InvalidRefreshToken(DomainException):
    """Raised when a refresh token is invalid or cannot be used."""

    default_message = "Invalid refresh token."
    default_http_status = 401


class PermissionDenied(DomainException):
    """Raised when an Employee lacks a required platform permission."""

    default_message = "You do not have permission to perform this action."
    default_http_status = 403


class DepartmentAccessDenied(DomainException):
    """Raised when an Employee cannot access another department's data."""

    default_message = "You do not have access to this department."
    default_http_status = 403


class CaseAccessDenied(DomainException):
    """Raised when an Employee cannot access the requested Case."""

    default_message = "You do not have access to this case."
    default_http_status = 403


class AssignmentAccessDenied(DomainException):
    """Raised when an Employee cannot access the requested Assignment."""

    default_message = "You do not have access to this assignment."
    default_http_status = 403
