"""Application workflow for listing Guests."""

from apps.guests.builders import GuestBuilder
from apps.guests.dto import GuestDTO
from apps.guests.services import GuestService


class ListGuestsUseCase:
    """Coordinate Guest retrieval and flat DTO construction."""

    @staticmethod
    def execute(user_id: int, **query_params) -> list[GuestDTO]:
        """Return all Guests as flat response DTOs."""

        return GuestBuilder.build_list(GuestService.list_guests(user_id, **query_params))
