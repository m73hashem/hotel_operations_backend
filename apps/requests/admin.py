from django.contrib import admin

from .models import Case, CaseTimeline, Feedback, Service, WorkOrder


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "department",
        "active",
    )
    search_fields = (
        "name",
        "description",
    )
    list_filter = (
        "department",
        "active",
    )


@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "subject",
        "stay",
        "service",
        "priority",
        "status",
        "completed_at",
    )
    search_fields = (
        "subject",
        "description",
        "stay__guest__first_name",
        "stay__guest__last_name",
        "stay__guest__phone",
    )
    list_filter = (
        "status",
        "priority",
        "service",
    )


@admin.register(WorkOrder)
class WorkOrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "case",
        "department",
        "status",
        "priority",
        "completed_at",
    )
    search_fields = (
        "case__subject",
        "department__name",
    )
    list_filter = (
        "status",
        "priority",
        "department",
    )


@admin.register(CaseTimeline)
class CaseTimelineAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "case",
        "event_type",
        "created_at",
    )
    search_fields = (
        "case__subject",
        "event_type",
        "description",
    )
    list_filter = ("event_type",)


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "case",
        "rating",
        "created_at",
    )
    search_fields = (
        "case__subject",
        "comment",
    )
    list_filter = ("rating",)
    