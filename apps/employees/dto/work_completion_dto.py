"""DTO returned after completing work on an Assignment."""

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class WorkCompletionDTO:
    """Flat representation of an Assignment and Case completed together."""

    assignment_id: int
    case_id: int
    assignment_status: str
    case_status: str
    completed_at: datetime
