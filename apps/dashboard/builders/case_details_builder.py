"""Builder for dashboard Case details DTOs."""

from collections.abc import Iterable

from apps.chat.models import Message
from apps.dashboard.dto import (
    CaseDetailsDTO,
    ConversationMessageDTO,
    RequestInformationDTO,
    TimelineEventDTO,
)
from apps.requests.models import Case, CaseTimeline


class CaseDetailsBuilder:
    """Map already-loaded Case detail records into immutable DTOs."""

    @staticmethod
    def build(
        case: Case,
        request_title: str,
        request_description: str,
        request_created_at,
        department: str | None,
        assigned_employee: str | None,
        closed_at,
        timeline_events: Iterable[CaseTimeline],
        messages: Iterable[Message],
    ) -> CaseDetailsDTO:
        """Build Case details DTOs without executing ORM operations."""

        return CaseDetailsDTO(
            case_id=case.id,
            request_id=case.request_id,
            request_title=request_title,
            request_description=request_description,
            case_status=case.status,
            priority=case.priority,
            created_at=case.created_at,
            closed_at=closed_at,
            department=department,
            assigned_employee=assigned_employee,
            guest_name=f"{case.stay.guest.first_name} {case.stay.guest.last_name}",
            room_number=case.stay.room.room_number,
            timeline=tuple(
                TimelineEventDTO(
                    event_type=event.event_type,
                    timestamp=event.created_at,
                )
                for event in timeline_events
            ),
            conversation=tuple(
                ConversationMessageDTO(
                    message_id=message.id,
                    sender=message.sender_type,
                    message=message.content,
                    created_at=message.created_at,
                )
                for message in messages
            ),
            request_information=RequestInformationDTO(
                request_id=case.request_id,
                category=None,
                title=request_title,
                description=request_description,
                created_at=request_created_at,
            ),
        )
