import anthropic

client = anthropic.Anthropic()


def count_words(text: str) -> str:
    return f"{len(text.split())} words, {len(text)} characters"


def reverse_text(text: str) -> str:
    return text[::-1]


TOOLS = [
    {
        "name": "count_words",
        "description": "Count words and characters in text.",
        "input_schema": {
            "type": "object",
            "properties": {"text": {"type": "string"}},
            "required": ["text"],
        },
    },
    {
        "name": "reverse_text",
        "description": "Reverse a string of text.",
        "input_schema": {
            "type": "object",
            "properties": {"text": {"type": "string"}},
            "required": ["text"],
        },
    },
]

FUNCTIONS = {"count_words": count_words, "reverse_text": reverse_text}

MAX_ITERATIONS = 5  # the hard stop
messages = [
    {
        "role": "user",
        "content": "Reverse the text 'hello world', then tell me how many words and characters are in the reversed version.",
    }
]

for iteration in range(MAX_ITERATIONS):
    response = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=500,
        tools=TOOLS,
        messages=messages,
    )

    print(f"\n--- iteration {iteration + 1}, stop_reason: {response.stop_reason} ---")

    if response.stop_reason != "tool_use":
        # Claude is done — print the final answer and stop the loop.
        final_text = "".join(b.text for b in response.content if b.type == "text")
        print("FINAL ANSWER:", final_text)
        break

    tool_use_blocks = [b for b in response.content if b.type == "tool_use"]
    messages.append({"role": "assistant", "content": response.content})

    tool_results = []
    for block in tool_use_blocks:
        print(f"  Claude is calling: {block.name}({block.input})")
        result = FUNCTIONS[block.name](**block.input)
        print(f"  -> result: {result}")
        tool_results.append({"type": "tool_result", "tool_use_id": block.id, "content": result})

    messages.append({"role": "user", "content": tool_results})

else:
    print(f"\nStopped after hitting MAX_ITERATIONS ({MAX_ITERATIONS}) without a final answer.")


"""
 OUTPUT :

--- iteration 1, stop_reason: tool_use ---
  Claude is calling: reverse_text({'text': 'hello world'})
  -> result: dlrow olleh

--- iteration 2, stop_reason: tool_use ---
  Claude is calling: count_words({'text': 'dlrow olleh'})
  -> result: 2 words, 11 characters

--- iteration 3, stop_reason: end_turn ---
FINAL ANSWER: Perfect! Here are the results:

- **Reversed text**: 'dlrow olleh'
- **Word count**: 2 words
- **Character count**: 11 characters (including the space between the words)

"""
