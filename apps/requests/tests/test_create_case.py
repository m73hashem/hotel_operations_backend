from datetime import datetime
from types import SimpleNamespace
from unittest.mock import Mock, patch

from django.test import SimpleTestCase

from apps.requests.api.serializers import CreateCaseSerializer
from apps.requests.builders import CaseCreationBuilder
from apps.requests.dto import CaseCreationDTO
from apps.requests.exceptions import RequestNotFound
from apps.requests.use_cases.create_case import CreateCaseUseCase


class CreateCaseUseCaseTests(SimpleTestCase):
    """Tests for Create Case application orchestration."""

    @patch("apps.requests.use_cases.create_case.CaseCreationBuilder.build")
    @patch(
        "apps.requests.use_cases.create_case.CaseCreationService.create_from_request",
    )
    def test_execute_coordinates_service_and_builder_in_order(
        self,
        create_case,
        build_dto,
    ):
        """The Use Case creates the Case before building its DTO."""

        case = SimpleNamespace()
        conversation = SimpleNamespace()
        dto = Mock(spec=CaseCreationDTO)
        calls = []
        create_case.side_effect = lambda request_id: (
            calls.append("service") or (case, conversation)
        )
        build_dto.side_effect = lambda value, related: (
            calls.append("builder") or dto
        )

        result = CreateCaseUseCase.execute(123)

        self.assertIs(result, dto)
        self.assertEqual(calls, ["service", "builder"])
        create_case.assert_called_once_with(123)
        build_dto.assert_called_once_with(case, conversation)

    @patch(
        "apps.requests.use_cases.create_case.CaseCreationService.create_from_request",
    )
    def test_execute_propagates_domain_exceptions_unchanged(self, create_case):
        """Domain errors pass unchanged to the global exception handler."""

        error = RequestNotFound()
        create_case.side_effect = error

        with self.assertRaises(RequestNotFound) as raised:
            CreateCaseUseCase.execute(123)

        self.assertIs(raised.exception, error)

    def test_serializer_accepts_a_positive_request_id(self):
        """The request serializer validates shape only."""

        serializer = CreateCaseSerializer(data={"request_id": 123})

        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["request_id"], 123)


class CaseCreationBuilderTests(SimpleTestCase):
    """Tests for flat Case creation DTO construction."""

    def test_build_returns_a_flat_case_dto(self):
        """The builder maps only client-facing Case fields."""

        created_at = datetime(2026, 8, 1, 12, 0, 0)
        case = SimpleNamespace(
            id=1,
            request_id=2,
            status="OPEN",
            subject="Please send two towels.",
            created_at=created_at,
        )
        conversation = SimpleNamespace(id=3)

        dto = CaseCreationBuilder.build(case, conversation)

        self.assertEqual(dto.case_id, 1)
        self.assertEqual(dto.request_id, 2)
        self.assertEqual(dto.conversation_id, 3)
        self.assertEqual(dto.status, "OPEN")
        self.assertEqual(dto.subject, "Please send two towels.")
        self.assertEqual(dto.created_at, created_at)
