"""JWT refresh and logout operations backed by Simple JWT."""

from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.exceptions import InvalidRefreshToken


class TokenManagementService:
    """Exchange and blacklist refresh tokens without application session state."""

    @staticmethod
    def refresh_access_token(refresh_token: str) -> str:
        """Return a new access token for a valid Simple JWT refresh token."""

        try:
            token = RefreshToken(refresh_token)
        except TokenError as error:
            raise InvalidRefreshToken from error

        return str(token.access_token)

    @staticmethod
    def blacklist_refresh_token(refresh_token: str) -> None:
        """Blacklist a valid Simple JWT refresh token."""

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except TokenError as error:
            raise InvalidRefreshToken from error
