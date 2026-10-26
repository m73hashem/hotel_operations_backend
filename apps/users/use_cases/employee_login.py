"""Application workflow for employee login."""

from apps.users.builders import AuthenticationBuilder
from apps.users.dto import EmployeeLoginDTO
from apps.users.services import EmployeeAuthenticationService


class EmployeeLoginUseCase:
    """Coordinate employee authentication and login DTO construction."""

    @staticmethod
    def execute(username: str, password: str) -> EmployeeLoginDTO:
        """Authenticate one Employee and return their JWT response DTO."""

        employee, access_token, refresh_token = (
            EmployeeAuthenticationService.authenticate_employee(username, password)
        )

        return AuthenticationBuilder.build_login(
            employee,
            access_token=access_token,
            refresh_token=refresh_token,
        )
