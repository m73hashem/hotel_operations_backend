"""Builder for Complete Work response DTOs."""

from apps.employees.dto import WorkCompletionDTO
from apps.employees.models import Assignment
from apps.requests.models import Case


class WorkCompletionBuilder:
    """Build a flat DTO from already-completed Assignment and Case objects."""

    @staticmethod
    def build(assignment: Assignment, case: Case) -> WorkCompletionDTO:
        """Transform the updated domain objects into their response DTO."""

        return WorkCompletionDTO(
            assignment_id=assignment.id,
            case_id=case.id,
            assignment_status=assignment.status,
            case_status=case.status,
            completed_at=assignment.updated_at,
        )
