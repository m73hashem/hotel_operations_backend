from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from apps.chat.constants import (
    CONVERSATION_STATUS_ACTIVE,
    CONVERSATION_TYPE_GENERAL,
    MESSAGE_CHANNEL_WEB_CHAT,
    MESSAGE_SENDER_TYPE_GUEST,
)
from apps.chat.models import Conversation, Message
from apps.guests.constants import GUEST_SESSION_STATUS_ACTIVE, STAY_STATUS_ACTIVE
from apps.guests.models import Guest, GuestSession, Stay
from apps.rooms.models import Hotel, Room


class SendMessageAPITests(TestCase):
    """Integration tests for the Send Message endpoint."""

    def create_guest_session(
        self,
        *,
        session_status=GUEST_SESSION_STATUS_ACTIVE,
        stay_status=STAY_STATUS_ACTIVE,
        expires_at=None,
    ) -> GuestSession:
        """Create a guest session with required chat context."""

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
        return GuestSession.objects.create(
            stay=stay,
            token="guest-session-token",
            status=session_status,
            expires_at=expires_at or timezone.now() + timedelta(hours=1),
        )

    def post_message(self, payload):
        """Post a JSON payload to the registered Send Message endpoint."""

        return self.client.post(
            reverse("chat:send-message"),
            data=payload,
            content_type="application/json",
        )

    def assert_error_envelope(self, response, expected_status):
        """Assert the standard error response envelope."""

        self.assertEqual(response.status_code, expected_status)
        self.assertFalse(response.data["success"])
        self.assertIn("message", response.data)
        self.assertIn("errors", response.data)

    def test_sends_one_message_to_the_active_general_conversation(self):
        """A valid request creates a guest message and returns its flat DTO."""

        guest_session = self.create_guest_session()

        response = self.post_message(
            {
                "session_token": f"  {guest_session.token}  ",
                "message": "  Exact content  ",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data["success"])
        self.assertEqual(response.data["message"], "Message sent successfully.")
        self.assertEqual(response.data["data"]["content"], "  Exact content  ")
        self.assertEqual(
            response.data["data"]["sender_type"],
            MESSAGE_SENDER_TYPE_GUEST,
        )
        self.assertEqual(response.data["data"]["channel"], MESSAGE_CHANNEL_WEB_CHAT)
        self.assertEqual(Message.objects.count(), 1)
        self.assertEqual(
            Conversation.objects.filter(
                stay=guest_session.stay,
                type=CONVERSATION_TYPE_GENERAL,
                status=CONVERSATION_STATUS_ACTIVE,
            ).count(),
            1,
        )

    def test_rejects_missing_message(self):
        """The request requires a message field."""

        response = self.post_message({"session_token": "guest-session-token"})

        self.assert_error_envelope(response, status.HTTP_400_BAD_REQUEST)
        self.assertIn("message", response.data["errors"])

    def test_rejects_missing_session_token(self):
        """The request requires a Guest Session token."""

        response = self.post_message({"message": "Hello"})

        self.assert_error_envelope(response, status.HTTP_400_BAD_REQUEST)
        self.assertIn("session_token", response.data["errors"])

    def test_rejects_blank_message(self):
        """An empty message is rejected by request-shape validation."""

        response = self.post_message(
            {"session_token": "guest-session-token", "message": ""},
        )

        self.assert_error_envelope(response, status.HTTP_400_BAD_REQUEST)
        self.assertIn("message", response.data["errors"])

    def test_rejects_an_unknown_session(self):
        """An unknown Guest Session token is unauthorized."""

        response = self.post_message(
            {"session_token": "unknown-token", "message": "Hello"},
        )

        self.assert_error_envelope(response, status.HTTP_401_UNAUTHORIZED)

    def test_rejects_an_inactive_session(self):
        """An inactive Guest Session token is unauthorized."""

        guest_session = self.create_guest_session(session_status="INACTIVE")

        response = self.post_message(
            {"session_token": guest_session.token, "message": "Hello"},
        )

        self.assert_error_envelope(response, status.HTTP_401_UNAUTHORIZED)

    def test_rejects_an_expired_session(self):
        """An expired Guest Session token is unauthorized."""

        guest_session = self.create_guest_session(
            expires_at=timezone.now() - timedelta(seconds=1),
        )

        response = self.post_message(
            {"session_token": guest_session.token, "message": "Hello"},
        )

        self.assert_error_envelope(response, status.HTTP_401_UNAUTHORIZED)

    def test_rejects_an_inactive_stay(self):
        """A valid session linked to an inactive Stay is forbidden."""

        guest_session = self.create_guest_session(stay_status="CHECKED_OUT")

        response = self.post_message(
            {"session_token": guest_session.token, "message": "Hello"},
        )

        self.assert_error_envelope(response, status.HTTP_403_FORBIDDEN)
