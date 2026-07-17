from rest_framework import serializers

ALLOWED_MODELS = [
    "claude-sonnet-4-6",
    "claude-haiku-4-5",
]

class ChatSerializer(serializers.Serializer):
    message = serializers.CharField(allow_blank=False, max_length=2000)
    model = serializers.ChoiceField(
        choices=ALLOWED_MODELS,
        required=False,
        default="claude-haiku-4-5"
    )

    def validate(self, attrs):
        if not attrs.get("message"):
            raise serializers.ValidationError("Message is required")
        if len(attrs.get("message")) > 2000:
            raise serializers.ValidationError("Message is too long")
        return attrs