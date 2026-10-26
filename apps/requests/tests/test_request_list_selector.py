"""Selector tests for department-isolated operational Request lists."""

from unittest.mock import MagicMock, patch

from django.test import SimpleTestCase

from apps.requests.selectors import RequestSelector


class RequestListSelectorTests(SimpleTestCase):
    """Verify Requests reuse the certified Case department visibility scope."""

    @patch("apps.requests.selectors.request_selector.Request.objects")
    @patch(
        "apps.requests.selectors.request_selector."
        "CaseDepartmentScopeSelector.visible_to_department",
    )
    def test_list_reuses_department_scope_and_query_options(
        self,
        visible_to_department,
        objects,
    ):
        """The selector scopes Requests through visible Cases before filtering."""

        visible_cases = MagicMock()
        visible_to_department.return_value = visible_cases
        visible_cases.values.return_value = visible_cases
        queryset = MagicMock()
        objects.filter.return_value = queryset
        queryset.select_related.return_value = queryset
        queryset.filter.return_value = queryset
        queryset.order_by.return_value = queryset

        RequestSelector.list_for_operations(
            4,
            search="towels",
            status="NEW",
            ordering="room_number",
        )

        visible_to_department.assert_called_once_with(4)
        visible_cases.values.assert_called_once_with("request_id")
        objects.filter.assert_called_once_with(id__in=visible_cases)
        queryset.order_by.assert_called_once_with("room__room_number")
