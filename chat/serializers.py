from rest_framework import serializers

ALLOWED_MODELS = [
    "claude-sonnet-4-6",
    "claude-haiku-4-5",
    "claude-opus-4-8"
]

class MessageItemSerializer(serializers.Serializer):
    role = serializers.ChoiceField(choices=["user", "assistant"])
    content = serializers.CharField(allow_blank=False)

class ChatSerializer(serializers.Serializer):
    messages = MessageItemSerializer(many=True)
    model = serializers.ChoiceField(
        choices=ALLOWED_MODELS,
        required=False,
        default="claude-haiku-4-5"
    )

    def validate_messages(self, value):
        if not value:
            raise serializers.ValidationError("Messages cannot be empty.")
        if value[-1]["role"] != "user":
            raise serializers.ValidationError("The last message must be from the user.")
        return value