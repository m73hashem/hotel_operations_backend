"""Selector tests for operational Room list queries."""

from unittest.mock import MagicMock, patch

from django.test import SimpleTestCase

from apps.rooms.selectors import RoomSelector


class RoomSelectorTests(SimpleTestCase):
    """Verify Room query options are applied by the selector."""

    @patch("apps.rooms.selectors.room_selector.Room.objects")
    def test_list_for_operations_applies_query_options(self, objects):
        """Search, filtering, and ordering remain database selector concerns."""

        queryset = MagicMock()
        objects.select_related.return_value = queryset
        queryset.filter.return_value = queryset
        queryset.order_by.return_value = queryset

        RoomSelector.list_for_operations(
            search="101",
            status="OCCUPIED",
            ordering="-room_number",
        )

        objects.select_related.assert_called_once_with("hotel")
        queryset.order_by.assert_called_once_with("-room_number")
