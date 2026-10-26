"""Read-only selectors for Chat Conversations."""

from apps.chat.constants import (
    CONVERSATION_STATUS_ACTIVE,
    CONVERSATION_TYPE_GENERAL,
)
from apps.chat.models import Conversation


class ConversationSelector:
    """Read active General Conversations for a Stay."""

    @staticmethod
    def get_active_general_for_stay(stay_id: int) -> Conversation | None:
        """Return the active General Conversation for the supplied Stay."""

        return (
            Conversation.objects.select_related("stay")
            .filter(
                stay_id=stay_id,
                type=CONVERSATION_TYPE_GENERAL,
                status=CONVERSATION_STATUS_ACTIVE,
            )
            .first()
        )
