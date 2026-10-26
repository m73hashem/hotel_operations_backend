from django.contrib import admin

from .models import (
    Assignment,
    Department,
    Employee,
    EmployeeShift,
    Leave,
    Shift,
)


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "status",
    )
    search_fields = ("name",)
    list_filter = ("status",)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "employee_number",
        "name",
        "department",
        "phone",
        "status",
        "user",
    )
    search_fields = (
        "employee_number",
        "name",
        "phone",
        "email",
    )
    list_filter = (
        "department",
        "status",
    )


@admin.register(Shift)
class ShiftAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "start_time",
        "end_time",
        "status",
    )
    search_fields = ("name",)
    list_filter = ("status",)


@admin.register(EmployeeShift)
class EmployeeShiftAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "employee",
        "shift",
        "created_at",
    )
    search_fields = (
        "employee__name",
        "employee__employee_number",
        "shift__name",
    )
    list_filter = ("shift",)


@admin.register(Leave)
class LeaveAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "employee",
        "start_at",
        "end_at",
        "status",
    )
    search_fields = (
        "employee__name",
        "employee__employee_number",
        "reason",
    )
    list_filter = ("status",)


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "case",
        "employee",
        "assigned_at",
        "accepted_at",
        "released_at",
        "status",
    )
    search_fields = (
        "employee__name",
        "employee__employee_number",
    )
    list_filter = (
        "status",
        "employee__department",
    )
    
