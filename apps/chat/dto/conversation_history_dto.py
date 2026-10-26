"""DTO returned for Conversation History."""

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ConversationHistoryDTO:
    """Message history for the active General Conversation."""

    messages: list[dict[str, Any]]
