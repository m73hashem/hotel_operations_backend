"""Map operational Stays into transport DTOs."""

from collections.abc import Iterable

from apps.guests.dto.stay_list_dto import StayListItemDTO
from apps.guests.models import Stay


class StayListBuilder:
    """Build flat DTOs from already-loaded Stay objects."""

    @staticmethod
    def build(stays: Iterable[Stay]) -> tuple[StayListItemDTO, ...]:
        """Map operational Stays into immutable list DTOs."""

        return tuple(
            StayListItemDTO(
                stay_id=stay.id,
                guest_id=stay.guest_id,
                guest_name=f"{stay.guest.first_name} {stay.guest.last_name}",
                room_id=stay.room_id,
                room_number=stay.room.room_number,
                status=stay.status,
                check_in=stay.check_in,
                expected_check_out=stay.expected_check_out,
                actual_check_out=stay.actual_check_out,
                created_at=stay.created_at,
                updated_at=stay.updated_at,
            )
            for stay in stays
        )
