from dotenv import load_dotenv
from langchain_groq import ChatGroq

from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages

from typing import Annotated
from typing_extensions import TypedDict

from langgraph.prebuilt import ToolNode, tools_condition

from langchain_core.tools import tool
from langchain_core.messages import BaseMessage


load_dotenv()


# ---------------- LLM ----------------

llm = ChatGroq(
    model="openai/gpt-oss-20b",
)


# ---------------- TOOLS ----------------

@tool
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b


@tool
def subtract(a: int, b: int) -> int:
    """Subtract b from a."""
    return a - b


@tool
def search(query: str) -> str:
    """Search for information."""
    return f"Searching for: {query}"


@tool
def get_weather(city: str) -> str:
    """Get the weather for a city."""
    return f"Weather information for {city}"


# ---------------- BIND TOOLS ----------------

tools = [
    add,
    subtract,
    search,
    get_weather
]

llm_with_tools = llm.bind_tools(tools)


# ---------------- STATE ----------------

class State(TypedDict):
    messages: Annotated[
        list[BaseMessage],
        add_messages
    ]


# ---------------- CHATBOT NODE ----------------

def chatbot(state: State):
    response = llm_with_tools.invoke(
        state["messages"]
    )

    return {
        "messages": [response]
    }


# ---------------- GRAPH ----------------

graph_builder = StateGraph(State)


graph_builder.add_node(
    "chatbot",
    chatbot
)


graph_builder.add_node(
    "tools",
    ToolNode(tools)
)


# ---------------- EDGES ----------------

graph_builder.add_edge(
    START,
    "chatbot"
)


graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition
)


graph_builder.add_edge(
    "tools",
    "chatbot"
)


# ---------------- COMPILE ----------------

graph = graph_builder.compile()