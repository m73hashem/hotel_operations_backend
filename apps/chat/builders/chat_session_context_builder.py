"""Builders for Chat response DTOs."""

from apps.chat.dto import ChatSessionContextDTO
from apps.chat.models import Conversation
from apps.guests.models import Guest, Stay
from apps.rooms.models import Hotel, Room


class ChatSessionContextBuilder:
    """Build flat chat session context DTOs from already-loaded domain objects."""

    @staticmethod
    def build(
        conversation: Conversation,
        guest: Guest,
        stay: Stay,
        room: Room,
        hotel: Hotel,
    ) -> ChatSessionContextDTO:
        """Transform domain objects into a flat chat session context DTO."""

        return ChatSessionContextDTO(
            conversation_id=conversation.pk,
            conversation_type=conversation.type,
            conversation_status=conversation.status,
            guest_id=guest.pk,
            guest_first_name=guest.first_name,
            guest_last_name=guest.last_name,
            guest_language=guest.language,
            stay_id=stay.pk,
            room_id=room.pk,
            room_number=room.room_number,
            room_type=room.room_type,
            hotel_id=hotel.pk,
            hotel_name=hotel.name,
            hotel_timezone=hotel.timezone,
        )
