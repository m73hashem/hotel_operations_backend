"""Application workflow for assigning an Employee to a Case."""

from apps.employees.builders import CaseAssignmentBuilder
from apps.employees.dto import CaseAssignmentDTO
from apps.employees.services import CaseAssignmentService


class AssignCaseUseCase:
    """Coordinate Case assignment and response DTO construction."""

    @staticmethod
    def execute(case_id: int, employee_id: int) -> CaseAssignmentDTO:
        """Create one Assignment and return its flat response DTO."""

        assignment = CaseAssignmentService.assign_case(case_id, employee_id)

        return CaseAssignmentBuilder.build(assignment)
