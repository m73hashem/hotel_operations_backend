"""Request-shape serializers for operational Request endpoints."""

from rest_framework import serializers


class CreateCaseSerializer(serializers.Serializer):
    """Validate the Create Case request shape."""

    request_id = serializers.IntegerField(min_value=1, required=True)


class CaseListQuerySerializer(serializers.Serializer):
    """Validate query parameters for the operational Case list."""

    search = serializers.CharField(required=False, allow_blank=False, trim_whitespace=True)
    status = serializers.CharField(required=False, allow_blank=False, trim_whitespace=True)
    priority = serializers.CharField(required=False, allow_blank=False, trim_whitespace=True)
    department = serializers.IntegerField(required=False, min_value=1)
    ordering = serializers.ChoiceField(
        required=False,
        choices=(
            "created_at",
            "-created_at",
            "updated_at",
            "-updated_at",
            "priority",
            "-priority",
            "room_number",
            "-room_number",
        ),
    )


class RequestListQuerySerializer(serializers.Serializer):
    """Validate query parameters for the operational Request list."""

    search = serializers.CharField(required=False, allow_blank=False, trim_whitespace=True)
    status = serializers.CharField(required=False, allow_blank=False, trim_whitespace=True)
    ordering = serializers.ChoiceField(
        required=False,
        choices=(
            "created_at",
            "-created_at",
            "updated_at",
            "-updated_at",
            "title",
            "-title",
            "room_number",
            "-room_number",
        ),
    )
