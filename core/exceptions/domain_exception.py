"""Shared contract for application domain exceptions."""


class DomainException(Exception):
    """Base exception carrying a client-safe message and HTTP status."""

    default_message = "Domain error."
    default_http_status = 400

    def __init__(
        self,
        message: str | None = None,
        http_status: int | None = None,
    ):
        self.message = message if message is not None else self.default_message
        self.http_status = (
            http_status
            if http_status is not None
            else self.default_http_status
        )
        super().__init__(self.message)
