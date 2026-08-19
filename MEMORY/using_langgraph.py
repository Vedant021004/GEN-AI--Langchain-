from langchain.agents import create_agent
from langgraph.checkpoint.memory import MemorySaver
from genai_shared.chat import agent_responder, chat_loop
from genai_shared.llms import ollama_llm

llm = ollama_llm()

memory = MemorySaver()

agent = create_agent(
    model=llm,
    checkpointer=memory
)

chat_loop(
    agent_responder(agent),
    prompt="Ask: ",
    exit_words=frozenset({"bye"}),
)