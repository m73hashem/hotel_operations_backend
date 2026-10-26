"""Unit tests for dashboard business services."""

from types import SimpleNamespace
from unittest.mock import patch

from django.test import SimpleTestCase

from apps.dashboard.services import (
    DashboardSummaryService,
    DepartmentQueueService,
    MyAssignmentsService,
)
from apps.employees.constants import EMPLOYEE_STATUS_ACTIVE
from apps.users.exceptions import EmployeeAccountNotFound, InactiveEmployee


class DashboardServiceTests(SimpleTestCase):
    """Verify dashboard services validate the authenticated Employee once."""

    @patch(
        "apps.dashboard.services.dashboard_summary_service."
        "DashboardEmployeeAccessService.get_active_employee",
    )
    @patch("apps.dashboard.services.dashboard_summary_service.DashboardSummarySelector")
    def test_summary_returns_employee_and_statistics(self, selector, get_active_employee):
        """Summary service delegates all reads to its selector."""

        employee = SimpleNamespace(
            id=2,
            department_id=4,
            status=EMPLOYEE_STATUS_ACTIVE,
        )
        statistics = {"new_cases_count": 1}
        get_active_employee.return_value = employee
        selector.get_statistics.return_value = statistics

        result = DashboardSummaryService.get_summary(10)

        self.assertEqual(result, (employee, statistics))
        selector.get_statistics.assert_called_once()

    @patch("apps.dashboard.services.my_assignments_service.MyAssignmentsSelector")
    @patch(
        "apps.dashboard.services.my_assignments_service."
        "DashboardEmployeeAccessService.get_active_employee",
    )
    def test_my_assignments_limits_results_to_current_employee(
        self,
        get_active_employee,
        assignments,
    ):
        """The service requests assignments only for the resolved Employee."""

        get_active_employee.return_value = SimpleNamespace(
            id=2,
            status=EMPLOYEE_STATUS_ACTIVE,
        )
        assignments.list_for_employee.return_value = []

        MyAssignmentsService.get_my_assignments(10)

        assignments.list_for_employee.assert_called_once_with(2)

    @patch(
        "apps.dashboard.services.department_queue_service."
        "DashboardEmployeeAccessService.get_active_employee",
    )
    def test_department_queue_rejects_missing_employee(self, get_active_employee):
        """Dashboard access requires an Employee profile."""

        get_active_employee.side_effect = EmployeeAccountNotFound

        with self.assertRaises(EmployeeAccountNotFound):
            DepartmentQueueService.get_department_queue(10)

    @patch(
        "apps.dashboard.services.department_queue_service."
        "DashboardEmployeeAccessService.get_active_employee",
    )
    def test_department_queue_rejects_inactive_employee(self, get_active_employee):
        """Dashboard access requires an active Employee profile."""

        get_active_employee.side_effect = InactiveEmployee

        with self.assertRaises(InactiveEmployee):
            DepartmentQueueService.get_department_queue(10)
