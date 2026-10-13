from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START,END
from pydantic import BaseModel
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph.message import add_messages
from typing import Annotated


load_dotenv()

memory = InMemorySaver()

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    
)

class State(BaseModel):
    messages: Annotated[list, add_messages]


# node

def chatbot(state: State):

    # Send messages to AI
    response = llm.invoke(state.messages)

    # Store AI response
    return {
        "messages": [response]
    }


graph = StateGraph(State)

graph.add_node("chatbot", chatbot)

graph.add_edge(START, "chatbot")
graph.add_edge("chatbot", END)

app = graph.compile()


user_input = input("You: ")

result = app.invoke({
    "messages": [user_input]
})


print("AI:", result["messages"][0].content)
print("AI:", result["messages"][-1].content)
print("AI:", result["messages"][1].content)