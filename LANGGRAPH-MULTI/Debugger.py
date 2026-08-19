from genai_shared.demo_tools import DEMO_TOOLS
from genai_shared.graphs import build_tool_calling_graph
from genai_shared.llms import groq_llm
from genai_shared.math_tools import add, subtract

llm = groq_llm()
tools = [add, subtract, *DEMO_TOOLS]
graph = build_tool_calling_graph(llm, tools)


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
