"""DTO returned after a guest sends a Chat message."""

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class SentMessageDTO:
    """Flat representation of a persisted guest message."""

    message_id: int
    conversation_id: int
    sender_type: str
    content: str
    channel: str
    created_at: datetime
