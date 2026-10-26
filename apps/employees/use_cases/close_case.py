"""Application workflow for closing a completed Case."""

from apps.employees.builders import CaseClosureBuilder
from apps.employees.dto import CaseClosureDTO
from apps.employees.services import CaseClosureService


class CloseCaseUseCase:
    """Coordinate Case closure and response DTO construction."""

    @staticmethod
    def execute(case_id: int) -> CaseClosureDTO:
        """Close one Case and return its flat response DTO."""

        case, assignment = CaseClosureService.close_case(case_id)

        return CaseClosureBuilder.build(case, assignment)
