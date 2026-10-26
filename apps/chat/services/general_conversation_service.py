"""Business capability for active General Conversations."""

from django.db import IntegrityError, transaction

from apps.chat.constants import (
    CONVERSATION_STATUS_ACTIVE,
    CONVERSATION_TYPE_GENERAL,
)
from apps.chat.exceptions import ActiveGeneralConversationNotFound
from apps.chat.models import Conversation, Message
from apps.chat.selectors import ConversationSelector, MessageSelector
from apps.guests.models import Stay


class GeneralConversationService:
    """Manage the active General Conversation for a Stay."""

    @staticmethod
    def get_or_create_active_general_conversation(stay: Stay) -> Conversation:
        """Return the Stay's active General Conversation, creating it safely."""

        existing_conversation = ConversationSelector.get_active_general_for_stay(
            stay.id,
        )
        if existing_conversation is not None:
            return existing_conversation

        with transaction.atomic():
            try:
                with transaction.atomic():
                    return Conversation.objects.create(
                        stay=stay,
                        type=CONVERSATION_TYPE_GENERAL,
                        status=CONVERSATION_STATUS_ACTIVE,
                    )
            except IntegrityError:
                existing_conversation = (
                    ConversationSelector.get_active_general_for_stay(stay.id)
                )
                if existing_conversation is None:
                    raise
                return existing_conversation

    @staticmethod
    def get_active_general_conversation(stay: Stay) -> Conversation:
        """Return the Stay's active General Conversation without creating one."""

        conversation = ConversationSelector.get_active_general_for_stay(stay.id)
        if conversation is None:
            raise ActiveGeneralConversationNotFound

        return conversation

    @staticmethod
    def get_active_general_conversation_history(stay: Stay) -> list[Message]:
        """Return messages from the Stay's active General Conversation without creating one."""

        conversation = ConversationSelector.get_active_general_for_stay(stay.id)
        if conversation is None:
            return []

        return MessageSelector.list_for_conversation(conversation.id)
