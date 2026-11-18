from pydantic import BaseModel, Field
from typing import Annotated

from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages

from langgraph.prebuilt import InjectedState
from langchain_core.tools import tool

from langgraph.types import Command




class AgentState(BaseModel):

    messages: Annotated[
        list[AnyMessage],
        add_messages
    ] = Field(default_factory=list)

    question: str = ""

    answer: str = ""

    tool_used: list[str] = Field(default_factory=list)


@tool
def add(
    a: float,
    b: float,
    state: Annotated[dict, InjectedState]
):
    """This tool is used to add two numbers."""

    result = a + b

    question = state["question"]

    return {
        "result": result,
        "original_question": question
    }