"""Web search providers: Tavily when a key exists, DuckDuckGo otherwise."""

from dataclasses import dataclass

from deepscope.config import Settings


@dataclass
class SearchHit:
    title: str
    url: str
    snippet: str
    provider: str


def _tavily(query: str, api_key: str, limit: int) -> list[SearchHit]:
    from langchain_tavily import TavilySearch

    tool = TavilySearch(max_results=limit, tavily_api_key=api_key)
    payload = tool.invoke({"query": query})
    raw = payload.get("results", []) if isinstance(payload, dict) else []
    hits = []
    for item in raw:
        if not isinstance(item, dict):
            continue
        hits.append(
            SearchHit(
                title=str(item.get("title", "Untitled")),
                url=str(item.get("url", "")),
                snippet=str(item.get("content", ""))[:1200],
                provider="tavily",
            )
        )
    return hits


def _duckduckgo(query: str, limit: int) -> list[SearchHit]:
    from ddgs import DDGS

    with DDGS() as client:
        raw = client.text(query, max_results=limit)
    hits = []
    for item in raw:
        hits.append(
            SearchHit(
                title=str(item.get("title", "Untitled")),
                url=str(item.get("href", "")),
                snippet=str(item.get("body", ""))[:1200],
                provider="duckduckgo",
            )
        )
    return hits


def web_search(query: str, settings: Settings, limit: int | None = None) -> list[SearchHit]:
    """Run one web query, degrading gracefully if the provider fails."""
    count = limit or settings.results_per_query
    try:
        if settings.tavily_api_key:
            return _tavily(query, settings.tavily_api_key, count)
        return _duckduckgo(query, count)
    except Exception as exc:  # provider outages must not kill the research run
        return [
            SearchHit(
                title="Search unavailable",
                url="",
                snippet=f"Search provider error for '{query}': {exc}",
                provider="error",
            )
        ]
