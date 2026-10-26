"""Read-only selectors for Chat Messages."""

from apps.chat.models import Message


class MessageSelector:
    """Read messages required for Conversation History."""

    @staticmethod
    def list_for_conversation(conversation_id: int) -> list[Message]:
        """Return a Conversation's messages in ascending creation order."""

        return list(
            Message.objects.filter(conversation_id=conversation_id)
            .only(
                "id",
                "sender_type",
                "content",
                "channel",
                "created_at",
            )
            .order_by("created_at", "id"),
        )
