"""Request-shape serializers for employee authentication endpoints."""

from rest_framework import serializers


class EmployeeLoginSerializer(serializers.Serializer):
    """Validate the employee login request shape."""

    username = serializers.CharField(required=True, trim_whitespace=True, max_length=150)
    password = serializers.CharField(required=True, trim_whitespace=False, write_only=True)


class RefreshTokenSerializer(serializers.Serializer):
    """Validate the JWT refresh request shape."""

    refresh_token = serializers.CharField(required=True, trim_whitespace=True)


class LogoutSerializer(serializers.Serializer):
    """Validate the JWT logout request shape."""

    refresh_token = serializers.CharField(required=True, trim_whitespace=True)
