from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from apps.chat.constants import (
    CONVERSATION_STATUS_ACTIVE,
    CONVERSATION_TYPE_GENERAL,
)
from apps.chat.models import Conversation
from apps.guests.constants import GUEST_SESSION_STATUS_ACTIVE, STAY_STATUS_ACTIVE
from apps.guests.models import Guest, GuestSession, Stay
from apps.rooms.models import Hotel, Room


class StartChatSessionAPITests(TestCase):
    """Integration tests for the Start Chat Session endpoint."""

    def create_guest_session(
        self,
        *,
        session_status=GUEST_SESSION_STATUS_ACTIVE,
        stay_status=STAY_STATUS_ACTIVE,
        expires_at=None,
    ) -> GuestSession:
        """Create a guest session with its required chat context."""

        hotel = Hotel.objects.create(
            name="Test Hotel",
            timezone="Asia/Riyadh",
            status="ACTIVE",
        )
        room = Room.objects.create(
            hotel=hotel,
            room_number="101",
            room_type="STANDARD",
            status="AVAILABLE",
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

    def post_start_session(self, payload):
        """Post a JSON payload to the registered Start Chat Session endpoint."""

        return self.client.post(
            reverse("chat:start-session"),
            data=payload,
            content_type="application/json",
        )

    def assert_error_envelope(self, response, expected_status):
        """Assert the standard error response envelope."""

        self.assertEqual(response.status_code, expected_status)
        self.assertFalse(response.data["success"])
        self.assertIn("message", response.data)
        self.assertIn("errors", response.data)

    def test_successfully_initializes_a_chat_session(self):
        """A valid request returns the standard envelope and flat chat context."""

        guest_session = self.create_guest_session()

        response = self.post_start_session(
            {"session_token": f"  {guest_session.token}  "},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["success"])
        self.assertEqual(response.data["message"], "Chat session initialized successfully.")
        self.assertNotIn("session_token", response.data["data"])
        self.assertEqual(response.data["data"]["guest_id"], guest_session.stay.guest_id)
        self.assertEqual(response.data["data"]["stay_id"], guest_session.stay_id)
        self.assertEqual(response.data["data"]["room_id"], guest_session.stay.room_id)
        self.assertEqual(
            response.data["data"]["hotel_id"],
            guest_session.stay.room.hotel_id,
        )
        self.assertEqual(
            response.data["data"]["conversation_type"],
            CONVERSATION_TYPE_GENERAL,
        )
        self.assertEqual(
            response.data["data"]["conversation_status"],
            CONVERSATION_STATUS_ACTIVE,
        )

    def test_rejects_an_invalid_payload(self):
        """A non-string session token returns serializer validation errors."""

        response = self.post_start_session({"session_token": ["token"]})

        self.assert_error_envelope(response, status.HTTP_400_BAD_REQUEST)
        self.assertIn("session_token", response.data["errors"])

    def test_rejects_a_missing_session_token(self):
        """A missing token returns serializer validation errors."""

        response = self.post_start_session({})

        self.assert_error_envelope(response, status.HTTP_400_BAD_REQUEST)
        self.assertIn("session_token", response.data["errors"])

    def test_rejects_an_unknown_session(self):
        """An unknown Guest Session token is unauthorized."""

        response = self.post_start_session({"session_token": "unknown-token"})

        self.assert_error_envelope(response, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["message"], "Invalid guest session.")

    def test_rejects_an_inactive_session(self):
        """An inactive Guest Session token is unauthorized."""

        guest_session = self.create_guest_session(session_status="INACTIVE")

        response = self.post_start_session({"session_token": guest_session.token})

        self.assert_error_envelope(response, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["message"], "Guest session is inactive.")

    def test_rejects_an_expired_session(self):
        """An expired Guest Session token is unauthorized."""

        guest_session = self.create_guest_session(
            expires_at=timezone.now() - timedelta(seconds=1),
        )

        response = self.post_start_session({"session_token": guest_session.token})

        self.assert_error_envelope(response, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["message"], "Guest session has expired.")

    def test_rejects_an_inactive_stay(self):
        """A valid session linked to an inactive Stay is forbidden."""

        guest_session = self.create_guest_session(stay_status="CHECKED_OUT")

        response = self.post_start_session({"session_token": guest_session.token})

        self.assert_error_envelope(response, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data["message"], "Stay is inactive.")

    def test_repeated_requests_return_the_same_general_conversation(self):
        """The endpoint preserves one active General Conversation per Stay."""

        guest_session = self.create_guest_session()

        first_response = self.post_start_session(
            {"session_token": guest_session.token},
        )
        second_response = self.post_start_session(
            {"session_token": guest_session.token},
        )

        self.assertEqual(first_response.status_code, status.HTTP_200_OK)
        self.assertEqual(second_response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            first_response.data["data"]["conversation_id"],
            second_response.data["data"]["conversation_id"],
        )
        self.assertEqual(
            Conversation.objects.filter(
                stay=guest_session.stay,
                type=CONVERSATION_TYPE_GENERAL,
                status=CONVERSATION_STATUS_ACTIVE,
            ).count(),
            1,
        )
