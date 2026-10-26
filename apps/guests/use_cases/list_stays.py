"""Application workflow for operational Stay list retrieval."""

from apps.guests.builders.stay_list_builder import StayListBuilder
from apps.guests.dto.stay_list_dto import StayListItemDTO
from apps.guests.services.stay_listing_service import StayListingService


class ListStaysUseCase:
    """Coordinate Stay retrieval and DTO mapping."""

    @staticmethod
    def execute(user_id: int, **query_params) -> tuple[StayListItemDTO, ...]:
        """Return immutable Stay list DTOs for one Employee context."""

        stays = StayListingService.get_operational_stays(user_id, **query_params)
        return StayListBuilder.build(stays)
