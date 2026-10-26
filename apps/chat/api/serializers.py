from rest_framework import serializers


class StartChatSessionSerializer(serializers.Serializer):
    """Validate the Start Chat Session request shape."""

    session_token = serializers.CharField(
        max_length=128,
        required=True,
        trim_whitespace=True,
    )


class SendMessageSerializer(serializers.Serializer):
    """Validate the Send Message request shape."""

    session_token = serializers.CharField(
        max_length=128,
        required=True,
        trim_whitespace=True,
    )
    message = serializers.CharField(
        required=True,
        trim_whitespace=False,
    )


class ConversationHistorySerializer(serializers.Serializer):
    """Validate the Conversation History request shape."""

    session_token = serializers.CharField(
        max_length=128,
        required=True,
        trim_whitespace=True,
    )


class CreateRequestSerializer(serializers.Serializer):
    """Validate the Create Request request shape."""

    session_token = serializers.CharField(
        max_length=128,
        required=True,
        trim_whitespace=True,
    )
    message = serializers.CharField(
        max_length=255,
        required=True,
        trim_whitespace=False,
    )
