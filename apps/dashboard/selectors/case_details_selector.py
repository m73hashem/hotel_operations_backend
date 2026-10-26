"""Read-only selectors for dashboard Case details."""

from apps.chat.models import Message
from apps.employees.models import Assignment
from apps.requests.models import Case, CaseTimeline


class CaseDetailsSelector:
    """Load all persisted facts required by the Case details dashboard screen."""

    @staticmethod
    def get_by_id(case_id: int) -> Case | None:
        """Return one Case with the details relations required by its builder."""

        return (
            Case.objects.select_related(
                "request",
                "service__department",
                "stay__guest",
                "stay__room",
            )
            .filter(id=case_id)
            .first()
        )

    @staticmethod
    def get_latest_assignment(case_id: int) -> Assignment | None:
        """Return the most recently assigned Employee context for one Case."""

        return (
            Assignment.objects.select_related("employee__department")
            .filter(case_id=case_id)
            .order_by("-assigned_at")
            .first()
        )

    @staticmethod
    def list_timeline_events(case_id: int) -> list[CaseTimeline]:
        """Return persisted Case timeline events in chronological order."""

        return list(
            CaseTimeline.objects.filter(case_id=case_id)
            .only("event_type", "created_at")
            .order_by("created_at")
        )

    @staticmethod
    def list_conversation_messages(case_id: int) -> list[Message]:
        """Return Case-conversation messages in chronological order."""

        return list(
            Message.objects.filter(conversation__case_id=case_id)
            .only("id", "sender_type", "content", "created_at")
            .order_by("created_at")
        )
