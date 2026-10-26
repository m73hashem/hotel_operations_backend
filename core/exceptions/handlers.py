from django.conf import settings
from rest_framework.views import exception_handler

from core.exceptions.domain_exception import DomainException
from core.responses import ApiResponse


def custom_exception_handler(exc, context):
    """Translate DRF and supported domain exceptions into API envelopes."""

    if isinstance(exc, DomainException):
        return ApiResponse.error(
            message=exc.message,
            status=exc.http_status,
        )

    response = exception_handler(exc, context)

    if response is None:
        if settings.DEBUG:
            raise exc

        return ApiResponse.error(
            message="Internal Server Error",
            status=500,
        )

    return ApiResponse.error(
        message="Validation Error",
        errors=response.data,
        status=response.status_code,
    )
