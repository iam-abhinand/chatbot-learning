import anthropic
from rest_framework.decorators import api_view
from django.http import JsonResponse
import logging

from .serializers import ChatSerializer, RagChatSerializer
from .rag import retrieve_relevant_chunks
from .tools import TOOL_DEFINITIONS, TOOL_FUNCTIONS

client = anthropic.Anthropic()
logger = logging.getLogger(__name__)

MAX_HISTORY_MESSAGES = 10  # keep only the most recent N messages


def trim_history(messages, max_messages=MAX_HISTORY_MESSAGES):
    """Sliding window: keep only the last N messages."""
    if len(messages) <= max_messages:
        return messages
    return messages[-max_messages:]


@api_view(['POST'])
def chat_view(request):
    serializer = ChatSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    messages = trim_history(list(serializer.validated_data["messages"]))
    model = serializer.validated_data["model"]

    try:
        logger.info(f"Initial messages: {messages}")
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
    return JsonResponse({
        "reply": reply_text,
        "model_used": model,
        "input_tokens": response.usage.input_tokens,
    })


@api_view(['POST'])
def rag_chat_view(request):
    serializer = RagChatSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    question = serializer.validated_data["question"]
    model = serializer.validated_data["model"]
    top_k = serializer.validated_data["top_k"]

    retrieved = retrieve_relevant_chunks(question, top_k=top_k)
    context = "\n".join(doc for doc, _ in retrieved)

    try:
        response = client.messages.create(
            model=model,
            max_tokens=300,
            system=f"Answer the user's question using only this context:\n\n{context}",
            messages=[{"role": "user", "content": question}],
        )
    except anthropic.APIStatusError as e:
        return JsonResponse({"error": e.message}, status=e.status_code)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

    reply_text = "".join(b.text for b in response.content if b.type == "text")

    return JsonResponse({
        "reply": reply_text,
        "model_used": model,
        # returning the retrieved chunks isn't required for the feature 
        # its added here to SEE what informed the answer
        # which is the actual transparency benefit of RAG
        "retrieved_chunks": [{"text": doc, "score": round(score, 3)} for doc, score in retrieved],
    })