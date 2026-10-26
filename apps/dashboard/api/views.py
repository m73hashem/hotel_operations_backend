"""API endpoints for employee operational dashboards."""

from dataclasses import asdict

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.dashboard.api.serializers import (
    CaseDetailsSerializer,
    DepartmentQueueQuerySerializer,
    DashboardQuerySerializer,
    MyAssignmentsQuerySerializer,
)
from apps.dashboard.use_cases import (
    CaseDetailsUseCase,
    DashboardSummaryUseCase,
    DashboardStatisticsUseCase,
    DashboardMetricsUseCase,
    DashboardWidgetsUseCase,
    DepartmentQueueUseCase,
    MyAssignmentsUseCase,
)
from apps.users.permissions import CanViewDashboard
from core.pagination import DefaultPagination
from core.responses import ApiResponse


class DashboardSummaryAPIView(APIView):
    """Return dashboard summary information for the authenticated Employee."""

    permission_classes = [IsAuthenticated, CanViewDashboard]
    serializer_class = DashboardQuerySerializer

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        result = DashboardSummaryUseCase.execute(user_id=request.user.id)

        return ApiResponse.success(
            data=asdict(result),
            message="Dashboard summary retrieved successfully.",
            status=status.HTTP_200_OK,
        )


class DashboardStatisticsAPIView(APIView):
    """Return department-scoped operational statistics for one Employee."""

    permission_classes = [IsAuthenticated, CanViewDashboard]
    serializer_class = DashboardQuerySerializer

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        result = DashboardStatisticsUseCase.execute(user_id=request.user.id)

        return ApiResponse.success(
            data=asdict(result),
            message="Dashboard statistics retrieved successfully.",
            status=status.HTTP_200_OK,
        )


class DashboardMetricsAPIView(APIView):
    """Return department-scoped operational metrics for one Employee."""

    permission_classes = [IsAuthenticated, CanViewDashboard]
    serializer_class = DashboardQuerySerializer

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        result = DashboardMetricsUseCase.execute(user_id=request.user.id)

        return ApiResponse.success(
            data=asdict(result),
            message="Dashboard metrics retrieved successfully.",
            status=status.HTTP_200_OK,
        )


class DashboardWidgetsAPIView(APIView):
    """Return operational dashboard widgets for one Employee."""

    permission_classes = [IsAuthenticated, CanViewDashboard]
    serializer_class = DashboardQuerySerializer

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        result = DashboardWidgetsUseCase.execute(user_id=request.user.id)

        return ApiResponse.success(
            data=asdict(result),
            message="Dashboard widgets retrieved successfully.",
            status=status.HTTP_200_OK,
        )


class MyAssignmentsAPIView(APIView):
    """Return active and historical Assignments for the authenticated Employee."""

    permission_classes = [IsAuthenticated, CanViewDashboard]
    serializer_class = MyAssignmentsQuerySerializer

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        result = MyAssignmentsUseCase.execute(
            user_id=request.user.id,
            **serializer.validated_data,
        )
        paginator = DefaultPagination()
        page = paginator.paginate_queryset(result.assignments, request, view=self)
        page_data = page if page is not None else result.assignments

        return ApiResponse.success(
            data={
                "count": paginator.page.paginator.count if page is not None else len(page_data),
                "next": paginator.get_next_link() if page is not None else None,
                "previous": paginator.get_previous_link() if page is not None else None,
                "results": [asdict(assignment) for assignment in page_data],
            },
            message="My assignments retrieved successfully.",
            status=status.HTTP_200_OK,
        )


class DepartmentQueueAPIView(APIView):
    """Return the authenticated Employee department's operational Case queue."""

    permission_classes = [IsAuthenticated, CanViewDashboard]
    serializer_class = DepartmentQueueQuerySerializer

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        result = DepartmentQueueUseCase.execute(
            user_id=request.user.id,
            **serializer.validated_data,
        )
        paginator = DefaultPagination()
        page = paginator.paginate_queryset(result.cases, request, view=self)
        page_data = page if page is not None else result.cases

        return ApiResponse.success(
            data={
                "count": paginator.page.paginator.count if page is not None else len(page_data),
                "next": paginator.get_next_link() if page is not None else None,
                "previous": paginator.get_previous_link() if page is not None else None,
                "results": [asdict(case) for case in page_data],
            },
            message="Department queue retrieved successfully.",
            status=status.HTTP_200_OK,
        )


class CaseDetailsAPIView(APIView):
    """Return one Case and its related timeline, messages, and Request details."""

    permission_classes = [IsAuthenticated, CanViewDashboard]
    serializer_class = CaseDetailsSerializer

    def get(self, request, case_id, *args, **kwargs):
        serializer = self.serializer_class(data={"case_id": case_id})
        serializer.is_valid(raise_exception=True)

        result = CaseDetailsUseCase.execute(
            case_id=serializer.validated_data["case_id"],
        )

        return ApiResponse.success(
            data=asdict(result),
            message="Case details retrieved successfully.",
            status=status.HTTP_200_OK,
        )
