from datetime import datetime
from types import SimpleNamespace
from unittest.mock import Mock, patch

from django.test import SimpleTestCase

from apps.employees.api.serializers import AssignCaseSerializer
from apps.employees.builders import CaseAssignmentBuilder
from apps.employees.dto import CaseAssignmentDTO
from apps.employees.exceptions import CaseNotFound
from apps.employees.use_cases.assign_case import AssignCaseUseCase


class AssignCaseUseCaseTests(SimpleTestCase):
    """Tests for Assign Case application orchestration."""

    @patch("apps.employees.use_cases.assign_case.CaseAssignmentBuilder.build")
    @patch(
        "apps.employees.use_cases.assign_case.CaseAssignmentService.assign_case",
    )
    def test_execute_coordinates_service_and_builder_in_order(
        self,
        assign_case,
        build_dto,
    ):
        """The Use Case assigns a Case before building its DTO."""

        assignment = SimpleNamespace()
        dto = Mock(spec=CaseAssignmentDTO)
        calls = []
        assign_case.side_effect = lambda case_id, employee_id: (
            calls.append("service") or assignment
        )
        build_dto.side_effect = lambda value: calls.append("builder") or dto

        result = AssignCaseUseCase.execute(case_id=1, employee_id=2)

        self.assertIs(result, dto)
        self.assertEqual(calls, ["service", "builder"])
        assign_case.assert_called_once_with(1, 2)
        build_dto.assert_called_once_with(assignment)

    @patch(
        "apps.employees.use_cases.assign_case.CaseAssignmentService.assign_case",
    )
    def test_execute_propagates_domain_exceptions_unchanged(self, assign_case):
        """Domain exceptions pass through to the global exception handler."""

        error = CaseNotFound()
        assign_case.side_effect = error

        with self.assertRaises(CaseNotFound) as raised:
            AssignCaseUseCase.execute(case_id=1, employee_id=2)

        self.assertIs(raised.exception, error)

    def test_serializer_validates_required_identifiers(self):
        """The serializer performs request-shape validation only."""

        serializer = AssignCaseSerializer(data={"case_id": 1, "employee_id": 2})

        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data, {"case_id": 1, "employee_id": 2})


class CaseAssignmentBuilderTests(SimpleTestCase):
    """Tests for flat Assignment DTO construction."""

    def test_build_returns_a_flat_assignment_dto(self):
        """The builder maps only client-facing Assignment fields."""

        assigned_at = datetime(2026, 8, 1, 12, 0, 0)
        assignment = SimpleNamespace(
            id=1,
            case_id=2,
            employee_id=3,
            status="ASSIGNED",
            assigned_at=assigned_at,
        )

        dto = CaseAssignmentBuilder.build(assignment)

        self.assertEqual(dto.assignment_id, 1)
        self.assertEqual(dto.case_id, 2)
        self.assertEqual(dto.employee_id, 3)
        self.assertEqual(dto.status, "ASSIGNED")
        self.assertEqual(dto.assigned_at, assigned_at)
