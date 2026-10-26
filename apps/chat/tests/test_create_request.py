from datetime import datetime
from types import SimpleNamespace
from unittest.mock import Mock, patch

from django.test import SimpleTestCase

from apps.chat.api.serializers import CreateRequestSerializer
from apps.chat.builders import RequestCreationBuilder
from apps.chat.dto import RequestCreationDTO
from apps.chat.exceptions import InvalidGuestSession
from apps.chat.use_cases.create_request import CreateRequestUseCase


class CreateRequestUseCaseTests(SimpleTestCase):
    """Tests for Create Request application orchestration."""

    @patch("apps.chat.use_cases.create_request.RequestCreationBuilder.build")
    @patch(
        "apps.chat.use_cases.create_request."
        "RequestCreationService.create_from_guest_message",
    )
    @patch(
        "apps.chat.use_cases.create_request."
        "GeneralConversationService.get_active_general_conversation",
    )
    @patch(
        "apps.chat.use_cases.create_request."
        "GuestChatAccessService.validate_access",
    )
    def test_execute_coordinates_services_and_builder_in_order(
        self,
        validate_access,
        get_conversation,
        create_request,
        build_dto,
    ):
        """The Use Case creates one Request for the authenticated Stay."""

        stay = SimpleNamespace()
        guest_session = SimpleNamespace(stay=stay)
        conversation = SimpleNamespace()
        request_record = SimpleNamespace()
        dto = Mock(spec=RequestCreationDTO)
        calls = []
        validate_access.side_effect = lambda token: calls.append("access") or guest_session
        get_conversation.side_effect = lambda value: (
            calls.append("conversation") or conversation
        )
        create_request.side_effect = lambda **kwargs: (
            calls.append("request") or request_record
        )
        build_dto.side_effect = lambda value: calls.append("builder") or dto

        result = CreateRequestUseCase.execute("session-token", "Need towels")

        self.assertIs(result, dto)
        self.assertEqual(calls, ["access", "conversation", "request", "builder"])
        validate_access.assert_called_once_with("session-token")
        get_conversation.assert_called_once_with(stay)
        create_request.assert_called_once_with(
            stay=stay,
            conversation=conversation,
            message="Need towels",
        )
        build_dto.assert_called_once_with(request_record)

    @patch(
        "apps.chat.use_cases.create_request."
        "GuestChatAccessService.validate_access",
    )
    def test_execute_propagates_domain_exceptions_unchanged(self, validate_access):
        """Domain errors propagate to the global exception handler unchanged."""

        error = InvalidGuestSession()
        validate_access.side_effect = error

        with self.assertRaises(InvalidGuestSession) as raised:
            CreateRequestUseCase.execute("invalid-session", "Need towels")

        self.assertIs(raised.exception, error)

    def test_serializer_preserves_message_whitespace(self):
        """The request serializer does not alter the original guest message."""

        serializer = CreateRequestSerializer(
            data={
                "session_token": "  session-token  ",
                "message": "  Please send two towels.  ",
            },
        )

        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["session_token"], "session-token")
        self.assertEqual(
            serializer.validated_data["message"],
            "  Please send two towels.  ",
        )


class RequestCreationBuilderTests(SimpleTestCase):
    """Tests for flat Request creation DTO construction."""

    def test_build_returns_a_flat_request_dto(self):
        """The builder maps only the client-facing Request fields."""

        created_at = datetime(2026, 8, 1, 12, 0, 0)
        request_record = SimpleNamespace(
            id=1,
            status="NEW",
            title="Please send two towels.",
            created_at=created_at,
        )

        dto = RequestCreationBuilder.build(request_record)

        self.assertEqual(dto.request_id, 1)
        self.assertEqual(dto.status, "NEW")
        self.assertEqual(dto.title, "Please send two towels.")
        self.assertEqual(dto.created_at, created_at)
