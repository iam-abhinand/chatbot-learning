import anthropic

client = anthropic.Anthropic()

# creatinga testing example for a conversation that's grown over several turns.
conversation = [
    {"role": "user", "content": "What's the capital of France?"},
    {"role": "assistant", "content": "The capital of France is Paris."},
    {"role": "user", "content": "What's a famous landmark there?"},
    {"role": "assistant", "content": "The Eiffel Tower is probably the most famous landmark in Paris."},
    {"role": "user", "content": "How tall is it?"},
    {"role": "assistant", "content": "The Eiffel Tower is approximately 330 meters (1,083 feet) tall, including its antennas."},
    {"role": "user", "content": "When was it built?"},
]

count = client.messages.count_tokens(
    model="claude-haiku-4-5",
    system="You are a concise assistant.",
    messages=conversation,
)

print(count)