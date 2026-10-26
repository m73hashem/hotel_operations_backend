"""Unit tests for dashboard Case details orchestration and mapping."""

from datetime import datetime
from types import SimpleNamespace
from unittest.mock import Mock, patch

from django.test import SimpleTestCase

from apps.dashboard.api.serializers import CaseDetailsSerializer
from apps.dashboard.builders import CaseDetailsBuilder
from apps.dashboard.dto import CaseDetailsDTO
from apps.dashboard.use_cases import CaseDetailsUseCase


class CaseDetailsUseCaseTests(SimpleTestCase):
    """Verify Case details use-case orchestration."""

    @patch("apps.dashboard.use_cases.case_details.CaseDetailsBuilder.build")
    @patch("apps.dashboard.use_cases.case_details.CaseDetailsService.get_case_details")
    def test_execute_coordinates_service_and_builder(self, get_case_details, build):
        """The use case loads detail records before mapping the DTO."""

        case = SimpleNamespace()
        timeline_events = [SimpleNamespace()]
        messages = [SimpleNamespace()]
        dto = Mock(spec=CaseDetailsDTO)
        get_case_details.return_value = (
            case,
            "Need towels",
            "Please send towels.",
            None,
            "Housekeeping",
            "Amina",
            None,
            timeline_events,
            messages,
        )
        build.return_value = dto

        self.assertIs(CaseDetailsUseCase.execute(4), dto)
        get_case_details.assert_called_once_with(4)
        build.assert_called_once_with(
            case,
            "Need towels",
            "Please send towels.",
            None,
            "Housekeeping",
            "Amina",
            None,
            timeline_events,
            messages,
        )

    def test_serializer_accepts_a_positive_case_identifier(self):
        """The serializer validates only Case identifier shape."""

        serializer = CaseDetailsSerializer(data={"case_id": 4})

        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["case_id"], 4)


class CaseDetailsBuilderTests(SimpleTestCase):
    """Verify Case details DTO mapping."""

    def test_build_maps_loaded_case_details_relations(self):
        """The builder maps only transport fields from loaded objects."""

        created_at = datetime(2026, 8, 2, 10, 0, 0)
        case = SimpleNamespace(
            id=4,
            request_id=5,
            request=SimpleNamespace(
                title="Need towels",
                original_message="Please send towels.",
                created_at=created_at,
            ),
            status="OPEN",
            priority="NORMAL",
            created_at=created_at,
            updated_at=created_at,
            stay=SimpleNamespace(
                guest=SimpleNamespace(first_name="John", last_name="Smith"),
                room=SimpleNamespace(room_number="101"),
            ),
        )
        timeline_event = SimpleNamespace(event_type="CASE_CREATED", created_at=created_at)
        message = SimpleNamespace(
            id=6,
            sender_type="GUEST",
            content="Please send towels.",
            created_at=created_at,
        )

        result = CaseDetailsBuilder.build(
            case,
            "Need towels",
            "Please send towels.",
            created_at,
            "Housekeeping",
            "Amina",
            None,
            [timeline_event],
            [message],
        )

        self.assertEqual(result.case_id, 4)
        self.assertEqual(result.department, "Housekeeping")
        self.assertEqual(result.assigned_employee, "Amina")
        self.assertEqual(result.timeline[0].event_type, "CASE_CREATED")
        self.assertEqual(result.conversation[0].message_id, 6)
        self.assertIsNone(result.request_information.category)
