"""Business capability for creating an operational Case from a Request."""

from django.db import transaction

from apps.chat.constants import (
    CASE_STATUS_OPEN,
    CONVERSATION_STATUS_ACTIVE,
    CONVERSATION_TYPE_CASE,
)
from apps.chat.models import Conversation
from apps.requests.exceptions import CaseAlreadyExistsForRequest, RequestNotFound
from apps.requests.models import Case
from apps.requests.selectors import CaseSelector, RequestSelector


class CaseCreationService:
    """Create one Case and its dedicated Conversation from an existing Request."""

    @staticmethod
    def create_from_request(request_id: int) -> tuple[Case, Conversation]:
        """Create the Case and CASE Conversation atomically for a Request."""

        with transaction.atomic():
            request_record = RequestSelector.get_by_id_for_case(
                request_id,
                for_update=True,
            )
            if request_record is None:
                raise RequestNotFound

            if CaseSelector.exists_for_request(request_record.id):
                raise CaseAlreadyExistsForRequest

            case = Case.objects.create(
                request=request_record,
                stay=request_record.stay,
                subject=request_record.title,
                status=CASE_STATUS_OPEN,
            )
            conversation = Conversation.objects.create(
                stay=request_record.stay,
                case=case,
                type=CONVERSATION_TYPE_CASE,
                status=CONVERSATION_STATUS_ACTIVE,
            )

        return case, conversation
