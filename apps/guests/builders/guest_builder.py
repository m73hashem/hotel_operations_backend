"""Builder for Guest response DTOs."""

from collections.abc import Sequence

from apps.guests.dto import GuestDTO
from apps.guests.models import Guest


class GuestBuilder:
    """Build flat DTOs from already-loaded Guest objects."""

    @staticmethod
    def build(guest: Guest) -> GuestDTO:
        """Transform one Guest into its response DTO."""

        return GuestDTO(
            id=guest.id,
            created_at=guest.created_at,
            updated_at=guest.updated_at,
            first_name=guest.first_name,
            last_name=guest.last_name,
            phone=guest.phone,
            email=guest.email,
            language=guest.language,
        )

    @classmethod
    def build_list(cls, guests: Sequence[Guest]) -> list[GuestDTO]:
        """Transform already-loaded Guests into response DTOs."""

        return [cls.build(guest) for guest in guests]
