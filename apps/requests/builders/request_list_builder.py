"""Map operational Requests into transport DTOs."""

from collections.abc import Iterable

from apps.chat.models import Request
from apps.requests.dto import RequestListItemDTO


class RequestListBuilder:
    """Build flat DTOs from already-loaded Request objects."""

    @staticmethod
    def build(requests: Iterable[Request]) -> tuple[RequestListItemDTO, ...]:
        """Map operational Requests into immutable list DTOs."""

        return tuple(
            RequestListItemDTO(
                request_id=request.id,
                title=request.title,
                original_message=request.original_message,
                status=request.status,
                source=request.source,
                guest_name=f"{request.guest.first_name} {request.guest.last_name}",
                room_number=request.room.room_number,
                created_at=request.created_at,
                updated_at=request.updated_at,
            )
            for request in requests
        )
