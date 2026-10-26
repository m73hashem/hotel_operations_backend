from types import SimpleNamespace
from unittest.mock import Mock, patch

from django.test import SimpleTestCase

from apps.chat.dto import ChatSessionContextDTO
from apps.chat.exceptions import InvalidGuestSession
from apps.chat.use_cases.start_chat_session import StartChatSessionUseCase


class StartChatSessionUseCaseTests(SimpleTestCase):
    """Tests for Start Chat Session application orchestration."""

    def create_guest_session(self):
        """Create loaded domain-object stand-ins for Use Case tests."""

        hotel = SimpleNamespace()
        room = SimpleNamespace(hotel=hotel)
        guest = SimpleNamespace()
        stay = SimpleNamespace(guest=guest, room=room)
        return SimpleNamespace(stay=stay)

    @patch("apps.chat.use_cases.start_chat_session.ChatSessionContextBuilder.build")
    @patch(
        "apps.chat.use_cases.start_chat_session."
        "GeneralConversationService.get_or_create_active_general_conversation",
    )
    @patch(
        "apps.chat.use_cases.start_chat_session."
        "GuestChatAccessService.validate_access",
    )
    def test_execute_coordinates_services_and_builder_in_order(
        self,
        validate_access,
        get_or_create_conversation,
        build_context,
    ):
        """The workflow calls collaborators in the required order."""

        session_token = "guest-session-token"
        guest_session = self.create_guest_session()
        conversation = SimpleNamespace()
        dto = Mock(spec=ChatSessionContextDTO)
        calls = []

        validate_access.side_effect = lambda token: calls.append("access") or guest_session
        get_or_create_conversation.side_effect = lambda stay: (
            calls.append("conversation") or conversation
        )
        build_context.side_effect = lambda **kwargs: calls.append("builder") or dto

        result = StartChatSessionUseCase.execute(session_token)

        self.assertIs(result, dto)
        self.assertEqual(calls, ["access", "conversation", "builder"])
        validate_access.assert_called_once_with(session_token)
        get_or_create_conversation.assert_called_once_with(guest_session.stay)
        build_context.assert_called_once_with(
            conversation=conversation,
            guest=guest_session.stay.guest,
            stay=guest_session.stay,
            room=guest_session.stay.room,
            hotel=guest_session.stay.room.hotel,
        )

    @patch(
        "apps.chat.use_cases.start_chat_session."
        "GeneralConversationService.get_or_create_active_general_conversation",
    )
    @patch(
        "apps.chat.use_cases.start_chat_session."
        "GuestChatAccessService.validate_access",
    )
    def test_execute_propagates_domain_exceptions_unchanged(
        self,
        validate_access,
        get_or_create_conversation,
    ):
        """Domain access failures pass through without application-layer handling."""

        exception = InvalidGuestSession()
        validate_access.side_effect = exception

        with self.assertRaises(InvalidGuestSession) as raised:
            StartChatSessionUseCase.execute("invalid-session-token")

        self.assertIs(raised.exception, exception)
        get_or_create_conversation.assert_not_called()
