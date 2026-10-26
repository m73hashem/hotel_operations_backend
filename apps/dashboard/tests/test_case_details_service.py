"""Unit tests for dashboard Case details service."""

from types import SimpleNamespace
from unittest.mock import patch

from django.test import SimpleTestCase

from apps.dashboard.services import CaseDetailsService
from apps.employees.exceptions import CaseNotFound


class CaseDetailsServiceTests(SimpleTestCase):
    """Verify Case details service validation and selector delegation."""

    @patch("apps.dashboard.services.case_details_service.CaseDetailsSelector")
    def test_returns_case_timeline_and_messages(self, selector):
        """The service obtains all persisted records through its selector."""

        case = SimpleNamespace(
            id=4,
            request=None,
            subject="",
            description="",
            service_id=None,
            status="OPEN",
            updated_at=None,
        )
        timeline_events = [SimpleNamespace()]
        messages = [SimpleNamespace()]
        selector.get_by_id.return_value = case
        selector.get_latest_assignment.return_value = None
        selector.list_timeline_events.return_value = timeline_events
        selector.list_conversation_messages.return_value = messages

        self.assertEqual(
            CaseDetailsService.get_case_details(4),
            (
                case,
                None,
                "",
                None,
                None,
                None,
                None,
                timeline_events,
                messages,
            ),
        )
        selector.list_timeline_events.assert_called_once_with(4)
        selector.list_conversation_messages.assert_called_once_with(4)

    @patch("apps.dashboard.services.case_details_service.CaseDetailsSelector")
    def test_raises_domain_exception_for_unknown_case(self, selector):
        """Unknown Cases are reported through the established domain exception."""

        selector.get_by_id.return_value = None

        with self.assertRaises(CaseNotFound):
            CaseDetailsService.get_case_details(404)
