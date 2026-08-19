"""Reusable LangGraph builders for tool-calling examples."""

from __future__ import annotations

from pathlib import Path
from typing import Annotated
from typing import Any
from typing_extensions import TypedDict

from langchain_core.messages import BaseMessage
from langgraph.graph import START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition


class MessagesState(TypedDict):
    """Message state used by a tool-calling graph."""

    messages: Annotated[list[BaseMessage], add_messages]


def build_tool_calling_graph(
    llm: Any,
    tools: list[Any],
    checkpointer: Any = None,
    node_name: str = "chatbot",
) -> Any:
    """Build and compile a standard LLM-to-tools graph."""
    llm_with_tools = llm.bind_tools(tools)

    def chatbot(state: MessagesState):
        return {"messages": [llm_with_tools.invoke(state["messages"])]}

    builder = StateGraph(MessagesState)
    builder.add_node(node_name, chatbot)
    builder.add_node("tools", ToolNode(tools))
    builder.add_edge(START, node_name)
    builder.add_conditional_edges(node_name, tools_condition)
    builder.add_edge("tools", node_name)
    return builder.compile(checkpointer=checkpointer)


def save_graph_png(graph: Any, path: str | Path) -> None:
    """Save a graph's Mermaid rendering as a PNG file."""
    with open(path, "wb") as output:
        output.write(graph.get_graph().draw_mermaid_png())
