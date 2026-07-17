import anthropic

client = anthropic.Anthropic()

tools = [
    {
        "name" : "get_weather",
        "description" : "Get the current weather for the given city.",
        "input_schema" : {
            "type" : "object",
            "properties" : {
                "city" : {
                    "type" : "string",
                    "description" : "City name, e.g. Kochi"
                }
            },
            "required" : ["city"],
        }

    }
]

# The actual Python function Claude's "request" will map to.
# Faked for now — the point of this step is the protocol, (not real weather data.)
def get_weather(city: str) -> str:
    return f"{city}: 31°C, humid, light rain expected later."


messages = [{"role": "user", "content": "What's the weather like in Kochi right now?"}]

response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=500,
    tools=tools,
    messages=messages,
)

print("stop_reason:", response.stop_reason)
print("content:", response.content)