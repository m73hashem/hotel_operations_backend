"""Application workflow for sending a guest Chat message."""

from apps.chat.builders import SentMessageBuilder
from apps.chat.dto import SentMessageDTO
from apps.chat.services import (
    GeneralConversationService,
    GuestChatAccessService,
    GuestMessageService,
)


class SendMessageUseCase:
    """Coordinate guest access, General Conversation retrieval, and message storage."""

    @staticmethod
    def execute(session_token: str, message: str) -> SentMessageDTO:
        """Persist one guest message and return its flat response DTO."""

        guest_session = GuestChatAccessService.validate_access(session_token)
        stay = guest_session.stay
        conversation = (
            GeneralConversationService.get_or_create_active_general_conversation(
                stay,
            )
        )
        persisted_message = GuestMessageService.send_to_general_conversation(
            conversation=conversation,
            guest_id=stay.guest.id,
            content=message,
        )

        return SentMessageBuilder.build(persisted_message)
