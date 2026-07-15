from rest_framework import serializers

class ChatSerializer(serializers.Serializer):
    message = serializers.CharField(allow_blank=False, max_length=2000)

    def validate(self, attrs):
        if not attrs.get("message"):
            raise serializers.ValidationError("Message is required")
        if len(attrs.get("message")) > 2000:
            raise serializers.ValidationError("Message is too long")
        return attrs