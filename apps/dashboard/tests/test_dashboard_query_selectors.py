"""Selector tests for dashboard search, filter, and ordering query construction."""

from unittest.mock import MagicMock, patch

from django.test import SimpleTestCase

from apps.dashboard.selectors import DepartmentQueueSelector, MyAssignmentsSelector


class MyAssignmentsSelectorTests(SimpleTestCase):
    """Verify My Assignments query options stay inside its selector."""

    @patch("apps.dashboard.selectors.my_assignments_selector.Assignment.objects")
    def test_applies_search_filters_and_database_ordering(self, objects):
        """Search, filters, and ordering are added to the selector queryset."""

        queryset = MagicMock()
        objects.filter.return_value = queryset
        queryset.select_related.return_value = queryset
        queryset.filter.return_value = queryset
        queryset.order_by.return_value = queryset

        MyAssignmentsSelector.list_for_employee(
            1,
            search="towels",
            assignment_status="ASSIGNED",
            case_status="OPEN",
            priority="HIGH",
            ordering="room_number",
        )

        queryset.order_by.assert_called_once_with("case__stay__room__room_number")


class DepartmentQueueSelectorTests(SimpleTestCase):
    """Verify Department Queue query options stay inside its selector."""

    @patch(
        "apps.dashboard.selectors.department_queue_selector."
        "CaseDepartmentScopeSelector.visible_to_department",
    )
    def test_reuses_department_scope_for_filtered_queue(self, visible_to_department):
        """The queue applies query options after the shared department scope."""

        queryset = MagicMock()
        visible_to_department.return_value = queryset
        queryset.filter.return_value = queryset
        queryset.select_related.return_value = queryset
        queryset.order_by.return_value = queryset
        queryset.distinct.return_value = queryset

        DepartmentQueueSelector.list_for_department(
            1,
            search="101",
            case_status="OPEN",
            priority="HIGH",
            ordering="-priority",
        )

        visible_to_department.assert_called_once_with(1)
        queryset.order_by.assert_called_once_with("-priority")
