import anthropic
from rest_framework.decorators import api_view
from django.http import JsonResponse

from .serializers import ChatSerializer
from .tools import TOOL_DEFINITIONS, TOOL_FUNCTIONS

client = anthropic.Anthropic()


@api_view(['POST'])
def chat_view(request):
    serializer = ChatSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user_message = serializer.validated_data["message"]
    model = serializer.validated_data["model"]

    messages = [{"role": "user", "content": user_message}]

    try:
        response = client.messages.create(
            model=model,
            max_tokens=500,
            tools=TOOL_DEFINITIONS,
            system="You are a concise assistant. Use the count_words tool whenever the user asks about word or character counts, instead of counting yourself.",
            messages=messages,
        )

        # Added Loop here instead of a single check cause - Claude could call the tool more than
        # once (e.g. counting two separate pieces of text) before it's
        # actually ready to give a final text answer.
        while response.stop_reason == "tool_use":
            tool_use_blocks = [b for b in response.content if b.type == "tool_use"]

            messages.append({"role": "assistant", "content": response.content})

            tool_results = []
            for block in tool_use_blocks:
                func = TOOL_FUNCTIONS[block.name]
                result = func(**block.input)
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": result,
                })

            messages.append({"role": "user", "content": tool_results})

            response = client.messages.create(
                model=model,
                max_tokens=500,
                tools=TOOL_DEFINITIONS,
                system="You are a concise assistant. Use the count_words tool whenever the user asks about word or character counts, instead of counting yourself.",
                messages=messages,
            )

    except anthropic.APIStatusError as e:
        return JsonResponse({"error": e.message}, status=e.status_code)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

    reply_text = "".join(b.text for b in response.content if b.type == "text")
    return JsonResponse({"reply": reply_text, "model_used": model})