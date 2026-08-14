from mcp.server import MCPServer

"""
FastMCP is a high-level wrapper — it turns a decorated Python function
directly into an MCP tool, generating the JSON schema from the function's
type hints and docstring automatically. Compare this to TOOL_DEFINITIONS
in tools.py, where i added that schema manually — MCP's SDK does that step
from ordinary Python.
"""
mcp = MCPServer("learning-tools") 


@mcp.tool()
def count_words(text: str) -> str:
    """Count words and characters in a piece of text."""
    return f"{len(text.split())} words, {len(text)} characters"


@mcp.tool()
def reverse_text(text: str) -> str:
    """Reverse a string of text."""
    return text[::-1]


if __name__ == "__main__":
    mcp.run()