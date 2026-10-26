"""Domain exceptions raised by Employee assignment operations."""

from core.exceptions import DomainException


class CaseNotFound(DomainException):
    """Raised when a Case cannot be resolved for assignment."""

    default_message = "Case not found."
    default_http_status = 404


class EmployeeNotFound(DomainException):
    """Raised when an Employee cannot be resolved for assignment."""

    default_message = "Employee not found."
    default_http_status = 404


class CaseAlreadyAssigned(DomainException):
    """Raised when a Case already has an active Assignment."""

    default_message = "Case already has an active Assignment."
    default_http_status = 409


class AssignmentNotFound(DomainException):
    """Raised when an Assignment cannot be resolved for acceptance."""

    default_message = "Assignment not found."
    default_http_status = 404


class AssignmentNotAssigned(DomainException):
    """Raised when an Assignment cannot transition to accepted."""

    default_message = "Assignment is not assigned."
    default_http_status = 409


class AssignmentNotAccepted(DomainException):
    """Raised when an Assignment cannot transition to in-progress."""

    default_message = "Assignment is not accepted."
    default_http_status = 409


class AssignmentNotInProgress(DomainException):
    """Raised when an Assignment cannot transition to completed."""

    default_message = "Assignment is not in progress."
    default_http_status = 409


class AssignmentNotCompleted(DomainException):
    """Raised when an Assignment cannot transition to released."""

    default_message = "Assignment is not completed."
    default_http_status = 409


class CaseNotOpen(DomainException):
    """Raised when a Case cannot transition to in-progress."""

    default_message = "Case is not open."
    default_http_status = 409


class CaseNotInProgress(DomainException):
    """Raised when a Case cannot transition to completed."""

    default_message = "Case is not in progress."
    default_http_status = 409


class CaseNotCompleted(DomainException):
    """Raised when a Case cannot transition to closed."""

    default_message = "Case is not completed."
    default_http_status = 409


__all__ = [
    "AssignmentNotAccepted",
    "AssignmentNotAssigned",
    "AssignmentNotCompleted",
    "AssignmentNotInProgress",
    "AssignmentNotFound",
    "CaseAlreadyAssigned",
    "CaseNotFound",
    "CaseNotCompleted",
    "CaseNotInProgress",
    "CaseNotOpen",
    "EmployeeNotFound",
]
