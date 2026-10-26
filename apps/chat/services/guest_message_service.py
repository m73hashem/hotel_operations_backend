"""Business capability for persisting guest Chat messages."""

from apps.chat.constants import (
    MESSAGE_CHANNEL_WEB_CHAT,
    MESSAGE_SENDER_TYPE_GUEST,
)
from apps.chat.models import Conversation, Message


class GuestMessageService:
    """Persist messages sent by a guest to a General Conversation."""

    @staticmethod
    def send_to_general_conversation(
        conversation: Conversation,
        guest_id: int,
        content: str,
    ) -> Message:
        """Persist one guest message in the supplied General Conversation."""

        return Message.objects.create(
            conversation=conversation,
            sender_type=MESSAGE_SENDER_TYPE_GUEST,
            sender_id=guest_id,
            content=content,
            channel=MESSAGE_CHANNEL_WEB_CHAT,
        )
