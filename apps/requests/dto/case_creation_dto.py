"""DTO returned after creating an operational Case."""

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class CaseCreationDTO:
    """Flat representation of a newly created Case and Conversation."""

    case_id: int
    request_id: int
    conversation_id: int
    status: str
    subject: str
    created_at: datetime
