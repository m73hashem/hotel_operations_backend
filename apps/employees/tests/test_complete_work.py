from datetime import datetime
from types import SimpleNamespace
from unittest.mock import Mock, patch

from django.test import SimpleTestCase

from apps.employees.api.serializers import CompleteWorkSerializer
from apps.employees.builders import WorkCompletionBuilder
from apps.employees.dto import WorkCompletionDTO
from apps.employees.exceptions import AssignmentNotFound
from apps.employees.use_cases.complete_work import CompleteWorkUseCase


class CompleteWorkUseCaseTests(SimpleTestCase):
    """Tests for Complete Work application orchestration."""

    @patch("apps.employees.use_cases.complete_work.WorkCompletionBuilder.build")
    @patch("apps.employees.use_cases.complete_work.WorkCompletionService.complete_work")
    def test_execute_coordinates_service_and_builder_in_order(
        self,
        complete_work,
        build_dto,
    ):
        """The Use Case completes work before building its DTO."""

        assignment = SimpleNamespace()
        case = SimpleNamespace()
        dto = Mock(spec=WorkCompletionDTO)
        calls = []
        complete_work.side_effect = lambda assignment_id: (
            calls.append("service") or (assignment, case)
        )
        build_dto.side_effect = lambda value_assignment, value_case: (
            calls.append("builder") or dto
        )

        result = CompleteWorkUseCase.execute(assignment_id=1)

        self.assertIs(result, dto)
        self.assertEqual(calls, ["service", "builder"])
        complete_work.assert_called_once_with(1)
        build_dto.assert_called_once_with(assignment, case)

    @patch("apps.employees.use_cases.complete_work.WorkCompletionService.complete_work")
    def test_execute_propagates_domain_exceptions_unchanged(self, complete_work):
        """Domain exceptions pass through to the global exception handler."""

        error = AssignmentNotFound()
        complete_work.side_effect = error

        with self.assertRaises(AssignmentNotFound) as raised:
            CompleteWorkUseCase.execute(assignment_id=1)

        self.assertIs(raised.exception, error)

    def test_serializer_validates_required_assignment_identifier(self):
        """The serializer performs request-shape validation only."""

        serializer = CompleteWorkSerializer(data={"assignment_id": 1})

        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data, {"assignment_id": 1})


class WorkCompletionBuilderTests(SimpleTestCase):
    """Tests for flat work-completion DTO construction."""

    def test_build_returns_a_flat_work_completion_dto(self):
        """The builder maps only client-facing transition fields."""

        completed_at = datetime(2026, 8, 1, 12, 0, 0)
        assignment = SimpleNamespace(
            id=1,
            status="COMPLETED",
            updated_at=completed_at,
        )
        case = SimpleNamespace(id=2, status="COMPLETED")

        dto = WorkCompletionBuilder.build(assignment, case)

        self.assertEqual(dto.assignment_id, 1)
        self.assertEqual(dto.case_id, 2)
        self.assertEqual(dto.assignment_status, "COMPLETED")
        self.assertEqual(dto.case_status, "COMPLETED")
        self.assertEqual(dto.completed_at, completed_at)
