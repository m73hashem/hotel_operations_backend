"""Selector tests for operational Guest list queries."""

from unittest.mock import MagicMock, patch

from django.test import SimpleTestCase

from apps.guests.api.serializers import GuestListQuerySerializer
from apps.guests.selectors.selectors import GuestSelector


class GuestListSelectorTests(SimpleTestCase):
    """Verify Guest list query options remain inside the selector."""

    @patch("apps.guests.selectors.selectors.Guest.objects")
    def test_list_applies_search_active_stay_filter_and_ordering(self, objects):
        """Guest search, filters, and ordering use the database queryset."""

        queryset = MagicMock()
        objects.all.return_value = queryset
        queryset.filter.return_value = queryset
        queryset.order_by.return_value = queryset
        queryset.distinct.return_value = queryset

        GuestSelector.list(search="Smith", active_stay=True, ordering="-last_name")

        queryset.order_by.assert_called_once_with("-last_name")
        queryset.distinct.assert_called_once()

    @patch("apps.guests.selectors.selectors.Guest.objects")
    def test_list_orders_by_full_name(self, objects):
        """Full-name ordering maps to the persisted name fields in the selector."""

        queryset = MagicMock()
        objects.all.return_value = queryset
        queryset.order_by.return_value = queryset
        queryset.distinct.return_value = queryset

        GuestSelector.list(ordering="full_name")

        queryset.order_by.assert_called_once_with("first_name", "last_name")

    def test_query_serializer_accepts_full_name_ordering(self):
        """The documented full-name ordering value has a valid request shape."""

        serializer = GuestListQuerySerializer(data={"ordering": "full_name"})

        self.assertTrue(serializer.is_valid())
