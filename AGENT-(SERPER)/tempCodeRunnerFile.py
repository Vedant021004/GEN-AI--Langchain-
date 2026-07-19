from dotenv import load_dotenv

load_dotenv()

from langchain_ollama import ChatOllama
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain.agents import create_agent
from langgraph.checkpoint.memory import MemorySaver

llm = ChatOllama(model = "llama3.2")
search = GoogleSerperAPIWrapper()


res = search.run("what is top 10 news of today\n")
print(res)
