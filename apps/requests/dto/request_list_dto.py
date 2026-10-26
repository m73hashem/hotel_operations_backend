"""Transport DTO for operational Request list rows."""

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class RequestListItemDTO:
    """Flat Request data returned by the operational Request list."""

    request_id: int
    title: str
    original_message: str
    status: str
    source: str
    guest_name: str
    room_number: str
    created_at: datetime
    updated_at: datetime
