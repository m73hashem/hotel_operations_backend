from dataclasses import asdict

from rest_framework import status
from rest_framework.views import APIView

from apps.chat.api.serializers import (
    ConversationHistorySerializer,
    CreateRequestSerializer,
    SendMessageSerializer,
    StartChatSessionSerializer,
)
from apps.chat.use_cases.create_request import CreateRequestUseCase
from apps.chat.use_cases.conversation_history import ConversationHistoryUseCase
from apps.chat.use_cases.start_chat_session import StartChatSessionUseCase
from apps.chat.use_cases.send_message import SendMessageUseCase
from core.responses import ApiResponse


class StartChatSessionAPIView(APIView):
    """Initialize a guest chat session."""

    serializer_class = StartChatSessionSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = StartChatSessionUseCase.execute(
            serializer.validated_data["session_token"],
        )

        return ApiResponse.success(
            data=asdict(result),
            message="Chat session initialized successfully.",
            status=status.HTTP_200_OK,
        )


class ConversationHistoryAPIView(APIView):
    """Return the authenticated guest's active General Conversation history."""


    def get(self, request, *args, **kwargs):
        serializer = ConversationHistorySerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        result = ConversationHistoryUseCase.execute(
            serializer.validated_data["session_token"],
        )

        return ApiResponse.success(
            data=asdict(result),
            message="Conversation history retrieved successfully.",
            status=status.HTTP_200_OK,
        )


class SendMessageAPIView(APIView):
    """Persist one guest message in the active General Conversation."""

    serializer_class = SendMessageSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = SendMessageUseCase.execute(
            session_token=serializer.validated_data["session_token"],
            message=serializer.validated_data["message"],
        )

        return ApiResponse.success(
            data=asdict(result),
            message="Message sent successfully.",
            status=status.HTTP_201_CREATED,
        )


class ChatMessagesAPIView(SendMessageAPIView, ConversationHistoryAPIView):
    """Expose independent message-history and send-message handlers at one path."""


class CreateRequestAPIView(APIView):
    """Create one service Request for the authenticated guest."""

    serializer_class = CreateRequestSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = CreateRequestUseCase.execute(
            session_token=serializer.validated_data["session_token"],
            message=serializer.validated_data["message"],
        )

        return ApiResponse.success(
            data=asdict(result),
            message="Request created successfully.",
            status=status.HTTP_201_CREATED,
        )
