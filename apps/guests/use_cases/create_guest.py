"""Application workflow for creating a Guest."""

from collections.abc import Mapping

from apps.guests.builders import GuestBuilder
from apps.guests.dto import GuestDTO
from apps.guests.services import GuestService


class CreateGuestUseCase:
    """Coordinate Guest creation and flat DTO construction."""

    @staticmethod
    def execute(validated_data: Mapping[str, object]) -> GuestDTO:
        """Create one Guest and return its response DTO."""

        return GuestBuilder.build(GuestService.create_guest(validated_data))
