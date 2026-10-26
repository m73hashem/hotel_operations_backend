"""Domain exceptions raised by Request business operations."""

from core.exceptions import DomainException


class RequestNotFound(DomainException):
    """Raised when a Request cannot be resolved."""

    default_message = "Request not found."
    default_http_status = 404


class CaseAlreadyExistsForRequest(DomainException):
    """Raised when a Request already has an operational Case."""

    default_message = "A Case already exists for this Request."
    default_http_status = 409


__all__ = [
    "CaseAlreadyExistsForRequest",
    "RequestNotFound",
]
