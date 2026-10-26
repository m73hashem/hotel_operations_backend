"""Builder for operational Room list DTOs."""

from collections.abc import Iterable

from apps.rooms.dto import RoomListItemDTO
from apps.rooms.models import Room


class RoomListBuilder:
    """Map already-loaded Room objects into immutable DTOs."""

    @staticmethod
    def build(rooms: Iterable[Room]) -> tuple[RoomListItemDTO, ...]:
        """Map Rooms into flat transport data without ORM operations."""

        return tuple(
            RoomListItemDTO(
                room_id=room.id,
                hotel_id=room.hotel_id,
                hotel_name=room.hotel.name,
                room_number=room.room_number,
                room_type=room.room_type,
                status=room.status,
                created_at=room.created_at,
                updated_at=room.updated_at,
            )
            for room in rooms
        )
