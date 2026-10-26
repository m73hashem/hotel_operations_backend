"""Application workflow for operational Request list retrieval."""

from apps.requests.builders import RequestListBuilder
from apps.requests.dto import RequestListItemDTO
from apps.requests.services.request_listing_service import RequestListingService


class ListRequestsUseCase:
    """Coordinate Request retrieval and DTO mapping."""

    @staticmethod
    def execute(user_id: int, **query_params) -> tuple[RequestListItemDTO, ...]:
        """Return immutable Request list DTOs for one Employee context."""

        requests = RequestListingService.get_operational_requests(user_id, **query_params)
        return RequestListBuilder.build(requests)
