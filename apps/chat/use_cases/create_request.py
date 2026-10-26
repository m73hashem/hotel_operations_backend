"""Application workflow for creating a guest service request."""

from apps.chat.builders import RequestCreationBuilder
from apps.chat.dto import RequestCreationDTO
from apps.chat.services import (
    GeneralConversationService,
    GuestChatAccessService,
    RequestCreationService,
)


class CreateRequestUseCase:
    """Coordinate guest access, active Conversation lookup, and Request creation."""

    @staticmethod
    def execute(session_token: str, message: str) -> RequestCreationDTO:
        """Create one Request for the authenticated guest's active Stay."""

        guest_session = GuestChatAccessService.validate_access(session_token)
        stay = guest_session.stay
        conversation = GeneralConversationService.get_active_general_conversation(stay)
        request_record = RequestCreationService.create_from_guest_message(
            stay=stay,
            conversation=conversation,
            message=message,
        )

        return RequestCreationBuilder.build(request_record)
