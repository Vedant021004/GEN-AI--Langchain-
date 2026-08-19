"""Small deterministic tools used in the multi-tool demonstrations."""

from langchain_core.tools import tool


@tool
def search(query: str) -> str:
    """Search for information."""
    return f"Searching for: {query}"


@tool
def get_weather(city: str) -> str:
    """Get the weather for a city."""
    return f"Weather information for {city}"


DEMO_TOOLS = [search, get_weather]
