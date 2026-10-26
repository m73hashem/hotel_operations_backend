"""Transport DTO for operational Case list rows."""

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class CaseListItemDTO:
    """Flat Case data returned by the operational Case list."""

    case_id: int
    request_id: int | None
    subject: str
    description: str
    status: str
    priority: str | None
    department_id: int | None
    department_name: str | None
    guest_name: str
    room_number: str
    created_at: datetime
    updated_at: datetime
