"""Application workflow for department queue retrieval."""

from apps.dashboard.builders import DepartmentQueueBuilder
from apps.dashboard.dto import DepartmentQueueDTO
from apps.dashboard.services import DepartmentQueueService


class DepartmentQueueUseCase:
    """Coordinate department queue retrieval and DTO construction."""

    @staticmethod
    def execute(user_id: int, **query_params) -> DepartmentQueueDTO:
        """Return immutable queue DTOs for the authenticated Employee department."""

        cases = DepartmentQueueService.get_department_queue(user_id, **query_params)
        return DepartmentQueueBuilder.build(cases)
