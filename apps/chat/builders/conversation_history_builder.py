"""Builder for Conversation History response DTOs."""

from collections.abc import Sequence

from apps.chat.dto import ConversationHistoryDTO
from apps.chat.models import Message


class ConversationHistoryBuilder:
    """Build a message-history DTO from already-loaded Chat Messages."""

    @staticmethod
    def build(messages: Sequence[Message]) -> ConversationHistoryDTO:
        """Transform loaded Chat Messages into a history response DTO."""

        return ConversationHistoryDTO(
            messages=[
                {
                    "id": message.id,
                    "sender_type": message.sender_type,
                    "content": message.content,
                    "channel": message.channel,
                    "created_at": message.created_at,
                }
                for message in messages
            ],
        )
