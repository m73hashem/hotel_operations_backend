"""Business capability for creating guest service requests."""

from apps.chat.constants import REQUEST_SOURCE_WEB_CHAT, REQUEST_STATUS_NEW
from apps.chat.models import Conversation, Request
from apps.guests.models import Stay


class RequestCreationService:
    """Persist the original service request made by a guest."""

    @staticmethod
    def create_from_guest_message(
        stay: Stay,
        conversation: Conversation,
        message: str,
    ) -> Request:
        """Create one Request from the original, unmodified guest message."""

        return Request.objects.create(
            stay=stay,
            guest=stay.guest,
            room=stay.room,
            conversation=conversation,
            original_message=message,
            title=message,
            status=REQUEST_STATUS_NEW,
            source=REQUEST_SOURCE_WEB_CHAT,
        )
