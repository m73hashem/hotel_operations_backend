from datetime import datetime
from types import SimpleNamespace

from django.test import SimpleTestCase

from apps.chat.builders import SentMessageBuilder


class SentMessageBuilderTests(SimpleTestCase):
    """Tests for flat Sent Message DTO construction."""

    def test_build_returns_a_flat_dto(self):
        """The builder maps an already-persisted message without ORM access."""

        created_at = datetime(2026, 7, 31, 12, 0, 0)
        message = SimpleNamespace(
            id=1,
            conversation_id=2,
            sender_type="GUEST",
            content="Hello",
            channel="WEB_CHAT",
            created_at=created_at,
        )

        dto = SentMessageBuilder.build(message)

        self.assertEqual(dto.message_id, message.id)
        self.assertEqual(dto.conversation_id, message.conversation_id)
        self.assertEqual(dto.content, message.content)
        self.assertEqual(dto.created_at, created_at)
