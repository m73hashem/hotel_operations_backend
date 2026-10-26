"""DTO returned after closing a Case."""

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class CaseClosureDTO:
    """Flat representation of a closed Case and released Assignment."""

    case_id: int
    assignment_id: int
    case_status: str
    assignment_status: str
    closed_at: datetime
