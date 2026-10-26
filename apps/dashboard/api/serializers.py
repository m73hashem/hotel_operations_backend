"""Request-shape serializers for dashboard read endpoints."""

from rest_framework import serializers


class DashboardQuerySerializer(serializers.Serializer):
    """Validate the intentionally empty dashboard query shape."""


class CaseDetailsSerializer(serializers.Serializer):
    """Validate the Case identifier supplied in the URL path."""

    case_id = serializers.IntegerField(min_value=1, required=True)


class MyAssignmentsQuerySerializer(serializers.Serializer):
    """Validate query shape for the My Assignments dashboard list."""

    search = serializers.CharField(required=False, allow_blank=False, trim_whitespace=True)
    assignment_status = serializers.CharField(
        required=False,
        allow_blank=False,
        trim_whitespace=True,
    )
    case_status = serializers.CharField(required=False, allow_blank=False, trim_whitespace=True)
    priority = serializers.CharField(required=False, allow_blank=False, trim_whitespace=True)
    ordering = serializers.ChoiceField(
        required=False,
        choices=(
            "created_at",
            "-created_at",
            "updated_at",
            "-updated_at",
            "assigned_at",
            "-assigned_at",
            "priority",
            "-priority",
            "room_number",
            "-room_number",
        ),
    )


class DepartmentQueueQuerySerializer(serializers.Serializer):
    """Validate query shape for the Department Queue dashboard list."""

    search = serializers.CharField(required=False, allow_blank=False, trim_whitespace=True)
    case_status = serializers.CharField(required=False, allow_blank=False, trim_whitespace=True)
    priority = serializers.CharField(required=False, allow_blank=False, trim_whitespace=True)
    ordering = serializers.ChoiceField(
        required=False,
        choices=(
            "created_at",
            "-created_at",
            "updated_at",
            "-updated_at",
            "assigned_at",
            "-assigned_at",
            "priority",
            "-priority",
            "room_number",
            "-room_number",
        ),
    )
