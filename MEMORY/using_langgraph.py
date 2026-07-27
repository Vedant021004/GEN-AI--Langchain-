from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from langgraph.checkpoint.memory import MemorySaver

llm = ChatOllama(
    model="llama3.2"
)

agent = create_agent(
    model = llm,
    checkpointer= MemorySaver()


)


res = llm.invoke("hello")

print(res.content)