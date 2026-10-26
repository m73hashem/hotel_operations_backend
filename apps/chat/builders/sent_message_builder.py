"""Builder for Send Message response DTOs."""

from apps.chat.dto import SentMessageDTO
from apps.chat.models import Message


class SentMessageBuilder:
    """Build a flat DTO from an already-persisted Chat Message."""

    @staticmethod
    def build(message: Message) -> SentMessageDTO:
        """Transform a Chat Message into its response DTO."""

        return SentMessageDTO(
            message_id=message.id,
            conversation_id=message.conversation_id,
            sender_type=message.sender_type,
            content=message.content,
            channel=message.channel,
            created_at=message.created_at,
        )
