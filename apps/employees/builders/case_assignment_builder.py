"""Builder for Assign Case response DTOs."""

from apps.employees.dto import CaseAssignmentDTO
from apps.employees.models import Assignment


class CaseAssignmentBuilder:
    """Build a flat DTO from an already-persisted Assignment."""

    @staticmethod
    def build(assignment: Assignment) -> CaseAssignmentDTO:
        """Transform the Assignment into its response DTO."""

        return CaseAssignmentDTO(
            assignment_id=assignment.id,
            case_id=assignment.case_id,
            employee_id=assignment.employee_id,
            status=assignment.status,
            assigned_at=assignment.assigned_at,
        )
