"""Domain exceptions raised by Chat business operations."""

from core.exceptions import DomainException


class InvalidGuestSession(DomainException):
    """Raised when a guest session token cannot be resolved."""

    default_message = "Invalid guest session."
    default_http_status = 401


class ExpiredGuestSession(DomainException):
    """Raised when a guest session has expired."""

    default_message = "Guest session has expired."
    default_http_status = 401


class InactiveGuestSession(DomainException):
    """Raised when a guest session is not active."""

    default_message = "Guest session is inactive."
    default_http_status = 401


class InactiveStay(DomainException):
    """Raised when a guest session is linked to an inactive Stay."""

    default_message = "Stay is inactive."
    default_http_status = 403


class ActiveGeneralConversationNotFound(DomainException):
    """Raised when a Stay has no active General Conversation."""

    default_message = "Active General Conversation not found."
    default_http_status = 404

__all__ = [
    "ActiveGeneralConversationNotFound",
    "ExpiredGuestSession",
    "InactiveGuestSession",
    "InactiveStay",
    "InvalidGuestSession",
]
