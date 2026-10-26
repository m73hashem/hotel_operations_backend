"""Application workflow for employee logout."""

from apps.users.builders import AuthenticationBuilder
from apps.users.dto import LogoutDTO
from apps.users.services import TokenManagementService


class LogoutUseCase:
    """Coordinate refresh-token blacklisting and confirmation DTO construction."""

    @staticmethod
    def execute(refresh_token: str) -> LogoutDTO:
        """Blacklist one refresh token and return a logout confirmation."""

        TokenManagementService.blacklist_refresh_token(refresh_token)

        return AuthenticationBuilder.build_logout()
