"""Builder for Close Case response DTOs."""

from apps.employees.dto import CaseClosureDTO
from apps.employees.models import Assignment
from apps.requests.models import Case


class CaseClosureBuilder:
    """Build a flat DTO from already-closed Case and released Assignment objects."""

    @staticmethod
    def build(case: Case, assignment: Assignment) -> CaseClosureDTO:
        """Transform the updated domain objects into their response DTO."""

        return CaseClosureDTO(
            case_id=case.id,
            assignment_id=assignment.id,
            case_status=case.status,
            assignment_status=assignment.status,
            closed_at=case.updated_at,
        )
