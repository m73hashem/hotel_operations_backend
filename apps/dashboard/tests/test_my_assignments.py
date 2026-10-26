"""Unit tests for My Assignments orchestration and mapping."""

from datetime import datetime
from types import SimpleNamespace
from unittest.mock import Mock, patch

from django.test import SimpleTestCase

from apps.dashboard.builders import MyAssignmentsBuilder
from apps.dashboard.dto import MyAssignmentsDTO
from apps.dashboard.use_cases import MyAssignmentsUseCase


class MyAssignmentsUseCaseTests(SimpleTestCase):
    """Verify My Assignments use-case orchestration."""

    @patch("apps.dashboard.use_cases.my_assignments.MyAssignmentsBuilder.build")
    @patch("apps.dashboard.use_cases.my_assignments.MyAssignmentsService.get_my_assignments")
    def test_execute_coordinates_service_and_builder(self, get_my_assignments, build):
        """The use case retrieves assignments before building its DTO."""

        assignments = [SimpleNamespace()]
        dto = Mock(spec=MyAssignmentsDTO)
        get_my_assignments.return_value = assignments
        build.return_value = dto

        self.assertIs(MyAssignmentsUseCase.execute(user_id=5), dto)
        get_my_assignments.assert_called_once_with(5)
        build.assert_called_once_with(assignments)

    @patch("apps.dashboard.use_cases.my_assignments.MyAssignmentsBuilder.build")
    @patch("apps.dashboard.use_cases.my_assignments.MyAssignmentsService.get_my_assignments")
    def test_execute_forwards_query_options_to_service(self, get_my_assignments, build):
        """The use case passes validated query options without interpreting them."""

        assignments = [SimpleNamespace()]
        get_my_assignments.return_value = assignments
        build.return_value = Mock(spec=MyAssignmentsDTO)

        MyAssignmentsUseCase.execute(
            user_id=5,
            search="towels",
            assignment_status="ASSIGNED",
            ordering="-assigned_at",
        )

        get_my_assignments.assert_called_once_with(
            5,
            search="towels",
            assignment_status="ASSIGNED",
            ordering="-assigned_at",
        )


class MyAssignmentsBuilderTests(SimpleTestCase):
    """Verify My Assignments DTO construction."""

    def test_build_maps_already_loaded_assignment_relations(self):
        """The builder maps only the requested Assignment fields."""

        assigned_at = datetime(2026, 8, 2, 9, 0, 0)
        assignment = SimpleNamespace(
            id=7,
            case_id=8,
            status="ASSIGNED",
            assigned_at=assigned_at,
            case=SimpleNamespace(
                request_id=9,
                request=SimpleNamespace(title="Need towels"),
                stay=SimpleNamespace(room=SimpleNamespace(room_number="101")),
                priority="NORMAL",
                status="ASSIGNED",
            ),
        )

        result = MyAssignmentsBuilder.build([assignment])

        self.assertEqual(result.assignments[0].assignment_id, 7)
        self.assertEqual(result.assignments[0].request_title, "Need towels")
        self.assertEqual(result.assignments[0].room_number, "101")
        self.assertEqual(result.assignments[0].assigned_at, assigned_at)
