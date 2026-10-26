"""Unit tests for operational dashboard statistics service behavior."""

from datetime import date
from types import SimpleNamespace
from unittest.mock import patch

from django.test import SimpleTestCase

from apps.dashboard.services import DashboardStatisticsService


class DashboardStatisticsServiceTests(SimpleTestCase):
    """Verify Employee access and statistics selector coordination."""

    @patch("apps.dashboard.services.dashboard_statistics_service.timezone.localdate")
    @patch("apps.dashboard.services.dashboard_statistics_service.DashboardStatisticsSelector")
    @patch("apps.dashboard.services.dashboard_statistics_service.EmployeeAccessService")
    def test_get_statistics_uses_active_employee_department(
        self,
        employee_access,
        selector,
        localdate,
    ):
        """The service delegates department scope facts to the selector."""

        employee = SimpleNamespace(id=4, department_id=7)
        statistics = {"total_open_cases": 2}
        today = date(2026, 8, 4)
        employee_access.get_active_employee.return_value = employee
        selector.get_statistics.return_value = statistics
        localdate.return_value = today

        self.assertIs(DashboardStatisticsService.get_statistics(9), statistics)
        employee_access.get_active_employee.assert_called_once_with(9)
        selector.get_statistics.assert_called_once_with(7, 4, today)
