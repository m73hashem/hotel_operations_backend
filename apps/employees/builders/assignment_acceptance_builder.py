"""Builder for Accept Assignment response DTOs."""

from apps.employees.dto import AssignmentAcceptanceDTO
from apps.employees.models import Assignment


class AssignmentAcceptanceBuilder:
    """Build a flat DTO from an already-accepted Assignment."""

    @staticmethod
    def build(assignment: Assignment) -> AssignmentAcceptanceDTO:
        """Transform the Assignment into its response DTO."""

        return AssignmentAcceptanceDTO(
            assignment_id=assignment.id,
            case_id=assignment.case_id,
            employee_id=assignment.employee_id,
            status=assignment.status,
            accepted_at=assignment.accepted_at,
        )
