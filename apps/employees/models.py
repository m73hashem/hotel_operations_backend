from django.db import models
from django.db.models import Q

from apps.employees.constants import (
    ACTIVE_ASSIGNMENT_STATUSES,
    ASSIGNMENT_STATUS_ACCEPTED,
    ASSIGNMENT_STATUS_ASSIGNED,
    ASSIGNMENT_STATUS_COMPLETED,
    ASSIGNMENT_STATUS_IN_PROGRESS,
    ASSIGNMENT_STATUS_RELEASED,
)
from apps.shared.models import BaseModel


class Department(BaseModel):
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=30)

    class Meta:
        db_table = "departments"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Employee(BaseModel):
    user = models.OneToOneField(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="employee",
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        related_name="employees",
    )
    employee_number = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=30)
    email = models.EmailField(blank=True)
    status = models.CharField(max_length=30)

    class Meta:
        db_table = "employees"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Shift(BaseModel):
    name = models.CharField(max_length=100)
    start_time = models.TimeField()
    end_time = models.TimeField()
    status = models.CharField(max_length=30)

    class Meta:
        db_table = "shifts"
        ordering = ["start_time"]

    def __str__(self):
        return self.name


class EmployeeShift(BaseModel):
    employee = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        related_name="employee_shifts",
    )
    shift = models.ForeignKey(
        Shift,
        on_delete=models.PROTECT,
        related_name="employee_shifts",
    )

    class Meta:
        db_table = "employee_shifts"
        constraints = [
            models.UniqueConstraint(
                fields=["employee", "shift"],
                name="unique_employee_shift",
            ),
        ]

    def __str__(self):
        return f"{self.employee} - {self.shift}"


class Leave(BaseModel):
    employee = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        related_name="leaves",
    )
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    status = models.CharField(max_length=30)
    reason = models.TextField(blank=True)

    class Meta:
        db_table = "leaves"
        ordering = ["-start_at"]

    def __str__(self):
        return f"{self.employee} - {self.start_at}"


class Assignment(BaseModel):
    case = models.ForeignKey(
        "requests.Case",
        on_delete=models.PROTECT,
        related_name="assignments",
    )
    employee = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        related_name="assignments",
    )
    assigned_at = models.DateTimeField()
    accepted_at = models.DateTimeField(
        null=True,
        blank=True,
    )
    released_at = models.DateTimeField(
        null=True,
        blank=True,
    )
    status = models.CharField(max_length=30)
    reason = models.TextField(blank=True)

    class Meta:
        db_table = "assignments"
        ordering = ["-assigned_at"]
        constraints = [
            models.CheckConstraint(
                condition=Q(
                    status__in=[
                        ASSIGNMENT_STATUS_ASSIGNED,
                        ASSIGNMENT_STATUS_ACCEPTED,
                        ASSIGNMENT_STATUS_IN_PROGRESS,
                        ASSIGNMENT_STATUS_COMPLETED,
                        ASSIGNMENT_STATUS_RELEASED,
                    ],
                ),
                name="valid_assignment_status",
            ),
            models.UniqueConstraint(
                fields=["case"],
                condition=Q(
                    status__in=ACTIVE_ASSIGNMENT_STATUSES,
                ),
                name="unique_active_assignment_per_case",
            ),
        ]

    def __str__(self):
        return f"{self.case} - {self.employee}"
