from django.db import models

from apps.rooms.models import Room
from apps.shared.models import BaseModel


class Guest(BaseModel):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=30)
    email = models.EmailField(blank=True)
    language = models.CharField(max_length=10)

    class Meta:
        db_table = "guests"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Stay(BaseModel):
    guest = models.ForeignKey(
        Guest,
        on_delete=models.PROTECT,
        related_name="stays",
    )
    room = models.ForeignKey(
        Room,
        on_delete=models.PROTECT,
        related_name="stays",
    )
    check_in = models.DateTimeField()
    expected_check_out = models.DateTimeField()
    actual_check_out = models.DateTimeField(
        null=True,
        blank=True,
    )
    status = models.CharField(max_length=30)

    class Meta:
        db_table = "stays"
        ordering = ["-check_in"]

    def __str__(self):
        return f"{self.guest} - Room {self.room.room_number}"


class GuestSession(BaseModel):
    stay = models.OneToOneField(
        Stay,
        on_delete=models.PROTECT,
        related_name="session",
    )

    token = models.CharField(
        max_length=128,
        unique=True,
    )

    status = models.CharField(
        max_length=30,
    )

    expires_at = models.DateTimeField()

    last_seen_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    class Meta:
        db_table = "guest_sessions"

    def __str__(self):
        return f"Session for Stay #{self.stay_id}"