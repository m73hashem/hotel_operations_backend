"""Application workflow for operational Room listing."""

from apps.rooms.builders import RoomListBuilder
from apps.rooms.dto import RoomListItemDTO
from apps.rooms.services import RoomListingService


class ListRoomsUseCase:
    """Coordinate Room retrieval and flat DTO construction."""

    @staticmethod
    def execute(user_id: int, **query_params) -> tuple[RoomListItemDTO, ...]:
        """Return filtered Rooms as immutable response DTOs."""

        rooms = RoomListingService.get_operational_rooms(user_id, **query_params)
        return RoomListBuilder.build(rooms)
