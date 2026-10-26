"""Business capability for validating guest access to Chat."""

from django.utils import timezone

from apps.chat.exceptions import (
    ExpiredGuestSession,
    InactiveGuestSession,
    InactiveStay,
    InvalidGuestSession,
)
from apps.guests.constants import (
    GUEST_SESSION_STATUS_ACTIVE,
    STAY_STATUS_ACTIVE,
)
from apps.guests.models import GuestSession
from apps.guests.selectors import GuestSessionSelector


class GuestChatAccessService:
    """Validate whether a guest session may access Chat."""

    @staticmethod
    def validate_access(session_token: str) -> GuestSession:
        """Validate chat access and return the guest session context."""

        guest_session = GuestSessionSelector.get_by_token_for_chat(session_token)

        if guest_session is None:
            raise InvalidGuestSession

        if guest_session.status != GUEST_SESSION_STATUS_ACTIVE:
            raise InactiveGuestSession

        if guest_session.expires_at <= timezone.now():
            raise ExpiredGuestSession

        if guest_session.stay.status != STAY_STATUS_ACTIVE:
            raise InactiveStay

        return guest_session
