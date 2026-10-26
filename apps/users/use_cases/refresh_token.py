"""Application workflow for refreshing a JWT access token."""

from apps.users.builders import AuthenticationBuilder
from apps.users.dto import TokenRefreshDTO
from apps.users.services import TokenManagementService


class RefreshTokenUseCase:
    """Coordinate Simple JWT token refresh and DTO construction."""

    @staticmethod
    def execute(refresh_token: str) -> TokenRefreshDTO:
        """Exchange one refresh token for a new access-token DTO."""

        access_token = TokenManagementService.refresh_access_token(refresh_token)

        return AuthenticationBuilder.build_refresh(access_token)
