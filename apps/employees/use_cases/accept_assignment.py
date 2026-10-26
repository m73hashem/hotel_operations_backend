"""Application workflow for accepting an Assignment."""

from apps.employees.builders import AssignmentAcceptanceBuilder
from apps.employees.dto import AssignmentAcceptanceDTO
from apps.employees.services import AssignmentAcceptanceService


class AcceptAssignmentUseCase:
    """Coordinate Assignment acceptance and response DTO construction."""

    @staticmethod
    def execute(assignment_id: int) -> AssignmentAcceptanceDTO:
        """Accept one Assignment and return its flat response DTO."""

        assignment = AssignmentAcceptanceService.accept_assignment(assignment_id)

        return AssignmentAcceptanceBuilder.build(assignment)
