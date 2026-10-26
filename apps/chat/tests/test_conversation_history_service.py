from types import SimpleNamespace
from unittest.mock import patch

from django.test import SimpleTestCase

from apps.chat.selectors import ConversationSelector, MessageSelector
from apps.chat.services import GeneralConversationService


class GeneralConversationHistoryServiceTests(SimpleTestCase):
    """Tests for active General Conversation history retrieval."""

    @patch.object(MessageSelector, "list_for_conversation")
    @patch.object(ConversationSelector, "get_active_general_for_stay")
    def test_returns_messages_for_the_active_general_conversation(
        self,
        get_active_conversation,
        list_messages,
    ):
        """The service selects the active General Conversation before loading messages."""

        stay = SimpleNamespace(id=1)
        conversation = SimpleNamespace(id=2)
        messages = [SimpleNamespace(), SimpleNamespace()]
        get_active_conversation.return_value = conversation
        list_messages.return_value = messages

        result = GeneralConversationService.get_active_general_conversation_history(
            stay,
        )

        self.assertIs(result, messages)
        get_active_conversation.assert_called_once_with(stay.id)
        list_messages.assert_called_once_with(conversation.id)

    @patch.object(MessageSelector, "list_for_conversation")
    @patch.object(ConversationSelector, "get_active_general_for_stay")
    def test_does_not_create_a_conversation_when_none_is_active(
        self,
        get_active_conversation,
        list_messages,
    ):
        """A missing active General Conversation produces an empty read-only history."""

        get_active_conversation.return_value = None

        result = GeneralConversationService.get_active_general_conversation_history(
            SimpleNamespace(id=1),
        )

        self.assertEqual(result, [])
        list_messages.assert_not_called()
