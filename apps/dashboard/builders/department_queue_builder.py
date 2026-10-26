"""Builder for department queue DTOs."""

from collections.abc import Iterable

from apps.dashboard.dto import DepartmentQueueDTO, DepartmentQueueItemDTO
from apps.requests.models import Case


class DepartmentQueueBuilder:
    """Map already-loaded Cases into immutable department queue DTOs."""

    @staticmethod
    def build(cases: Iterable[Case]) -> DepartmentQueueDTO:
        """Build department queue DTOs without executing ORM operations."""

        return DepartmentQueueDTO(
            cases=tuple(
                DepartmentQueueItemDTO(
                    case_id=case.id,
                    request_title=(case.request.title if case.request_id else case.subject),
                    room_number=case.stay.room.room_number,
                    priority=case.priority,
                    current_status=case.status,
                    created_at=case.created_at,
                )
                for case in cases
            ),
        )
