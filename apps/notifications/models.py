from django.db import models

from apps.employees.models import Employee
from apps.shared.models import BaseModel


class Notification(BaseModel):
    employee = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        related_name="notifications",
    )
    notification_type = models.CharField(max_length=50)
    title = models.CharField(max_length=200)
    message = models.TextField()
    read_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    class Meta:
        db_table = "notifications"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
    
