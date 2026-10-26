"""Application workflow for updating a Guest."""

from collections.abc import Mapping

from apps.guests.builders import GuestBuilder
from apps.guests.dto import GuestDTO
from apps.guests.services import GuestService


class UpdateGuestUseCase:
    """Coordinate Guest updates and flat DTO construction."""

    @staticmethod
    def execute(guest_id: int, validated_data: Mapping[str, object]) -> GuestDTO:
        """Update one Guest and return its response DTO."""

        return GuestBuilder.build(GuestService.update_guest(guest_id, validated_data))
