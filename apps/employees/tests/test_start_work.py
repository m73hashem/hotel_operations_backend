from datetime import datetime
from types import SimpleNamespace
from unittest.mock import Mock, patch

from django.test import SimpleTestCase

from apps.employees.api.serializers import StartWorkSerializer
from apps.employees.builders import WorkStartBuilder
from apps.employees.dto import WorkStartDTO
from apps.employees.exceptions import AssignmentNotFound
from apps.employees.use_cases.start_work import StartWorkUseCase


class StartWorkUseCaseTests(SimpleTestCase):
    """Tests for Start Work application orchestration."""

    @patch("apps.employees.use_cases.start_work.WorkStartBuilder.build")
    @patch("apps.employees.use_cases.start_work.WorkStartService.start_work")
    def test_execute_coordinates_service_and_builder_in_order(
        self,
        start_work,
        build_dto,
    ):
        """The Use Case starts work before building its DTO."""

        assignment = SimpleNamespace()
        case = SimpleNamespace()
        dto = Mock(spec=WorkStartDTO)
        calls = []
        start_work.side_effect = lambda assignment_id: (
            calls.append("service") or (assignment, case)
        )
        build_dto.side_effect = lambda value_assignment, value_case: (
            calls.append("builder") or dto
        )

        result = StartWorkUseCase.execute(assignment_id=1)

        self.assertIs(result, dto)
        self.assertEqual(calls, ["service", "builder"])
        start_work.assert_called_once_with(1)
        build_dto.assert_called_once_with(assignment, case)

    @patch("apps.employees.use_cases.start_work.WorkStartService.start_work")
    def test_execute_propagates_domain_exceptions_unchanged(self, start_work):
        """Domain exceptions pass through to the global exception handler."""

        error = AssignmentNotFound()
        start_work.side_effect = error

        with self.assertRaises(AssignmentNotFound) as raised:
            StartWorkUseCase.execute(assignment_id=1)

        self.assertIs(raised.exception, error)

    def test_serializer_validates_required_assignment_identifier(self):
        """The serializer performs request-shape validation only."""

        serializer = StartWorkSerializer(data={"assignment_id": 1})

        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data, {"assignment_id": 1})


class WorkStartBuilderTests(SimpleTestCase):
    """Tests for flat work-start DTO construction."""

    def test_build_returns_a_flat_work_start_dto(self):
        """The builder maps only the client-facing transition fields."""

        started_at = datetime(2026, 8, 1, 12, 0, 0)
        assignment = SimpleNamespace(
            id=1,
            status="IN_PROGRESS",
            updated_at=started_at,
        )
        case = SimpleNamespace(id=2, status="IN_PROGRESS")

        dto = WorkStartBuilder.build(assignment, case)

        self.assertEqual(dto.assignment_id, 1)
        self.assertEqual(dto.case_id, 2)
        self.assertEqual(dto.assignment_status, "IN_PROGRESS")
        self.assertEqual(dto.case_status, "IN_PROGRESS")
        self.assertEqual(dto.started_at, started_at)
