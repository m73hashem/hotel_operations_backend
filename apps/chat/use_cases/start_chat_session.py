"""Application workflow for starting a guest chat session."""

from apps.chat.builders import ChatSessionContextBuilder
from apps.chat.dto import ChatSessionContextDTO
from apps.chat.services import (
    GeneralConversationService,
    GuestChatAccessService,
)


class StartChatSessionUseCase:
    """Coordinate guest chat access, conversation retrieval, and DTO building."""

    @staticmethod
    def execute(session_token: str) -> ChatSessionContextDTO:
        """Start a chat session and return its flat context DTO."""

        guest_session = GuestChatAccessService.validate_access(session_token)
        stay = guest_session.stay
        conversation = (
            GeneralConversationService.get_or_create_active_general_conversation(
                stay,
            )
        )

        return ChatSessionContextBuilder.build(
            conversation=conversation,
            guest=stay.guest,
            stay=stay,
            room=stay.room,
            hotel=stay.room.hotel,
        )
