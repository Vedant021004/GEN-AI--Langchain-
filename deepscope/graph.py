"""The DeepScope research graph.

    plan -> research -> reflect -+-> research (next round)
                                 `-> write

Every node appends to `log`, so the UI can render the agent's reasoning live
instead of showing a spinner.
"""

import operator
from collections.abc import Iterator
from typing import Annotated, TypedDict

from langgraph.graph import END, StateGraph

from deepscope.config import Settings
from deepscope.llm import ask, build_llm, parse_string_list
from deepscope.retrieval import DocumentIndex
from deepscope.search import web_search

PLANNER_SYSTEM = (
    "You are a research planner. Break the user's question into 3 to 5 specific, "
    "non-overlapping sub-questions that together answer it. Each sub-question must be "
    "answerable with a single web or document search. Reply ONLY with a JSON array of strings."
)

ANALYST_SYSTEM = (
    "You are a research analyst. Using ONLY the numbered evidence provided, write 2-4 "
    "dense bullet points that answer the sub-question. Every bullet MUST end with the "
    "citation ids it relies on, like [S2] or [S1][S4]. If the evidence does not answer "
    "the sub-question, say so explicitly instead of guessing."
)

CRITIC_SYSTEM = (
    "You are a skeptical research critic. Given a question and the findings gathered so "
    "far, list up to 3 concrete follow-up search queries that would close the most "
    "important remaining gaps (missing numbers, dates, counter-evidence, sources). "
    "If the findings are already sufficient, reply with exactly: SUFFICIENT. "
    "Otherwise reply ONLY with a JSON array of query strings."
)

WRITER_SYSTEM = (
    "You are a research writer. Write a markdown report using ONLY the findings and "
    "evidence given. Structure: '## Answer' (3-5 sentences), '## Key findings' "
    "(bullets), '## Caveats & open questions' (bullets). Preserve the [S#] citations "
    "inline. Never invent facts or citation ids."
)


class Source(TypedDict):
    id: str
    title: str
    url: str
    snippet: str
    origin: str


class Finding(TypedDict):
    question: str
    text: str
    round: int


class ResearchState(TypedDict, total=False):
    question: str
    plan: list[str]
    queue: list[str]
    round: int
    sources: list[Source]
    findings: list[Finding]
    gaps: list[str]
    report: str
    log: Annotated[list[str], operator.add]


def initial_state(question: str) -> ResearchState:
    return {
        "question": question,
        "plan": [],
        "queue": [],
        "round": 0,
        "sources": [],
        "findings": [],
        "gaps": [],
        "report": "",
        "log": [],
    }


def format_evidence(sources: list[Source]) -> str:
    return "\n\n".join(
        f"[{source['id']}] {source['title']} ({source['origin']})\n{source['snippet']}"
        for source in sources
    )


def build_graph(settings: Settings, index: DocumentIndex | None = None):
    """Compile the research graph for one set of settings and uploaded documents."""
    llm = build_llm(settings)
    docs = index or DocumentIndex()

    def register(sources: list[Source], title: str, url: str, snippet: str, origin: str) -> Source | None:
        key = url or f"{origin}:{title}"
        for existing in sources:
            existing_key = existing["url"] or f"{existing['origin']}:{existing['title']}"
            if existing_key == key:
                return None
        source: Source = {
            "id": f"S{len(sources) + 1}",
            "title": title,
            "url": url,
            "snippet": snippet,
            "origin": origin,
        }
        sources.append(source)
        return source

    def plan_node(state: ResearchState) -> ResearchState:
        question = state["question"]
        raw = ask(llm, PLANNER_SYSTEM, f"Question: {question}")
        plan = parse_string_list(raw)[:5] or [question]
        return {
            "plan": plan,
            "queue": list(plan),
            "log": [f"Planned {len(plan)} sub-questions: " + " | ".join(plan)],
        }

    def research_node(state: ResearchState) -> ResearchState:
        sources = list(state.get("sources", []))
        findings = list(state.get("findings", []))
        current_round = state.get("round", 0) + 1
        log: list[str] = []

        for sub_question in state.get("queue", []):
            fresh: list[Source] = []
            for hit in web_search(sub_question, settings):
                added = register(sources, hit.title, hit.url, hit.snippet, hit.provider)
                if added:
                    fresh.append(added)

            for chunk in docs.search(sub_question, k=2):
                label = f"{chunk.document} p.{chunk.page}"
                added = register(sources, label, "", chunk.text, "uploaded document")
                if added:
                    fresh.append(added)

            log.append(
                f"Round {current_round} · searched '{sub_question}' → {len(fresh)} new sources"
            )
            if not fresh:
                findings.append(
                    {
                        "question": sub_question,
                        "text": "- No new evidence found for this sub-question.",
                        "round": current_round,
                    }
                )
                continue

            analysis = ask(
                llm,
                ANALYST_SYSTEM,
                f"Sub-question: {sub_question}\n\nEvidence:\n{format_evidence(fresh)}",
            )
            findings.append({"question": sub_question, "text": analysis, "round": current_round})
            log.append(f"Extracted findings for '{sub_question}'")

        return {
            "sources": sources,
            "findings": findings,
            "round": current_round,
            "queue": [],
            "log": log,
        }

    def reflect_node(state: ResearchState) -> ResearchState:
        if state.get("round", 0) >= settings.max_rounds:
            return {"gaps": [], "queue": [], "log": ["Round budget reached → writing report"]}

        summary = "\n\n".join(
            f"### {item['question']}\n{item['text']}" for item in state.get("findings", [])
        )
        raw = ask(
            llm,
            CRITIC_SYSTEM,
            f"Question: {state['question']}\n\nFindings so far:\n{summary}",
        )
        if "SUFFICIENT" in raw.upper() and "[" not in raw:
            return {"gaps": [], "queue": [], "log": ["Critic: evidence is sufficient"]}

        gaps = parse_string_list(raw)[:3]
        if not gaps:
            return {"gaps": [], "queue": [], "log": ["Critic returned no gaps → writing report"]}
        return {
            "gaps": gaps,
            "queue": gaps,
            "log": ["Critic found gaps: " + " | ".join(gaps)],
        }

    def write_node(state: ResearchState) -> ResearchState:
        findings = "\n\n".join(
            f"### {item['question']}\n{item['text']}" for item in state.get("findings", [])
        )
        sources = state.get("sources", [])
        report = ask(
            llm,
            WRITER_SYSTEM,
            f"Question: {state['question']}\n\nFindings:\n{findings}\n\n"
            f"Evidence:\n{format_evidence(sources)}",
        )
        citations = "\n".join(
            f"- [{source['id']}] {source['title']}" + (f" — {source['url']}" if source["url"] else "")
            for source in sources
        )
        full = f"{report}\n\n## Sources\n{citations}" if citations else report
        return {"report": full, "log": [f"Report written from {len(sources)} sources"]}

    def route(state: ResearchState) -> str:
        return "research" if state.get("queue") else "write"

    graph = StateGraph(ResearchState)
    graph.add_node("plan", plan_node)
    graph.add_node("research", research_node)
    graph.add_node("reflect", reflect_node)
    graph.add_node("write", write_node)
    graph.set_entry_point("plan")
    graph.add_edge("plan", "research")
    graph.add_edge("research", "reflect")
    graph.add_conditional_edges("reflect", route, {"research": "research", "write": "write"})
    graph.add_edge("write", END)
    return graph.compile()


def stream_research(
    question: str, settings: Settings, index: DocumentIndex | None = None
) -> Iterator[tuple[str, ResearchState]]:
    """Yield (node_name, node_update) pairs as the graph executes."""
    app = build_graph(settings, index)
    for update in app.stream(initial_state(question), stream_mode="updates"):
        for node, payload in update.items():
            yield node, payload
