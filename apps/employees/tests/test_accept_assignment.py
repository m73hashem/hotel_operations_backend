from datetime import datetime
from types import SimpleNamespace
from unittest.mock import Mock, patch

from django.test import SimpleTestCase

from apps.employees.api.serializers import AcceptAssignmentSerializer
from apps.employees.builders import AssignmentAcceptanceBuilder
from apps.employees.dto import AssignmentAcceptanceDTO
from apps.employees.exceptions import AssignmentNotFound
from apps.employees.use_cases.accept_assignment import AcceptAssignmentUseCase


class AcceptAssignmentUseCaseTests(SimpleTestCase):
    """Tests for Accept Assignment application orchestration."""

    @patch("apps.employees.use_cases.accept_assignment.AssignmentAcceptanceBuilder.build")
    @patch(
        "apps.employees.use_cases.accept_assignment."
        "AssignmentAcceptanceService.accept_assignment",
    )
    def test_execute_coordinates_service_and_builder_in_order(
        self,
        accept_assignment,
        build_dto,
    ):
        """The Use Case accepts an Assignment before building its DTO."""

        assignment = SimpleNamespace()
        dto = Mock(spec=AssignmentAcceptanceDTO)
        calls = []
        accept_assignment.side_effect = lambda assignment_id: (
            calls.append("service") or assignment
        )
        build_dto.side_effect = lambda value: calls.append("builder") or dto

        result = AcceptAssignmentUseCase.execute(assignment_id=1)

        self.assertIs(result, dto)
        self.assertEqual(calls, ["service", "builder"])
        accept_assignment.assert_called_once_with(1)
        build_dto.assert_called_once_with(assignment)

    @patch(
        "apps.employees.use_cases.accept_assignment."
        "AssignmentAcceptanceService.accept_assignment",
    )
    def test_execute_propagates_domain_exceptions_unchanged(self, accept_assignment):
        """Domain exceptions pass through to the global exception handler."""

        error = AssignmentNotFound()
        accept_assignment.side_effect = error

        with self.assertRaises(AssignmentNotFound) as raised:
            AcceptAssignmentUseCase.execute(assignment_id=1)

        self.assertIs(raised.exception, error)

    def test_serializer_validates_required_assignment_identifier(self):
        """The serializer performs request-shape validation only."""

        serializer = AcceptAssignmentSerializer(data={"assignment_id": 1})

        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data, {"assignment_id": 1})


class AssignmentAcceptanceBuilderTests(SimpleTestCase):
    """Tests for flat accepted-Assignment DTO construction."""

    def test_build_returns_a_flat_assignment_dto(self):
        """The builder maps only client-facing Assignment fields."""

        accepted_at = datetime(2026, 8, 1, 12, 0, 0)
        assignment = SimpleNamespace(
            id=1,
            case_id=2,
            employee_id=3,
            status="ACCEPTED",
            accepted_at=accepted_at,
        )

        dto = AssignmentAcceptanceBuilder.build(assignment)

        self.assertEqual(dto.assignment_id, 1)
        self.assertEqual(dto.case_id, 2)
        self.assertEqual(dto.employee_id, 3)
        self.assertEqual(dto.status, "ACCEPTED")
        self.assertEqual(dto.accepted_at, accepted_at)
