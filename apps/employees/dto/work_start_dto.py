"""DTO returned after starting work on an Assignment."""

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class WorkStartDTO:
    """Flat representation of an Assignment and Case started together."""

    assignment_id: int
    case_id: int
    assignment_status: str
    case_status: str
    started_at: datetime
