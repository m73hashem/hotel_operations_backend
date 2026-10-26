"""Builder for Start Work response DTOs."""

from apps.employees.dto import WorkStartDTO
from apps.employees.models import Assignment
from apps.requests.models import Case


class WorkStartBuilder:
    """Build a flat DTO from already-transitioned Assignment and Case objects."""

    @staticmethod
    def build(assignment: Assignment, case: Case) -> WorkStartDTO:
        """Transform the updated domain objects into their response DTO."""

        return WorkStartDTO(
            assignment_id=assignment.id,
            case_id=case.id,
            assignment_status=assignment.status,
            case_status=case.status,
            started_at=assignment.updated_at,
        )
