"""Offline tests: no API keys, no network."""

from deepscope.config import load_settings
from deepscope.graph import format_evidence, initial_state
from deepscope.llm import parse_string_list
from deepscope.retrieval import DocumentIndex, tokenize


def test_settings_report_missing_keys():
    settings = load_settings({})
    assert settings.missing == ["GROQ_API_KEY"]
    assert settings.search_provider == "duckduckgo"

    with_keys = load_settings({"GROQ_API_KEY": "g", "TAVILY_API_KEY": "t"})
    assert with_keys.missing == []
    assert with_keys.has_llm
    assert with_keys.search_provider == "tavily"


def test_parse_string_list_handles_json_and_bullets():
    assert parse_string_list('Sure!\n["a", "b"]') == ["a", "b"]
    assert parse_string_list("- first\n- second") == ["first", "second"]
    assert parse_string_list("") == []


def test_bm25_ranks_relevant_chunk_first():
    index = DocumentIndex()
    index.add_text("LangGraph builds stateful agent graphs with checkpointers.", "notes.pdf", 1)
    index.add_text("Bananas are a good source of potassium.", "notes.pdf", 2)

    hits = index.search("stateful agent graphs", k=1)
    assert len(hits) == 1
    assert "LangGraph" in hits[0].text
    assert hits[0].page == 1
    assert index.documents == ["notes.pdf"]


def test_search_on_empty_index_is_safe():
    assert DocumentIndex().search("anything") == []
    assert tokenize("Hello, World-2024!") == ["hello", "world", "2024"]


def test_format_evidence_includes_citation_ids():
    sources = [
        {"id": "S1", "title": "Paper", "url": "http://x", "snippet": "body", "origin": "tavily"}
    ]
    rendered = format_evidence(sources)
    assert "[S1] Paper (tavily)" in rendered
    assert "body" in rendered


def test_initial_state_defaults():
    state = initial_state("why?")
    assert state["question"] == "why?"
    assert state["round"] == 0
    assert state["sources"] == []
