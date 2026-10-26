"""Transport DTO for operational Stay list rows."""

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class StayListItemDTO:
    """Flat Stay data returned by the operational Stay list."""

    stay_id: int
    guest_id: int
    guest_name: str
    room_id: int
    room_number: str
    status: str
    check_in: datetime
    expected_check_out: datetime
    actual_check_out: datetime | None
    created_at: datetime
    updated_at: datetime
