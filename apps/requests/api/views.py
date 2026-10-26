"""API endpoints for operational Request actions."""

from dataclasses import asdict

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.requests.api.serializers import (
    CaseListQuerySerializer,
    CreateCaseSerializer,
    RequestListQuerySerializer,
)
from apps.requests.use_cases import CreateCaseUseCase, ListCasesUseCase, ListRequestsUseCase
from apps.users.permissions import CanCreateCases, CanViewDashboard
from core.pagination import DefaultPagination
from core.responses import ApiResponse


class CreateCaseAPIView(APIView):
    """Create one operational Case from an existing Request."""

    serializer_class = CreateCaseSerializer
    permission_classes = [IsAuthenticated, CanCreateCases]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = CreateCaseUseCase.execute(
            serializer.validated_data["request_id"],
        )

        return ApiResponse.success(
            data=asdict(result),
            message="Case created successfully.",
            status=status.HTTP_201_CREATED,
        )


class CaseListAPIView(APIView):
    """Return department-visible operational Cases."""

    serializer_class = CaseListQuerySerializer
    permission_classes = [IsAuthenticated, CanViewDashboard]

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        result = ListCasesUseCase.execute(
            request.user.id,
            **serializer.validated_data,
        )
        paginator = DefaultPagination()
        page = paginator.paginate_queryset(result, request, view=self)
        page_data = page if page is not None else result

        return ApiResponse.success(
            data={
                "count": paginator.page.paginator.count if page is not None else len(page_data),
                "next": paginator.get_next_link() if page is not None else None,
                "previous": paginator.get_previous_link() if page is not None else None,
                "results": [asdict(case) for case in page_data],
            },
            message="Cases retrieved successfully.",
            status=status.HTTP_200_OK,
        )


class RequestListAPIView(APIView):
    """Return operational Requests."""

    serializer_class = RequestListQuerySerializer
    permission_classes = [IsAuthenticated, CanViewDashboard]

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        result = ListRequestsUseCase.execute(
            request.user.id,
            **serializer.validated_data,
        )
        paginator = DefaultPagination()
        page = paginator.paginate_queryset(result, request, view=self)
        page_data = page if page is not None else result

        return ApiResponse.success(
            data={
                "count": paginator.page.paginator.count if page is not None else len(page_data),
                "next": paginator.get_next_link() if page is not None else None,
                "previous": paginator.get_previous_link() if page is not None else None,
                "results": [asdict(item) for item in page_data],
            },
            message="Requests retrieved successfully.",
            status=status.HTTP_200_OK,
        )
