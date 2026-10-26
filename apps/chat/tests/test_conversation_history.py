from datetime import datetime
from types import SimpleNamespace
from unittest.mock import Mock, patch

from django.test import SimpleTestCase

from apps.chat.api.serializers import ConversationHistorySerializer
from apps.chat.builders import ConversationHistoryBuilder
from apps.chat.dto import ConversationHistoryDTO
from apps.chat.exceptions import InvalidGuestSession
from apps.chat.use_cases.conversation_history import ConversationHistoryUseCase


class ConversationHistoryUseCaseTests(SimpleTestCase):
    """Tests for Conversation History application orchestration."""

    @patch("apps.chat.use_cases.conversation_history.ConversationHistoryBuilder.build")
    @patch(
        "apps.chat.use_cases.conversation_history."
        "GeneralConversationService.get_active_general_conversation_history",
    )
    @patch(
        "apps.chat.use_cases.conversation_history."
        "GuestChatAccessService.validate_access",
    )
    def test_execute_coordinates_services_and_builder_in_order(
        self,
        validate_access,
        get_history,
        build_dto,
    ):
        """The Use Case validates access, reads history, and builds the DTO."""

        stay = SimpleNamespace()
        guest_session = SimpleNamespace(stay=stay)
        messages = [SimpleNamespace()]
        dto = Mock(spec=ConversationHistoryDTO)
        calls = []
        validate_access.side_effect = lambda token: calls.append("access") or guest_session
        get_history.side_effect = lambda value: calls.append("history") or messages
        build_dto.side_effect = lambda value: calls.append("builder") or dto

        result = ConversationHistoryUseCase.execute("session-token")

        self.assertIs(result, dto)
        self.assertEqual(calls, ["access", "history", "builder"])
        validate_access.assert_called_once_with("session-token")
        get_history.assert_called_once_with(stay)
        build_dto.assert_called_once_with(messages)

    @patch(
        "apps.chat.use_cases.conversation_history."
        "GuestChatAccessService.validate_access",
    )
    def test_execute_propagates_domain_exceptions_unchanged(self, validate_access):
        """The Use Case leaves domain exception translation to the global handler."""

        error = InvalidGuestSession()
        validate_access.side_effect = error

        with self.assertRaises(InvalidGuestSession) as raised:
            ConversationHistoryUseCase.execute("invalid-session-token")

        self.assertIs(raised.exception, error)

    def test_serializer_trims_the_session_token(self):
        """The request serializer performs request-shape validation only."""

        serializer = ConversationHistorySerializer(
            data={"session_token": "  session-token  "},
        )

        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["session_token"], "session-token")


class ConversationHistoryBuilderTests(SimpleTestCase):
    """Tests for flat Conversation History DTO construction."""

    def test_build_maps_already_loaded_messages_without_orm_access(self):
        """The builder exposes only client-facing Message fields."""

        created_at = datetime(2026, 7, 31, 12, 0, 0)
        message = SimpleNamespace(
            id=1,
            sender_type="GUEST",
            content="Hello",
            channel="WEB_CHAT",
            created_at=created_at,
        )

        dto = ConversationHistoryBuilder.build([message])

        self.assertEqual(
            dto.messages,
            [
                {
                    "id": 1,
                    "sender_type": "GUEST",
                    "content": "Hello",
                    "channel": "WEB_CHAT",
                    "created_at": created_at,
                },
            ],
        )
