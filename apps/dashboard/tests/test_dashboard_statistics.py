"""Unit tests for operational dashboard statistics orchestration and mapping."""

from unittest.mock import Mock, patch

from django.test import SimpleTestCase

from apps.dashboard.builders import DashboardStatisticsBuilder
from apps.dashboard.dto import DashboardStatisticsDTO
from apps.dashboard.use_cases import DashboardStatisticsUseCase


class DashboardStatisticsUseCaseTests(SimpleTestCase):
    """Verify statistics use-case orchestration."""

    @patch("apps.dashboard.use_cases.dashboard_statistics.DashboardStatisticsBuilder.build")
    @patch("apps.dashboard.use_cases.dashboard_statistics.DashboardStatisticsService.get_statistics")
    def test_execute_coordinates_service_and_builder(self, get_statistics, build):
        """The use case retrieves statistics before building its DTO."""

        statistics = {"total_open_cases": 2}
        dto = Mock(spec=DashboardStatisticsDTO)
        get_statistics.return_value = statistics
        build.return_value = dto

        self.assertIs(DashboardStatisticsUseCase.execute(user_id=5), dto)
        get_statistics.assert_called_once_with(5)
        build.assert_called_once_with(statistics)


class DashboardStatisticsBuilderTests(SimpleTestCase):
    """Verify statistics DTO construction."""

    def test_build_maps_all_statistics(self):
        """The builder maps aggregate values without domain decisions."""

        statistics = {
            "total_open_cases": 1,
            "total_in_progress_cases": 2,
            "total_closed_today": 3,
            "my_active_assignments": 4,
            "my_completed_today": 5,
            "pending_requests": 6,
            "active_stays": 7,
            "occupied_rooms": 8,
            "available_rooms": 9,
            "out_of_service_rooms": 10,
        }

        result = DashboardStatisticsBuilder.build(statistics)

        self.assertEqual(result, DashboardStatisticsDTO(**statistics))
