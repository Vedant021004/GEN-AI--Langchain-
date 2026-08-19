from langchain_community.tools import GoogleSerperRun
from langchain.agents import create_agent
from langgraph.checkpoint.memory import MemorySaver
from genai_shared.chat import DEFAULT_EXIT_WORDS, agent_responder, chat_loop
from genai_shared.llms import ollama_llm

llm = ollama_llm()
search = GoogleSerperRun()

# res = search.run("what is top 10 news of today")
# print(res)

agent = create_agent(
    model = llm,
    tools = [search],
    system_prompt = """
    You are a helpful AI assistant.

    Rules:
    - Answer in 1-3 sentences.
    - Be concise.
    - Do not add unnecessary explanations.
    - If the user asks for a simple answer, give only the direct answer.
    """,
    checkpointer = MemorySaver()
)

chat_loop(
    agent_responder(agent),
    prompt="ASK:  ",
    exit_words=DEFAULT_EXIT_WORDS,
)
