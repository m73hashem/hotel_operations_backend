from datetime import datetime
from types import SimpleNamespace
from unittest.mock import Mock, patch

from django.test import SimpleTestCase

from apps.employees.api.serializers import CloseCaseSerializer
from apps.employees.builders import CaseClosureBuilder
from apps.employees.dto import CaseClosureDTO
from apps.employees.exceptions import CaseNotFound
from apps.employees.use_cases.close_case import CloseCaseUseCase


class CloseCaseUseCaseTests(SimpleTestCase):
    """Tests for Close Case application orchestration."""

    @patch("apps.employees.use_cases.close_case.CaseClosureBuilder.build")
    @patch("apps.employees.use_cases.close_case.CaseClosureService.close_case")
    def test_execute_coordinates_service_and_builder_in_order(
        self,
        close_case,
        build_dto,
    ):
        """The Use Case closes a Case before building its DTO."""

        case = SimpleNamespace()
        assignment = SimpleNamespace()
        dto = Mock(spec=CaseClosureDTO)
        calls = []
        close_case.side_effect = lambda case_id: (
            calls.append("service") or (case, assignment)
        )
        build_dto.side_effect = lambda value_case, value_assignment: (
            calls.append("builder") or dto
        )

        result = CloseCaseUseCase.execute(case_id=1)

        self.assertIs(result, dto)
        self.assertEqual(calls, ["service", "builder"])
        close_case.assert_called_once_with(1)
        build_dto.assert_called_once_with(case, assignment)

    @patch("apps.employees.use_cases.close_case.CaseClosureService.close_case")
    def test_execute_propagates_domain_exceptions_unchanged(self, close_case):
        """Domain exceptions pass through to the global exception handler."""

        error = CaseNotFound()
        close_case.side_effect = error

        with self.assertRaises(CaseNotFound) as raised:
            CloseCaseUseCase.execute(case_id=1)

        self.assertIs(raised.exception, error)

    def test_serializer_validates_required_case_identifier(self):
        """The serializer performs request-shape validation only."""

        serializer = CloseCaseSerializer(data={"case_id": 1})

        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data, {"case_id": 1})


class CaseClosureBuilderTests(SimpleTestCase):
    """Tests for flat Case-closure DTO construction."""

    def test_build_returns_a_flat_case_closure_dto(self):
        """The builder maps only client-facing transition fields."""

        closed_at = datetime(2026, 8, 1, 12, 0, 0)
        case = SimpleNamespace(id=1, status="CLOSED", updated_at=closed_at)
        assignment = SimpleNamespace(id=2, status="RELEASED")

        dto = CaseClosureBuilder.build(case, assignment)

        self.assertEqual(dto.case_id, 1)
        self.assertEqual(dto.assignment_id, 2)
        self.assertEqual(dto.case_status, "CLOSED")
        self.assertEqual(dto.assignment_status, "RELEASED")
        self.assertEqual(dto.closed_at, closed_at)
