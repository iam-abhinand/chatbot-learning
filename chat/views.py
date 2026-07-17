import json
import anthropic
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

from .serializers import ChatSerializer

client = anthropic.Anthropic()


@api_view(['POST'])
def chat_view(request):
    serializer = ChatSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user_message = serializer.validated_data["message"]
    model = serializer.validated_data["model"]

    try:
        response = client.messages.create(
            model=model,
            max_tokens=200,
            system="You are a concise assistant",
            messages=[{"role": "user", "content": user_message}]
        )
    except anthropic.APIStatusError as e:
        return JsonResponse({"error": e.message}, status=e.status_code)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

    reply_text = response.content[0].text
    return JsonResponse({"reply": reply_text, "model_used": model})