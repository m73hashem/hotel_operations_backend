"""Application workflow for completing work on an Assignment."""

from apps.employees.builders import WorkCompletionBuilder
from apps.employees.dto import WorkCompletionDTO
from apps.employees.services import WorkCompletionService


class CompleteWorkUseCase:
    """Coordinate work-completion transition and response DTO construction."""

    @staticmethod
    def execute(assignment_id: int) -> WorkCompletionDTO:
        """Complete work on one Assignment and return its flat response DTO."""

        assignment, case = WorkCompletionService.complete_work(assignment_id)

        return WorkCompletionBuilder.build(assignment, case)
