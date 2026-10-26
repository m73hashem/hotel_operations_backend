from django.urls import path

from .views import ChatMessagesAPIView, CreateRequestAPIView, StartChatSessionAPIView

app_name = "chat"

urlpatterns = [
    path(
        "start-session/",
        StartChatSessionAPIView.as_view(),
        name="start-session",
    ),
    path(
        "messages/",
        ChatMessagesAPIView.as_view(),
        name="send-message",
    ),
    path(
        "create-request/",
        CreateRequestAPIView.as_view(),
        name="create-request",
    ),
]
