"""Map operational Cases into transport DTOs."""

from collections.abc import Iterable

from apps.requests.dto import CaseListItemDTO
from apps.requests.models import Case


class CaseListBuilder:
    """Build flat DTOs from already-loaded Case objects."""

    @staticmethod
    def build(cases: Iterable[Case]) -> tuple[CaseListItemDTO, ...]:
        """Map operational Cases into immutable list DTOs."""

        return tuple(
            CaseListItemDTO(
                case_id=case.id,
                request_id=case.request_id,
                subject=case.subject,
                description=case.description,
                status=case.status,
                priority=case.priority,
                department_id=case.service.department_id if case.service_id else None,
                department_name=case.service.department.name if case.service_id else None,
                guest_name=f"{case.stay.guest.first_name} {case.stay.guest.last_name}",
                room_number=case.stay.room.room_number,
                created_at=case.created_at,
                updated_at=case.updated_at,
            )
            for case in cases
        )
