
from pydantic import BaseModel, Field
from typing import Annotated

from langchain_core.messages import AnyMessage, HumanMessage
from langchain_core.tools import tool
from langchain_groq import ChatGroq

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition


# -------------------------
# 1. LLM
# -------------------------

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0
)


# -------------------------
# 2. AGENT STATE
# -------------------------

class AgentState(BaseModel):

    messages: Annotated[
        list[AnyMessage],
        add_messages
    ] = Field(default_factory=list)

    question: str = ""

    answer: str = ""

    tool_used: list[str] = Field(default_factory=list)


# -------------------------
# 3. TOOLS
# -------------------------

@tool
def add(a: float, b: float):
    """Add two numbers."""
    return a + b


@tool
def subtract(a: float, b: float):
    """Subtract second number from first number."""
    return a - b


@tool
def multiply(a: float, b: float):
    """Multiply two numbers."""
    return a * b


@tool
def divide(a: float, b: float):
    """Divide first number by second number."""

    if b == 0:
        return "Cannot divide by zero"

    return a / b


tools = [add, subtract, multiply, divide]


# -------------------------
# 4. BIND TOOLS
# -------------------------

llm_with_tools = llm.bind_tools(tools)


# -------------------------
# 5. TOOL NODE
# -------------------------

tool_node = ToolNode(tools)


# -------------------------
# 6. ASSISTANT NODE
# -------------------------

def assistant(state: AgentState):

    response = llm_with_tools.invoke(state.messages)

    return {
        "messages": [response]
    }


# -------------------------
# 7. BUILD GRAPH
# -------------------------

builder = StateGraph(AgentState)

builder.add_node("assistant", assistant)

builder.add_node("tools", tool_node)


# -------------------------
# 8. ADD EDGES
# -------------------------

builder.add_edge(START, "assistant")

builder.add_conditional_edges(
    "assistant",
    tools_condition
)

builder.add_edge("tools", "assistant")


# -------------------------
# 9. COMPILE GRAPH
# -------------------------

graph = builder.compile()


# -------------------------
# 10. RUN AGENT
# -------------------------

def run_agent(question: str):

    response = graph.invoke({
        "messages": [
            HumanMessage(content=question)
        ],
        "question": question
    })

    final_answer = response["messages"][-1].content

    return final_answer


# -------------------------
# 11. CHAT LOOP
# -------------------------

if __name__ == "__main__":

    print("AI Math Agent Started!")
    print("Type 'exit' to stop.")

    while True:

        question = input("\nYou: ")

        if question.lower() in ["exit", "quit"]:
            print("Agent stopped.")
            break

        try:
            answer = run_agent(question)

            print("\nAgent:", answer)

        except Exception as e:
            print("\nError:", e)
