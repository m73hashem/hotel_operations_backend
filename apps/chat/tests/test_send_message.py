from types import SimpleNamespace
from unittest.mock import Mock, patch

from django.test import SimpleTestCase

from apps.chat.api.serializers import SendMessageSerializer
from apps.chat.dto import SentMessageDTO
from apps.chat.exceptions import InvalidGuestSession
from apps.chat.use_cases.send_message import SendMessageUseCase


class SendMessageUseCaseTests(SimpleTestCase):
    """Tests for Send Message application orchestration."""

    @patch("apps.chat.use_cases.send_message.SentMessageBuilder.build")
    @patch(
        "apps.chat.use_cases.send_message."
        "GuestMessageService.send_to_general_conversation",
    )
    @patch(
        "apps.chat.use_cases.send_message."
        "GeneralConversationService.get_or_create_active_general_conversation",
    )
    @patch(
        "apps.chat.use_cases.send_message."
        "GuestChatAccessService.validate_access",
    )
    def test_execute_coordinates_services_and_builder_in_order(
        self,
        validate_access,
        get_or_create_conversation,
        send_message,
        build_dto,
    ):
        """The Use Case performs the Send Message workflow in order."""

        guest = SimpleNamespace(id=10)
        stay = SimpleNamespace(guest=guest)
        guest_session = SimpleNamespace(stay=stay)
        conversation = SimpleNamespace()
        persisted_message = SimpleNamespace()
        dto = Mock(spec=SentMessageDTO)
        calls = []

        validate_access.side_effect = lambda token: calls.append("access") or guest_session
        get_or_create_conversation.side_effect = lambda value: (
            calls.append("conversation") or conversation
        )
        send_message.side_effect = lambda **kwargs: (
            calls.append("message") or persisted_message
        )
        build_dto.side_effect = lambda value: calls.append("builder") or dto

        result = SendMessageUseCase.execute("session-token", "Exact content")

        self.assertIs(result, dto)
        self.assertEqual(calls, ["access", "conversation", "message", "builder"])
        validate_access.assert_called_once_with("session-token")
        get_or_create_conversation.assert_called_once_with(stay)
        send_message.assert_called_once_with(
            conversation=conversation,
            guest_id=guest.id,
            content="Exact content",
        )
        build_dto.assert_called_once_with(persisted_message)

    @patch(
        "apps.chat.use_cases.send_message."
        "GuestChatAccessService.validate_access",
    )
    def test_execute_propagates_domain_exceptions_unchanged(self, validate_access):
        """The Use Case leaves domain-exception translation to the global handler."""

        error = InvalidGuestSession()
        validate_access.side_effect = error

        with self.assertRaises(InvalidGuestSession) as raised:
            SendMessageUseCase.execute("session-token", "Exact content")

        self.assertIs(raised.exception, error)

    def test_serializer_preserves_message_whitespace(self):
        """Message content is not trimmed during request-shape validation."""

        serializer = SendMessageSerializer(
            data={"session_token": "  session-token  ", "message": "  Keep spaces  "},
        )

        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["session_token"], "session-token")
        self.assertEqual(serializer.validated_data["message"], "  Keep spaces  ")
