"""DTOs for a department's Case queue."""

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class DepartmentQueueItemDTO:
    """Immutable Case item shown in a department queue."""

    case_id: int
    request_title: str
    room_number: str
    priority: str | None
    current_status: str
    created_at: datetime


@dataclass(frozen=True)
class DepartmentQueueDTO:
    """Immutable collection of department queue Cases."""

    cases: tuple[DepartmentQueueItemDTO, ...]
