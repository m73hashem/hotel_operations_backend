"""Builder for Create Request response DTOs."""

from apps.chat.dto import RequestCreationDTO
from apps.chat.models import Request


class RequestCreationBuilder:
    """Build a flat DTO from an already-persisted Request."""

    @staticmethod
    def build(request_record: Request) -> RequestCreationDTO:
        """Transform a Request into its response DTO."""

        return RequestCreationDTO(
            request_id=request_record.id,
            status=request_record.status,
            title=request_record.title,
            created_at=request_record.created_at,
        )
