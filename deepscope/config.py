"""Runtime configuration for DeepScope."""

import os
from dataclasses import dataclass, field

# Override with DEEPSCOPE_MODEL if your Groq account exposes a different set.
DEFAULT_MODEL = "openai/gpt-oss-120b"


@dataclass
class Settings:
    """Everything the agent needs to know about its environment."""

    groq_api_key: str = ""
    tavily_api_key: str = ""
    model: str = DEFAULT_MODEL
    temperature: float = 0.2
    max_rounds: int = 2
    results_per_query: int = 4
    missing: list[str] = field(default_factory=list)

    @property
    def has_llm(self) -> bool:
        return bool(self.groq_api_key)

    @property
    def search_provider(self) -> str:
        return "tavily" if self.tavily_api_key else "duckduckgo"


def load_settings(env: dict[str, str] | None = None) -> Settings:
    """Read settings from the environment, recording what is missing."""
    source = dict(os.environ) if env is None else env
    settings = Settings(
        groq_api_key=source.get("GROQ_API_KEY", "").strip(),
        tavily_api_key=source.get("TAVILY_API_KEY", "").strip(),
        model=source.get("DEEPSCOPE_MODEL", DEFAULT_MODEL).strip() or DEFAULT_MODEL,
    )
    if not settings.groq_api_key:
        settings.missing.append("GROQ_API_KEY")
    return settings
