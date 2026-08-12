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



while True:

    question = input("ASK: ")
    if question.lower() in [ "bye", "done", "exit"]:
        break
    res = graph.invoke({
            "messages": 
                    
                [{"role": "user",
                "content": question}]
            
                },
                config = {"configurable":{"thread_id": "1"}}
                )

    result = res["messages"][-1].content

    print(result)