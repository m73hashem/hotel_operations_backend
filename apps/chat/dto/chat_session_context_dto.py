"""DTOs used by Chat use cases."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ChatSessionContextDTO:
    """Flat chat context returned after a guest starts a chat session."""

    conversation_id: int
    conversation_type: str
    conversation_status: str
    guest_id: int
    guest_first_name: str
    guest_last_name: str
    guest_language: str
    stay_id: int
    room_id: int
    room_number: str
    room_type: str
    hotel_id: int
    hotel_name: str
    hotel_timezone: str
