from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from apps.chat.constants import (
    CASE_STATUS_OPEN,
    CONVERSATION_STATUS_ACTIVE,
    CONVERSATION_TYPE_CASE,
    CONVERSATION_TYPE_GENERAL,
)
from apps.chat.models import Conversation, Request
from apps.guests.constants import STAY_STATUS_ACTIVE
from apps.guests.models import Guest, Stay
from apps.requests.models import Case
from apps.rooms.models import Hotel, Room


class CreateCaseAPITests(TestCase):
    """Integration tests for the Create Case endpoint."""

    def create_request(self) -> Request:
        """Create a Request ready for operational Case creation."""

        hotel = Hotel.objects.create(
            name="Test Hotel",
            timezone="Asia/Riyadh",
            status="ACTIVE",
        )
        room = Room.objects.create(
            hotel=hotel,
            room_number="101",
            room_type="STANDARD",
            status="OCCUPIED",
        )
        guest = Guest.objects.create(
            first_name="Test",
            last_name="Guest",
            phone="555000000",
            language="en",
        )
        stay = Stay.objects.create(
            guest=guest,
            room=room,
            check_in=timezone.now(),
            expected_check_out=timezone.now() + timedelta(days=1),
            status=STAY_STATUS_ACTIVE,
        )
        conversation = Conversation.objects.create(
            stay=stay,
            type=CONVERSATION_TYPE_GENERAL,
            status=CONVERSATION_STATUS_ACTIVE,
        )
        return Request.objects.create(
            stay=stay,
            guest=guest,
            room=room,
            conversation=conversation,
            original_message="Please send two towels.",
            title="Please send two towels.",
        )

    def post_create_case(self, payload):
        """Post JSON to the registered Create Case endpoint."""

        return self.client.post(
            reverse("requests:create-case"),
            data=payload,
            content_type="application/json",
        )

    def assert_error_envelope(self, response, expected_status):
        """Assert the standard error response envelope."""

        self.assertEqual(response.status_code, expected_status)
        self.assertFalse(response.data["success"])
        self.assertIn("message", response.data)
        self.assertIn("errors", response.data)

    def test_creates_case_and_dedicated_conversation(self):
        """A valid Request creates exactly one Case and CASE Conversation."""

        request_record = self.create_request()

        response = self.post_create_case({"request_id": request_record.id})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data["success"])
        self.assertEqual(response.data["message"], "Case created successfully.")
        self.assertEqual(
            set(response.data["data"]),
            {"case_id", "request_id", "conversation_id", "status", "subject", "created_at"},
        )
        case = Case.objects.get(pk=response.data["data"]["case_id"])
        conversation = Conversation.objects.get(
            pk=response.data["data"]["conversation_id"],
        )
        self.assertEqual(case.request_id, request_record.id)
        self.assertEqual(case.stay_id, request_record.stay_id)
        self.assertEqual(case.subject, request_record.title)
        self.assertEqual(case.status, CASE_STATUS_OPEN)
        self.assertIsNone(case.service)
        self.assertIsNone(case.priority)
        self.assertEqual(conversation.case_id, case.id)
        self.assertEqual(conversation.type, CONVERSATION_TYPE_CASE)
        self.assertEqual(conversation.status, CONVERSATION_STATUS_ACTIVE)

    def test_rejects_a_missing_request_id(self):
        """The request requires a Request identifier."""

        response = self.post_create_case({})

        self.assert_error_envelope(response, status.HTTP_400_BAD_REQUEST)
        self.assertIn("request_id", response.data["errors"])

    def test_rejects_an_unknown_request(self):
        """An unknown Request returns the domain not-found response."""

        response = self.post_create_case({"request_id": 999})

        self.assert_error_envelope(response, status.HTTP_404_NOT_FOUND)

    def test_rejects_a_duplicate_case_for_the_same_request(self):
        """A Request cannot create a second operational Case."""

        request_record = self.create_request()
        self.post_create_case({"request_id": request_record.id})

        response = self.post_create_case({"request_id": request_record.id})

        self.assert_error_envelope(response, status.HTTP_409_CONFLICT)
        self.assertEqual(Case.objects.count(), 1)
