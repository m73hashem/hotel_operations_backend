"""Application workflow for reading a guest's Conversation History."""

from apps.chat.builders import ConversationHistoryBuilder
from apps.chat.dto import ConversationHistoryDTO
from apps.chat.services import GeneralConversationService, GuestChatAccessService


class ConversationHistoryUseCase:
    """Coordinate guest access validation and active Conversation history retrieval."""

    @staticmethod
    def execute(session_token: str) -> ConversationHistoryDTO:
        """Return messages from the Stay's active General Conversation."""

        guest_session = GuestChatAccessService.validate_access(session_token)
        messages = GeneralConversationService.get_active_general_conversation_history(
            guest_session.stay,
        )

        return ConversationHistoryBuilder.build(messages)
