"""DTO returned after assigning a Case."""

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class CaseAssignmentDTO:
    """Flat representation of a newly created Assignment."""

    assignment_id: int
    case_id: int
    employee_id: int
    status: str
    assigned_at: datetime
