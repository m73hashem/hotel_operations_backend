"""Unit tests for department queue orchestration and mapping."""

from datetime import datetime
from types import SimpleNamespace
from unittest.mock import Mock, patch

from django.test import SimpleTestCase

from apps.dashboard.builders import DepartmentQueueBuilder
from apps.dashboard.dto import DepartmentQueueDTO
from apps.dashboard.use_cases import DepartmentQueueUseCase


class DepartmentQueueUseCaseTests(SimpleTestCase):
    """Verify department queue use-case orchestration."""

    @patch("apps.dashboard.use_cases.department_queue.DepartmentQueueBuilder.build")
    @patch("apps.dashboard.use_cases.department_queue.DepartmentQueueService.get_department_queue")
    def test_execute_coordinates_service_and_builder(self, get_department_queue, build):
        """The use case retrieves Cases before building its DTO."""

        cases = [SimpleNamespace()]
        dto = Mock(spec=DepartmentQueueDTO)
        get_department_queue.return_value = cases
        build.return_value = dto

        self.assertIs(DepartmentQueueUseCase.execute(user_id=6), dto)
        get_department_queue.assert_called_once_with(6)
        build.assert_called_once_with(cases)

    @patch("apps.dashboard.use_cases.department_queue.DepartmentQueueBuilder.build")
    @patch("apps.dashboard.use_cases.department_queue.DepartmentQueueService.get_department_queue")
    def test_execute_forwards_query_options_to_service(self, get_department_queue, build):
        """The use case passes validated query options without interpreting them."""

        cases = [SimpleNamespace()]
        get_department_queue.return_value = cases
        build.return_value = Mock(spec=DepartmentQueueDTO)

        DepartmentQueueUseCase.execute(
            user_id=6,
            search="101",
            case_status="OPEN",
            ordering="room_number",
        )

        get_department_queue.assert_called_once_with(
            6,
            search="101",
            case_status="OPEN",
            ordering="room_number",
        )


class DepartmentQueueBuilderTests(SimpleTestCase):
    """Verify department queue DTO construction."""

    def test_build_maps_already_loaded_case_relations(self):
        """The builder maps only the requested Case queue fields."""

        created_at = datetime(2026, 8, 2, 9, 0, 0)
        case = SimpleNamespace(
            id=8,
            request_id=9,
            request=SimpleNamespace(title="Need towels"),
            stay=SimpleNamespace(room=SimpleNamespace(room_number="101")),
            priority="NORMAL",
            status="OPEN",
            created_at=created_at,
        )

        result = DepartmentQueueBuilder.build([case])

        self.assertEqual(result.cases[0].case_id, 8)
        self.assertEqual(result.cases[0].request_title, "Need towels")
        self.assertEqual(result.cases[0].room_number, "101")
        self.assertEqual(result.cases[0].created_at, created_at)
