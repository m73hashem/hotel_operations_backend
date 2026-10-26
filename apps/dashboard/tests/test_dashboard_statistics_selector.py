"""Selector tests for operational dashboard statistics aggregates."""

from datetime import date
from unittest.mock import MagicMock, patch

from django.test import SimpleTestCase

from apps.dashboard.selectors import DashboardStatisticsSelector


class DashboardStatisticsSelectorTests(SimpleTestCase):
    """Verify aggregate queries reuse the certified department case scope."""

    @patch("apps.dashboard.selectors.dashboard_statistics_selector.Assignment.objects")
    @patch("apps.dashboard.selectors.dashboard_statistics_selector.Room.objects")
    @patch(
        "apps.dashboard.selectors.dashboard_statistics_selector."
        "CaseDepartmentScopeSelector.visible_to_department",
    )
    def test_get_statistics_reuses_department_scope(
        self,
        visible_to_department,
        room_objects,
        assignment_objects,
    ):
        """All department aggregates originate from the canonical Case scope."""

        visible_cases = MagicMock()
        visible_cases.aggregate.return_value = {
            "total_open_cases": 1,
            "total_in_progress_cases": 2,
            "total_closed_today": 3,
            "pending_requests": 4,
            "active_stays": 5,
        }
        visible_to_department.return_value = visible_cases
        room_queryset = MagicMock()
        room_queryset.aggregate.return_value = {
            "occupied_rooms": 6,
            "available_rooms": 7,
            "out_of_service_rooms": 8,
        }
        room_objects.filter.return_value = room_queryset
        assignment_queryset = MagicMock()
        assignment_queryset.aggregate.return_value = {
            "my_active_assignments": 9,
            "my_completed_today": 10,
        }
        assignment_objects.filter.return_value = assignment_queryset

        result = DashboardStatisticsSelector.get_statistics(2, 3, date(2026, 8, 4))

        visible_to_department.assert_called_once_with(2)
        room_objects.filter.assert_called_once_with(stays__cases__in=visible_cases)
        assignment_objects.filter.assert_called_once_with(employee_id=3)
        self.assertEqual(result["out_of_service_rooms"], 8)
