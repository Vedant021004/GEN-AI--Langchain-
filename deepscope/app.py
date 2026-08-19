"""DeepScope Streamlit UI: ask once, watch the agent research, get a cited report.

Run with:  streamlit run deepscope/app.py
"""

import os
import tempfile

import streamlit as st

from deepscope.config import load_settings
from deepscope.graph import stream_research
from deepscope.retrieval import DocumentIndex

NODE_LABELS = {
    "plan": "🧭 Planner",
    "research": "🔎 Researcher",
    "reflect": "🧐 Critic",
    "write": "✍️ Writer",
}

EXAMPLES = [
    "How are Indian startups using small language models in production?",
    "Compare LangGraph and CrewAI for building multi-agent systems",
    "What does the latest research say about RAG hallucination benchmarks?",
]


def _settings():
    settings = load_settings()
    if not settings.groq_api_key:
        settings.groq_api_key = st.session_state.get("groq_key", "")
        if settings.groq_api_key and "GROQ_API_KEY" in settings.missing:
            settings.missing.remove("GROQ_API_KEY")
    if not settings.tavily_api_key:
        settings.tavily_api_key = st.session_state.get("tavily_key", "")
    return settings


def _index() -> DocumentIndex:
    if "index" not in st.session_state:
        st.session_state["index"] = DocumentIndex()
    return st.session_state["index"]


def _ingest(uploads) -> None:
    index = _index()
    known = set(st.session_state.setdefault("ingested", []))
    for upload in uploads:
        if upload.name in known:
            continue
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as handle:
            handle.write(upload.getbuffer())
            path = handle.name
        try:
            count = index.add_pdf(path, upload.name)
        finally:
            os.unlink(path)
        st.session_state["ingested"].append(upload.name)
        st.sidebar.success(f"Indexed {upload.name} ({count} chunks)")


st.set_page_config(page_title="DeepScope", page_icon="🔬", layout="wide")
st.title("🔬 DeepScope")
st.caption(
    "A LangGraph research agent that plans, searches the web and your documents, "
    "critiques its own findings, then writes a cited report."
)

with st.sidebar:
    st.header("Setup")
    settings = _settings()
    if not settings.groq_api_key:
        st.text_input(
            "Groq API key",
            type="password",
            key="groq_key",
            help="Free at console.groq.com. Set GROQ_API_KEY to skip this box.",
        )
        settings = _settings()
    else:
        st.success("Groq model ready")
    st.text_input(
        "Tavily API key (optional)",
        type="password",
        key="tavily_key",
        help="Without it DeepScope falls back to keyless DuckDuckGo search.",
    )
    settings = _settings()
    st.caption(f"Model: `{settings.model}`  ·  Search: `{settings.search_provider}`")

    settings.max_rounds = st.slider("Research rounds", 1, 3, 2)
    settings.results_per_query = st.slider("Results per query", 2, 8, 4)

    st.header("Your documents (optional)")
    uploads = st.file_uploader("PDFs to research against", type="pdf", accept_multiple_files=True)
    if uploads:
        _ingest(uploads)
    indexed = _index().documents
    if indexed:
        st.caption("Grounded on: " + ", ".join(indexed))

st.session_state.setdefault("question", "")
columns = st.columns(len(EXAMPLES))
for column, example in zip(columns, EXAMPLES):
    if column.button(example, use_container_width=True):
        st.session_state["question"] = example

question = st.text_input("Research question", key="question", placeholder=EXAMPLES[0])
start = st.button("Run research", type="primary")

if start:
    if not question:
        st.warning("Enter a research question first.")
    elif not settings.groq_api_key:
        st.error("A Groq API key is required — add one in the sidebar.")
    else:
        trace_box = st.container()
        report_box = st.empty()
        sources_box = st.empty()
        state = {"sources": [], "findings": [], "plan": [], "report": ""}

        with trace_box:
            st.subheader("Agent trace")
            trace = st.empty()
        lines: list[str] = []

        for node, payload in stream_research(question, settings, _index()):
            for entry in payload.get("log", []):
                lines.append(f"**{NODE_LABELS.get(node, node)}** — {entry}")
            for key in ("sources", "findings", "plan", "report"):
                if key in payload:
                    state[key] = payload[key]
            trace.markdown("\n\n".join(lines))

        if state["report"]:
            report_box.markdown(state["report"])
            st.download_button(
                "Download report (markdown)",
                data=state["report"],
                file_name="deepscope-report.md",
            )
        with sources_box.expander(f"Evidence collected ({len(state['sources'])} sources)"):
            for source in state["sources"]:
                link = f"[{source['title']}]({source['url']})" if source["url"] else source["title"]
                st.markdown(f"**[{source['id']}]** {link}  · _{source['origin']}_")
                st.caption(source["snippet"][:400])
