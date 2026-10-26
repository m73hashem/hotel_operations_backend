"""DTOs for an Employee's assignment list."""

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class MyAssignmentDTO:
    """Immutable assignment item for the authenticated Employee."""

    assignment_id: int
    case_id: int
    request_title: str
    room_number: str
    priority: str | None
    assignment_status: str
    case_status: str
    assigned_at: datetime


@dataclass(frozen=True)
class MyAssignmentsDTO:
    """Immutable collection of an Employee's assignments."""

    assignments: tuple[MyAssignmentDTO, ...]
