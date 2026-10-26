"""Application workflow for the authenticated Employee profile."""

from apps.users.builders import AuthenticationBuilder
from apps.users.dto import CurrentEmployeeDTO
from apps.users.services import EmployeeAuthenticationService


class CurrentEmployeeUseCase:
    """Coordinate current Employee retrieval and DTO construction."""

    @staticmethod
    def execute(user_id: int) -> CurrentEmployeeDTO:
        """Return the active Employee DTO for an authenticated User."""

        employee = EmployeeAuthenticationService.get_current_employee(user_id)

        return AuthenticationBuilder.build_current_employee(employee)
