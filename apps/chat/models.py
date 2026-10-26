from django.db import models
from django.db.models import Q

from apps.chat.constants import (
    CONVERSATION_STATUS_ACTIVE,
    CONVERSATION_TYPE_CASE,
    CONVERSATION_TYPE_GENERAL,
    REQUEST_SOURCE_WEB_CHAT,
    REQUEST_STATUS_CLOSED,
    REQUEST_STATUS_NEW,
    REQUEST_STATUS_PROCESSING,
    REQUEST_STATUS_REJECTED,
)
from apps.shared.models import BaseModel


class Conversation(BaseModel):
    stay = models.ForeignKey(
        "guests.Stay",
        on_delete=models.PROTECT,
        related_name="conversations",
    )
    case = models.ForeignKey(
        "requests.Case",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="conversations",
    )
    type = models.CharField(max_length=30)
    status = models.CharField(max_length=30)

    class Meta:
        db_table = "conversations"
        ordering = ["-created_at"]
        constraints = [
            models.CheckConstraint(
                condition=Q(
                    type__in=[
                        CONVERSATION_TYPE_GENERAL,
                        CONVERSATION_TYPE_CASE,
                    ],
                ),
                name="valid_conversation_type",
            ),
            models.UniqueConstraint(
                fields=["stay"],
                condition=Q(
                    type=CONVERSATION_TYPE_GENERAL,
                    status=CONVERSATION_STATUS_ACTIVE,
                ),
                name="unique_active_general_conversation_per_stay",
            ),
            models.CheckConstraint(
                condition=~Q(type=CONVERSATION_TYPE_GENERAL) | Q(case__isnull=True),
                name="general_conversation_requires_no_case",
            ),
            models.CheckConstraint(
                condition=~Q(type=CONVERSATION_TYPE_CASE) | Q(case__isnull=False),
                name="case_conversation_requires_case",
            ),
        ]

    def __str__(self):
        return f"Conversation #{self.pk}"


class Message(BaseModel):
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.PROTECT,
        related_name="messages",
    )
    sender_type = models.CharField(max_length=30)
    sender_id = models.BigIntegerField(null=True, blank=True)
    content = models.TextField()
    channel = models.CharField(max_length=30)

    class Meta:
        db_table = "messages"
        ordering = ["created_at"]

    def __str__(self):
        return f"Message #{self.pk}"


class Request(BaseModel):
    """The original service request made by a guest through Chat."""

    stay = models.ForeignKey(
        "guests.Stay",
        on_delete=models.PROTECT,
        related_name="requests",
    )
    guest = models.ForeignKey(
        "guests.Guest",
        on_delete=models.PROTECT,
        related_name="requests",
    )
    room = models.ForeignKey(
        "rooms.Room",
        on_delete=models.PROTECT,
        related_name="requests",
    )
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.PROTECT,
        related_name="requests",
    )
    original_message = models.TextField()
    title = models.CharField(max_length=255)
    status = models.CharField(
        max_length=30,
        default=REQUEST_STATUS_NEW,
    )
    source = models.CharField(
        max_length=30,
        default=REQUEST_SOURCE_WEB_CHAT,
    )

    class Meta:
        db_table = "requests"
        ordering = ["-created_at"]
        constraints = [
            models.CheckConstraint(
                condition=Q(
                    status__in=[
                        REQUEST_STATUS_NEW,
                        REQUEST_STATUS_PROCESSING,
                        REQUEST_STATUS_CLOSED,
                        REQUEST_STATUS_REJECTED,
                    ],
                ),
                name="valid_request_status",
            ),
            models.CheckConstraint(
                condition=Q(source__in=[REQUEST_SOURCE_WEB_CHAT]),
                name="valid_request_source",
            ),
        ]

    def __str__(self):
        return f"Request #{self.pk}"
