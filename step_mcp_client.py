import asyncio

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

server_params = StdioServerParameters(
    command="python",
    args=["step_mcp_server.py"],  # the client launches the server itself
)


async def main():
    async with stdio_client(server_params) as (read, write), ClientSession(read, write) as session:
        await session.initialize()

        # Ask the server what tools it exposes — this is the actual
        # "discovery" MCP provides. The client didn't need to know
        # count_words/reverse_text existed in advance.
        tools = await session.list_tools()
        print("Available tools:")
        for tool in tools.tools:
            print(f"  - {tool.name}: {tool.description}")

        # Now actually call one
        result = await session.call_tool("reverse_text", {"text": "hello mcp"})
        print("\nreverse_text result:", result.content[0].text)


asyncio.run(main())


""" From my Output:
Available tools:
  - count_words: Count words and characters in a piece of text.
  - reverse_text: Reverse a string of text.

reverse_text result: pcm olleh
"""