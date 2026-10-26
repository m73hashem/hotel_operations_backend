"""Domain exceptions raised by Guest operations."""

from core.exceptions import DomainException


class GuestNotFound(DomainException):
    """Raised when a Guest cannot be resolved."""

    default_message = "Guest not found."
    default_http_status = 404


__all__ = ["GuestNotFound"]
