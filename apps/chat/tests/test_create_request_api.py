from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from apps.chat.constants import (
    CONVERSATION_STATUS_ACTIVE,
    CONVERSATION_TYPE_GENERAL,
    REQUEST_SOURCE_WEB_CHAT,
    REQUEST_STATUS_NEW,
)
from apps.chat.models import Conversation, Request
from apps.guests.constants import GUEST_SESSION_STATUS_ACTIVE, STAY_STATUS_ACTIVE
from apps.guests.models import Guest, GuestSession, Stay
from apps.rooms.models import Hotel, Room


class CreateRequestAPITests(TestCase):
    """Integration tests for the Create Request endpoint."""

    def create_guest_session(
        self,
        *,
        session_status=GUEST_SESSION_STATUS_ACTIVE,
        stay_status=STAY_STATUS_ACTIVE,
        expires_at=None,
        with_conversation=True,
    ) -> GuestSession:
        """Create a guest session with optional active General Conversation."""

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
            status=stay_status,
        )
        if with_conversation:
            Conversation.objects.create(
                stay=stay,
                type=CONVERSATION_TYPE_GENERAL,
                status=CONVERSATION_STATUS_ACTIVE,
            )
        return GuestSession.objects.create(
            stay=stay,
            token="guest-session-token",
            status=session_status,
            expires_at=expires_at or timezone.now() + timedelta(hours=1),
        )

    def post_create_request(self, payload):
        """Post JSON to the registered Create Request endpoint."""

        return self.client.post(
            reverse("chat:create-request"),
            data=payload,
            content_type="application/json",
        )

    def assert_error_envelope(self, response, expected_status):
        """Assert the standard error response envelope."""

        self.assertEqual(response.status_code, expected_status)
        self.assertFalse(response.data["success"])
        self.assertIn("message", response.data)
        self.assertIn("errors", response.data)

    def test_creates_one_request_for_the_authenticated_guest_stay(self):
        """A valid request persists one Request and returns its flat DTO."""

        guest_session = self.create_guest_session()
        message = "  Please send two towels.  "

        response = self.post_create_request(
            {
                "session_token": f"  {guest_session.token}  ",
                "message": message,
            },
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data["success"])
        self.assertEqual(response.data["message"], "Request created successfully.")
        self.assertEqual(set(response.data["data"]), {"request_id", "status", "title", "created_at"})
        request_record = Request.objects.get(pk=response.data["data"]["request_id"])
        self.assertEqual(request_record.stay_id, guest_session.stay_id)
        self.assertEqual(request_record.guest_id, guest_session.stay.guest_id)
        self.assertEqual(request_record.room_id, guest_session.stay.room_id)
        self.assertEqual(request_record.original_message, message)
        self.assertEqual(request_record.title, message)
        self.assertEqual(request_record.status, REQUEST_STATUS_NEW)
        self.assertEqual(request_record.source, REQUEST_SOURCE_WEB_CHAT)
        self.assertEqual(Request.objects.count(), 1)

    def test_rejects_missing_message(self):
        """The request requires the original guest message."""

        response = self.post_create_request({"session_token": "guest-session-token"})

        self.assert_error_envelope(response, status.HTTP_400_BAD_REQUEST)
        self.assertIn("message", response.data["errors"])

    def test_rejects_blank_message(self):
        """A blank message is rejected by request-shape validation."""

        response = self.post_create_request(
            {"session_token": "guest-session-token", "message": ""},
        )

        self.assert_error_envelope(response, status.HTTP_400_BAD_REQUEST)
        self.assertIn("message", response.data["errors"])

    def test_rejects_missing_session_token(self):
        """The request requires a Guest Session token."""

        response = self.post_create_request({"message": "Need towels"})

        self.assert_error_envelope(response, status.HTTP_400_BAD_REQUEST)
        self.assertIn("session_token", response.data["errors"])

    def test_rejects_an_unknown_session(self):
        """An unknown Guest Session token is unauthorized."""

        response = self.post_create_request(
            {"session_token": "unknown-token", "message": "Need towels"},
        )

        self.assert_error_envelope(response, status.HTTP_401_UNAUTHORIZED)

    def test_rejects_an_inactive_session(self):
        """An inactive Guest Session token is unauthorized."""

        guest_session = self.create_guest_session(session_status="INACTIVE")

        response = self.post_create_request(
            {"session_token": guest_session.token, "message": "Need towels"},
        )

        self.assert_error_envelope(response, status.HTTP_401_UNAUTHORIZED)

    def test_rejects_an_expired_session(self):
        """An expired Guest Session token is unauthorized."""

        guest_session = self.create_guest_session(
            expires_at=timezone.now() - timedelta(seconds=1),
        )

        response = self.post_create_request(
            {"session_token": guest_session.token, "message": "Need towels"},
        )

        self.assert_error_envelope(response, status.HTTP_401_UNAUTHORIZED)

    def test_rejects_an_inactive_stay(self):
        """An inactive Stay cannot create a Request."""

        guest_session = self.create_guest_session(stay_status="CHECKED_OUT")

        response = self.post_create_request(
            {"session_token": guest_session.token, "message": "Need towels"},
        )

        self.assert_error_envelope(response, status.HTTP_403_FORBIDDEN)

    def test_does_not_create_a_request_without_an_active_general_conversation(self):
        """The endpoint does not create or change a Conversation to create a Request."""

        guest_session = self.create_guest_session(with_conversation=False)

        response = self.post_create_request(
            {"session_token": guest_session.token, "message": "Need towels"},
        )

        self.assert_error_envelope(response, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Request.objects.count(), 0)
        self.assertEqual(Conversation.objects.count(), 0)
