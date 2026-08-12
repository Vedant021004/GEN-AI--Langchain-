from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END
from pydantic import BaseModel
from langgraph.graph.message import add_messages
from typing import Annotated




load_dotenv()

llm = ChatGroq(
    model="openai/gpt-oss-20b"
)

class State(BaseModel):
    messages: Annotated[list, add_messages]


# NODE -->1

def chatbot(state: State):
    return {
        "messages": [
            llm.invoke(state.messages)
        ]
    }

# NODE -->2

def node_2(state: State):
    response = state.messages[-1].content

    modified_response = response.upper()

    return {
        "messages": [
            {"role": "assistant", "content": modified_response}
        ]
    }


graph_builder = StateGraph(State)

graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("node_2", node_2) 

graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", "node_2")
graph_builder.add_edge("node_2",END)

graph = graph_builder.compile()

result = graph.invoke({"messages": [{"role": "user","content": "Hi"}]})



print(result["messages"][-1].content)