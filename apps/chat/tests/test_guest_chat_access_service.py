from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from apps.chat.exceptions import (
    ExpiredGuestSession,
    InactiveGuestSession,
    InactiveStay,
    InvalidGuestSession,
)
from apps.chat.services import GuestChatAccessService
from apps.guests.constants import GUEST_SESSION_STATUS_ACTIVE, STAY_STATUS_ACTIVE
from apps.guests.models import Guest, GuestSession, Stay
from apps.rooms.models import Hotel, Room


class GuestChatAccessServiceTests(TestCase):
    """Tests for guest access validation before starting Chat."""

    def create_guest_session(
        self,
        *,
        session_status=GUEST_SESSION_STATUS_ACTIVE,
        stay_status=STAY_STATUS_ACTIVE,
        expires_at=None,
    ) -> GuestSession:
        """Create a guest session with configurable access state."""

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
            token="valid-session-token",
            status=session_status,
            expires_at=expires_at or timezone.now() + timedelta(hours=1),
        )

    def test_validate_access_returns_valid_loaded_guest_session(self):
        """A valid active session grants access to Chat."""

        guest_session = self.create_guest_session()

        result = GuestChatAccessService.validate_access(guest_session.token)

        self.assertEqual(result.pk, guest_session.pk)
        self.assertIn("stay", result._state.fields_cache)

    def test_validate_access_raises_for_unknown_session(self):
        """An unknown session token cannot access Chat."""

        with self.assertRaises(InvalidGuestSession):
            GuestChatAccessService.validate_access("unknown-session-token")

    def test_validate_access_raises_for_inactive_session(self):
        """An inactive session cannot access Chat."""

        guest_session = self.create_guest_session(session_status="INACTIVE")

        with self.assertRaises(InactiveGuestSession):
            GuestChatAccessService.validate_access(guest_session.token)

    def test_validate_access_raises_for_expired_session(self):
        """An expired session cannot access Chat."""

        guest_session = self.create_guest_session(
            expires_at=timezone.now() - timedelta(seconds=1),
        )

        with self.assertRaises(ExpiredGuestSession):
            GuestChatAccessService.validate_access(guest_session.token)

    def test_validate_access_raises_for_inactive_stay(self):
        """A session linked to an inactive Stay cannot access Chat."""

        guest_session = self.create_guest_session(stay_status="CHECKED_OUT")

        with self.assertRaises(InactiveStay):
            GuestChatAccessService.validate_access(guest_session.token)
