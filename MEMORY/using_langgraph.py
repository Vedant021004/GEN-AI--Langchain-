from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from langgraph.checkpoint.memory import MemorySaver


llm = ChatOllama(
    model="llama3.2"
)

memory = MemorySaver()

agent = create_agent(
    model=llm,
    checkpointer=memory
)

config = {
    "configurable": {"thread_id": "1"}
}

while True:

    user = input("Ask: ")

    if user.lower() == "bye":
        break

    res = agent.invoke(
        {"messages": [{"role": "user", "content": user}]},
        config=config
    )

    print("AI:", res["messages"][-1].content)