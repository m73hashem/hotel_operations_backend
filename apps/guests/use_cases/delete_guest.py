"""Application workflow for deleting a Guest."""

from apps.guests.services import GuestService


class DeleteGuestUseCase:
    """Coordinate Guest deletion."""

    @staticmethod
    def execute(guest_id: int) -> None:
        """Delete one Guest after domain validation."""

        GuestService.delete_guest(guest_id)
