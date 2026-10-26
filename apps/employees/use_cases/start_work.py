"""Application workflow for starting work on an Assignment."""

from apps.employees.builders import WorkStartBuilder
from apps.employees.dto import WorkStartDTO
from apps.employees.services import WorkStartService


class StartWorkUseCase:
    """Coordinate work-start transition and response DTO construction."""

    @staticmethod
    def execute(assignment_id: int) -> WorkStartDTO:
        """Start work on one Assignment and return its flat response DTO."""

        assignment, case = WorkStartService.start_work(assignment_id)

        return WorkStartBuilder.build(assignment, case)
