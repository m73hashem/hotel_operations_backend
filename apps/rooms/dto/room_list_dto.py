"""Transport DTO for operational Room list rows."""

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class RoomListItemDTO:
    """Flat Room data returned by the operational Room list."""

    room_id: int
    hotel_id: int
    hotel_name: str
    room_number: str
    room_type: str
    status: str
    created_at: datetime
    updated_at: datetime
