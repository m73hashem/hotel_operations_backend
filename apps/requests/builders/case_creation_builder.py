"""Builder for Create Case response DTOs."""

from apps.chat.models import Conversation
from apps.requests.dto import CaseCreationDTO
from apps.requests.models import Case


class CaseCreationBuilder:
    """Build a flat DTO from an already-persisted Case and Conversation."""

    @staticmethod
    def build(case: Case, conversation: Conversation) -> CaseCreationDTO:
        """Transform the domain objects into a Case creation response DTO."""

        return CaseCreationDTO(
            case_id=case.id,
            request_id=case.request_id,
            conversation_id=conversation.id,
            status=case.status,
            subject=case.subject,
            created_at=case.created_at,
        )
