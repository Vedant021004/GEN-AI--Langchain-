from langgraph.graph import StateGraph, START,END
from pydantic import BaseModel
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph.message import add_messages
from typing import Annotated
from genai_shared.chat import agent_responder, chat_loop
from genai_shared.llms import groq_llm

memory = InMemorySaver()

llm = groq_llm()

class Chatstate(BaseModel):
    messages:Annotated[list,add_messages]


# Node

def chatbotNode(state:Chatstate):
    res = llm.invoke(state.messages)  
    state.messages = [res]
    return state

# Graph

graph = StateGraph(Chatstate)
graph.add_node("chatbot", chatbotNode)

# Edge
graph.add_edge(START, "chatbot")
graph.add_edge("chatbot", END)

graph = graph.compile(checkpointer=memory)



chat_loop(
    agent_responder(graph),
    prompt="ASK: ",
    exit_words=frozenset({"bye", "done", "exit"}),
    answer_format="{answer}",
)