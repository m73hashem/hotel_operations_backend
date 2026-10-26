"""DTO returned after accepting an Assignment."""

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class AssignmentAcceptanceDTO:
    """Flat representation of an accepted Assignment."""

    assignment_id: int
    case_id: int
    employee_id: int
    status: str
    accepted_at: datetime
