"""API endpoints for employee authentication."""

from dataclasses import asdict

from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView

from apps.users.api.serializers import (
    EmployeeLoginSerializer,
    LogoutSerializer,
    RefreshTokenSerializer,
)
from apps.users.use_cases.current_employee import CurrentEmployeeUseCase
from apps.users.use_cases.employee_login import EmployeeLoginUseCase
from apps.users.use_cases.logout import LogoutUseCase
from apps.users.use_cases.refresh_token import RefreshTokenUseCase
from core.responses import ApiResponse


class EmployeeLoginAPIView(APIView):
    """Authenticate one Employee and return a Simple JWT token pair."""

    permission_classes = [AllowAny]
    serializer_class = EmployeeLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = EmployeeLoginUseCase.execute(**serializer.validated_data)

        return ApiResponse.success(
            data=asdict(result),
            message="Employee logged in successfully.",
            status=status.HTTP_200_OK,
        )


class CurrentEmployeeAPIView(APIView):
    """Return the authenticated Employee profile."""

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        result = CurrentEmployeeUseCase.execute(user_id=request.user.id)

        return ApiResponse.success(
            data=asdict(result),
            message="Current employee retrieved successfully.",
            status=status.HTTP_200_OK,
        )


class RefreshTokenAPIView(APIView):
    """Exchange a valid Simple JWT refresh token for a new access token."""

    permission_classes = [AllowAny]
    serializer_class = RefreshTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = RefreshTokenUseCase.execute(
            refresh_token=serializer.validated_data["refresh_token"],
        )

        return ApiResponse.success(
            data=asdict(result),
            message="Access token refreshed successfully.",
            status=status.HTTP_200_OK,
        )


class LogoutAPIView(APIView):
    """Blacklist one Simple JWT refresh token."""

    permission_classes = [AllowAny]
    serializer_class = LogoutSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = LogoutUseCase.execute(
            refresh_token=serializer.validated_data["refresh_token"],
        )

        return ApiResponse.success(
            data=asdict(result),
            message="Logged out successfully.",
            status=status.HTTP_200_OK,
        )
