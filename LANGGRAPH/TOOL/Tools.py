from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END
from pydantic import BaseModel
from langgraph.graph.message import add_messages
from typing import Annotated
from langchain_tavily import TavilySearch
from langgraph.prebuilt import ToolNode
from langgraph.prebuilt import tools_condition


load_dotenv()

llm = ChatGroq(
    model="openai/gpt-oss-20b"
)

tool = TavilySearch(max_results =2)
res = tool.invoke("what is the news about the jharkhand today why there is too much caos")
print(res["results"][0]["content"])

class State(BaseModel):
    messages: Annotated[list, add_messages]

## Custom function
def multiply(a:int,b:int)->int:
    """Multiply a and b

    Args:
        a (int): first int
        b (int): second int

    Returns:
        int: output int
    """
    return a*b

tools=[tool,multiply]
llm_with_tool=llm.bind_tools(tools)    


#state

def tool_calling_llm(state:State):
    return {"messages":[llm_with_tool.invoke(state.messages)]}

## Graph
builder=StateGraph(State)
builder.add_node("tool_calling_llm",tool_calling_llm)
builder.add_node("tools",ToolNode(tools))

## Add Edges
builder.add_edge(START, "tool_calling_llm")
builder.add_conditional_edges(
    "tool_calling_llm",
    # If the latest message (result) from assistant is a tool call -> tools_condition routes to tools
    # If the latest message (result) from assistant is a not a tool call -> tools_condition routes to END
    tools_condition
)
builder.add_edge("tools","tool_calling_llm")

## compile the graph
graph=builder.compile()

response=graph.invoke({"messages":"What is the recent ai news, and what is 345 multiply by 67"})

for m in response['messages']:
    m.pretty_print()


# png = graph.get_graph().draw_mermaid_png()

# with open("graph.png", "wb") as f:
#     f.write(png)

# print("Graph saved as graph.png")