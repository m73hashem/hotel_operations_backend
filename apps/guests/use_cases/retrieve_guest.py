"""Application workflow for retrieving a Guest."""

from apps.guests.builders import GuestBuilder
from apps.guests.dto import GuestDTO
from apps.guests.services import GuestService


class RetrieveGuestUseCase:
    """Coordinate Guest retrieval and flat DTO construction."""

    @staticmethod
    def execute(guest_id: int) -> GuestDTO:
        """Return one Guest as a flat response DTO."""

        return GuestBuilder.build(GuestService.get_guest(guest_id))
