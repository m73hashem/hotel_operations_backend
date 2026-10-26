from django.db import models
from django.db.models import Q

from apps.chat.constants import (
    CASE_STATUS_ACCEPTED,
    CASE_STATUS_ASSIGNED,
    CASE_STATUS_CLOSED,
    CASE_STATUS_COMPLETED,
    CASE_STATUS_IN_PROGRESS,
    CASE_STATUS_OPEN,
    CASE_STATUS_VERIFIED,
)
from apps.employees.models import Department
from apps.guests.models import Stay
from apps.shared.models import BaseModel


class Service(BaseModel):
    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        related_name="services",
    )
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=True)

    class Meta:
        db_table = "services"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Case(BaseModel):
    request = models.ForeignKey(
        "chat.Request",
        on_delete=models.PROTECT,
        related_name="cases",
        null=True,
        blank=True,
    )
    stay = models.ForeignKey(
        Stay,
        on_delete=models.PROTECT,
        related_name="cases",
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.PROTECT,
        related_name="cases",
        null=True,
        blank=True,
    )
    priority = models.CharField(
        max_length=30,
        null=True,
        blank=True,
    )
    status = models.CharField(
        max_length=30,
        default=CASE_STATUS_OPEN,
    )
    subject = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    completed_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    class Meta:
        db_table = "cases"
        ordering = ["-created_at"]
        constraints = [
            models.CheckConstraint(
                condition=Q(
                    status__in=[
                        CASE_STATUS_OPEN,
                        CASE_STATUS_ASSIGNED,
                        CASE_STATUS_ACCEPTED,
                        CASE_STATUS_IN_PROGRESS,
                        CASE_STATUS_COMPLETED,
                        CASE_STATUS_VERIFIED,
                        CASE_STATUS_CLOSED,
                    ],
                ),
                name="valid_case_status",
            ),
        ]

    def __str__(self):
        return self.subject


class WorkOrder(BaseModel):
    case = models.ForeignKey(
        Case,
        on_delete=models.PROTECT,
        related_name="work_orders",
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        related_name="work_orders",
    )
    status = models.CharField(max_length=30)
    priority = models.CharField(max_length=30)
    completed_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    class Meta:
        db_table = "work_orders"
        ordering = ["-created_at"]

    def __str__(self):
        return f"WO-{self.pk}"


class CaseTimeline(BaseModel):
    case = models.ForeignKey(
        Case,
        on_delete=models.PROTECT,
        related_name="timeline",
    )
    event_type = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    class Meta:
        db_table = "case_timelines"
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.case} - {self.event_type}"


class Feedback(BaseModel):
    case = models.OneToOneField(
        Case,
        on_delete=models.PROTECT,
        related_name="feedback",
    )
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField(blank=True)

    class Meta:
        db_table = "feedback"

    def __str__(self):
        return f"Feedback for {self.case}"
    
