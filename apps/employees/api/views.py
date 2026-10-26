"""API endpoints for Employee operations."""

from dataclasses import asdict

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.employees.api.serializers import (
    AcceptAssignmentSerializer,
    AssignCaseSerializer,
    CloseCaseSerializer,
    CompleteWorkSerializer,
    StartWorkSerializer,
)
from apps.employees.use_cases.accept_assignment import AcceptAssignmentUseCase
from apps.employees.use_cases.assign_case import AssignCaseUseCase
from apps.employees.use_cases.complete_work import CompleteWorkUseCase
from apps.employees.use_cases.close_case import CloseCaseUseCase
from apps.employees.use_cases.start_work import StartWorkUseCase
from apps.users.permissions import (
    CanAcceptAssignments,
    CanAssignCases,
    CanCloseCases,
    CanCompleteWork,
    CanStartWork,
)
from core.responses import ApiResponse


class AssignCaseAPIView(APIView):
    """Assign one Employee to an existing Case."""

    serializer_class = AssignCaseSerializer
    permission_classes = [IsAuthenticated, CanAssignCases]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = AssignCaseUseCase.execute(
            case_id=serializer.validated_data["case_id"],
            employee_id=serializer.validated_data["employee_id"],
        )

        return ApiResponse.success(
            data=asdict(result),
            message="Case assigned successfully.",
            status=status.HTTP_201_CREATED,
        )


class AcceptAssignmentAPIView(APIView):
    """Accept one assigned Case Assignment."""

    serializer_class = AcceptAssignmentSerializer
    permission_classes = [IsAuthenticated, CanAcceptAssignments]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = AcceptAssignmentUseCase.execute(
            assignment_id=serializer.validated_data["assignment_id"],
        )

        return ApiResponse.success(
            data=asdict(result),
            message="Assignment accepted successfully.",
            status=status.HTTP_200_OK,
        )


class StartWorkAPIView(APIView):
    """Start work on one accepted Case Assignment."""

    serializer_class = StartWorkSerializer
    permission_classes = [IsAuthenticated, CanStartWork]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = StartWorkUseCase.execute(
            assignment_id=serializer.validated_data["assignment_id"],
        )

        return ApiResponse.success(
            data=asdict(result),
            message="Work started successfully.",
            status=status.HTTP_200_OK,
        )


class CompleteWorkAPIView(APIView):
    """Complete work on one in-progress Case Assignment."""

    serializer_class = CompleteWorkSerializer
    permission_classes = [IsAuthenticated, CanCompleteWork]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = CompleteWorkUseCase.execute(
            assignment_id=serializer.validated_data["assignment_id"],
        )

        return ApiResponse.success(
            data=asdict(result),
            message="Work completed successfully.",
            status=status.HTTP_200_OK,
        )


class CloseCaseAPIView(APIView):
    """Close one completed Case and release its Assignment."""

    serializer_class = CloseCaseSerializer
    permission_classes = [IsAuthenticated, CanCloseCases]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = CloseCaseUseCase.execute(
            case_id=serializer.validated_data["case_id"],
        )

        return ApiResponse.success(
            data=asdict(result),
            message="Case closed successfully.",
            status=status.HTTP_200_OK,
        )
