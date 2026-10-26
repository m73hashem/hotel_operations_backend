"""Unit tests for dashboard summary orchestration and mapping."""

from types import SimpleNamespace
from unittest.mock import Mock, patch

from django.test import SimpleTestCase

from apps.dashboard.builders import DashboardSummaryBuilder
from apps.dashboard.dto import DashboardSummaryDTO
from apps.dashboard.use_cases import DashboardSummaryUseCase


class DashboardSummaryUseCaseTests(SimpleTestCase):
    """Verify dashboard summary use-case orchestration."""

    @patch("apps.dashboard.use_cases.dashboard_summary.DashboardSummaryBuilder.build")
    @patch("apps.dashboard.use_cases.dashboard_summary.DashboardSummaryService.get_summary")
    def test_execute_coordinates_service_and_builder(self, get_summary, build):
        """The use case retrieves summary facts before mapping a DTO."""

        employee = SimpleNamespace()
        statistics = {"new_cases_count": 0}
        dto = Mock(spec=DashboardSummaryDTO)
        get_summary.return_value = employee, statistics
        build.return_value = dto

        self.assertIs(DashboardSummaryUseCase.execute(user_id=3), dto)
        get_summary.assert_called_once_with(3)
        build.assert_called_once_with(employee, statistics)


class DashboardSummaryBuilderTests(SimpleTestCase):
    """Verify dashboard summary DTO construction."""

    def test_build_maps_client_facing_summary_fields(self):
        """The builder maps values without exposing ORM objects."""

        employee = SimpleNamespace(
            id=3,
            name="Housekeeping User",
            department=SimpleNamespace(name="Housekeeping"),
        )
        statistics = {
            "new_cases_count": 2,
            "assigned_cases_count": 1,
            "in_progress_cases_count": 3,
            "completed_today_count": 4,
            "my_active_assignments_count": 1,
        }

        self.assertEqual(
            DashboardSummaryBuilder.build(employee, statistics),
            DashboardSummaryDTO(3, "Housekeeping User", "Housekeeping", 2, 1, 3, 4, 1),
        )
