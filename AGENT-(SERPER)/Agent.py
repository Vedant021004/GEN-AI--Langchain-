from dotenv import load_dotenv

load_dotenv()

from langchain_community.tools import GoogleSerperRun



from langchain_ollama import ChatOllama
from langchain.agents import create_agent
# from langgraph.checkpoint.memory import MemorySaver
# from langchain_community.utilities import GoogleSerperAPIWrapper 


llm = ChatOllama(model = "llama3.2")
search = GoogleSerperRun()

# res = search.run("what is top 10 news of today")
# print(res)

agent = create_agent(
    model = llm,
    tools = [search],
    system_prompt="You are a agent and can search for any question on google."
)

while True:
    question = input("ASK:  ")
    if question.lower() in "done":
        break
    response = agent.invoke(
            {"messages":[{"role":"user", "content":question}]},
            
        )

    print(response["messages"][-1].content)
