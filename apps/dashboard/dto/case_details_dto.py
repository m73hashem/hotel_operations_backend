"""DTOs for the dashboard Case details screen."""

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class TimelineEventDTO:
    """Immutable timeline event transport data."""

    event_type: str
    timestamp: datetime


@dataclass(frozen=True)
class ConversationMessageDTO:
    """Immutable Case conversation message transport data."""

    message_id: int
    sender: str
    message: str
    created_at: datetime


@dataclass(frozen=True)
class RequestInformationDTO:
    """Immutable original guest Request transport data."""

    request_id: int | None
    category: str | None
    title: str
    description: str
    created_at: datetime | None


@dataclass(frozen=True)
class CaseDetailsDTO:
    """Immutable Case details response for the employee dashboard."""

    case_id: int
    request_id: int | None
    request_title: str
    request_description: str
    case_status: str
    priority: str | None
    created_at: datetime
    closed_at: datetime | None
    department: str | None
    assigned_employee: str | None
    guest_name: str
    room_number: str
    timeline: tuple[TimelineEventDTO, ...]
    conversation: tuple[ConversationMessageDTO, ...]
    request_information: RequestInformationDTO
