
def count_words(text: str) -> str:
    """Count words and characters in a piece of text."""
    words = len(text.split())
    chars = len(text)
    return f"{words} words, {chars} characters"

TOOL_DEFINITIONS = [
    {
        "name": "count_words",
        "description": "Count the number of words and characters in a given text.",
        "input_schema": {
            "type": "object",
            "properties": {
                "text": {"type": "string", "description": "The text to count."}
            },
            "required": ["text"],
        },
    }
]

TOOL_FUNCTIONS = {"count_words": count_words}