from dotenv import load_dotenv
from langchain_groq import ChatGroq

from langgraph.graph import (
    StateGraph,
    START,
    END
)

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph.message import add_messages

from typing import Annotated
from typing_extensions import TypedDict

from langgraph.prebuilt import ToolNode, tools_condition

from langchain_core.tools import tool
from langchain_core.messages import BaseMessage


load_dotenv()


memory = InMemorySaver()


llm = ChatGroq(
    model="openai/gpt-oss-20b",
)


#             TOOLS 

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


#            BIND TOOLS 

tools = [
    add,
    subtract,
    search,
    get_weather
]

llm_with_tools = llm.bind_tools(tools)


#                  STATE 

class State(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


#                LLM NODE  

def chatbot(state: State):
    return {
        "messages": [
            llm_with_tools.invoke(state["messages"])
        ]
    }


#                 GRAPH  

graph_builder = StateGraph(State)

graph_builder.add_node("chatbot", chatbot)

graph_builder.add_node(
    "tools",
    ToolNode(tools)
)


#                  Edge

graph_builder.add_edge(START, "chatbot")

graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition
)

graph_builder.add_edge("tools", "chatbot")


#                 Compile

graph = graph_builder.compile()


result = graph.invoke({
    "messages": [
        {
            "role": "user",
            "content": """
            "who is 40+3+5-6-7-8-9*3+4.
            """
        }
    ]
})

for message in result["messages"]:
    print("\n---")
    print(message)


