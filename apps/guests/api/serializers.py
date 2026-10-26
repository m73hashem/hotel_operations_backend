from rest_framework import serializers

from apps.guests.models import Guest


class GuestSerializer(serializers.ModelSerializer):

    class Meta:
        model = Guest

        fields = "__all__"

        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )


class GuestListQuerySerializer(serializers.Serializer):
    """Validate query parameters for the operational Guest list."""

    search = serializers.CharField(required=False, allow_blank=False, trim_whitespace=True)
    active_stay = serializers.BooleanField(required=False)
    ordering = serializers.ChoiceField(
        required=False,
        choices=(
            "created_at",
            "-created_at",
            "updated_at",
            "-updated_at",
            "first_name",
            "-first_name",
            "last_name",
            "-last_name",
            "full_name",
            "-full_name",
        ),
    )


class StayListQuerySerializer(serializers.Serializer):
    """Validate query parameters for the operational Stay list."""

    search = serializers.CharField(required=False, allow_blank=False, trim_whitespace=True)
    status = serializers.CharField(required=False, allow_blank=False, trim_whitespace=True)
    ordering = serializers.ChoiceField(
        required=False,
        choices=(
            "check_in",
            "-check_in",
            "expected_check_out",
            "-expected_check_out",
            "created_at",
            "-created_at",
            "updated_at",
            "-updated_at",
            "room_number",
            "-room_number",
        ),
    )
