from langchain_tavily import TavilySearch
from genai_shared.graphs import build_tool_calling_graph, save_graph_png
from genai_shared.llms import groq_llm
from genai_shared.math_tools import multiply

llm = groq_llm()

tool = TavilySearch(max_results =2)
res = tool.invoke("what is the news about the jharkhand today why there is too much caos")
print(res["results"][0]["content"])

tools=[tool,multiply]
graph = build_tool_calling_graph(llm, tools, node_name="tool_calling_llm")

response=graph.invoke({"messages":"What is the recent ai news, and what is 345 multiply by 67"})

for m in response['messages']:
    m.pretty_print()


save_graph_png(graph, "graphh.png")

print("Graph saved as graph.png")