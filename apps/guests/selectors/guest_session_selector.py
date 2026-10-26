"""Read-only selectors for Guest Sessions."""

from apps.guests.models import GuestSession


class GuestSessionSelector:
    """Read guest session context required by Chat."""

    @staticmethod
    def get_by_token_for_chat(session_token: str) -> GuestSession | None:
        """Return the guest session and related chat context for a token."""

        return (
            GuestSession.objects.select_related(
                "stay__guest",
                "stay__room__hotel",
            )
            .filter(token=session_token)
            .first()
        )
