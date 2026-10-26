"""Application workflow for personal assignment retrieval."""

from apps.dashboard.builders import MyAssignmentsBuilder
from apps.dashboard.dto import MyAssignmentsDTO
from apps.dashboard.services import MyAssignmentsService


class MyAssignmentsUseCase:
    """Coordinate personal assignment retrieval and DTO construction."""

    @staticmethod
    def execute(user_id: int, **query_params) -> MyAssignmentsDTO:
        """Return immutable assignment DTOs for the authenticated Employee."""

        assignments = MyAssignmentsService.get_my_assignments(user_id, **query_params)
        return MyAssignmentsBuilder.build(assignments)
