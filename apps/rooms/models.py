from django.db import models

from apps.shared.models import BaseModel


class Hotel(BaseModel):
    name = models.CharField(max_length=200)
    timezone = models.CharField(max_length=64)
    status = models.CharField(max_length=30)

    class Meta:
        db_table = "hotels"

    def __str__(self):
        return self.name


class Room(BaseModel):
    hotel = models.ForeignKey(
        Hotel,
        on_delete=models.PROTECT,
        related_name="rooms",
    )
    room_number = models.CharField(max_length=20)
    room_type = models.CharField(max_length=50)
    status = models.CharField(max_length=30)

    class Meta:
        db_table = "rooms"
        constraints = [
            models.UniqueConstraint(
                fields=["hotel", "room_number"],
                name="unique_room_number_per_hotel",
            ),
        ]
        ordering = ["room_number"]

    def __str__(self):
        return self.room_number
    