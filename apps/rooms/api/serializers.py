"""Request-shape serializers for operational Room endpoints."""

from rest_framework import serializers


class RoomListQuerySerializer(serializers.Serializer):
    """Validate query parameters for the operational Room list."""

    search = serializers.CharField(required=False, allow_blank=False, trim_whitespace=True)
    status = serializers.CharField(required=False, allow_blank=False, trim_whitespace=True)
    ordering = serializers.ChoiceField(
        required=False,
        choices=(
            "created_at",
            "-created_at",
            "updated_at",
            "-updated_at",
            "room_number",
            "-room_number",
            "room_type",
            "-room_type",
        ),
    )
