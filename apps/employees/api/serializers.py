"""Request-shape serializers for Employee operations."""

from rest_framework import serializers


class AssignCaseSerializer(serializers.Serializer):
    """Validate the Assign Case request shape."""

    case_id = serializers.IntegerField(min_value=1, required=True)
    employee_id = serializers.IntegerField(min_value=1, required=True)


class AcceptAssignmentSerializer(serializers.Serializer):
    """Validate the Accept Assignment request shape."""

    assignment_id = serializers.IntegerField(min_value=1, required=True)


class StartWorkSerializer(serializers.Serializer):
    """Validate the Start Work request shape."""

    assignment_id = serializers.IntegerField(min_value=1, required=True)


class CompleteWorkSerializer(serializers.Serializer):
    """Validate the Complete Work request shape."""

    assignment_id = serializers.IntegerField(min_value=1, required=True)


class CloseCaseSerializer(serializers.Serializer):
    """Validate the Close Case request shape."""

    case_id = serializers.IntegerField(min_value=1, required=True)
