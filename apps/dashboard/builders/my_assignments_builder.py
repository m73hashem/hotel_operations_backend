"""Builder for My Assignments DTOs."""

from collections.abc import Iterable

from apps.dashboard.dto import MyAssignmentDTO, MyAssignmentsDTO
from apps.employees.models import Assignment


class MyAssignmentsBuilder:
    """Map already-loaded Assignments into immutable dashboard DTOs."""

    @staticmethod
    def build(assignments: Iterable[Assignment]) -> MyAssignmentsDTO:
        """Build assignment DTOs without executing ORM operations."""

        return MyAssignmentsDTO(
            assignments=tuple(
                MyAssignmentDTO(
                    assignment_id=assignment.id,
                    case_id=assignment.case_id,
                    request_title=(
                        assignment.case.request.title
                        if assignment.case.request_id is not None
                        else assignment.case.subject
                    ),
                    room_number=assignment.case.stay.room.room_number,
                    priority=assignment.case.priority,
                    assignment_status=assignment.status,
                    case_status=assignment.case.status,
                    assigned_at=assignment.assigned_at,
                )
                for assignment in assignments
            ),
        )
