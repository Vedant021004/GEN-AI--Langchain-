from genai_shared.chat import chat_loop, history_responder
from genai_shared.llms import ollama_llm

llm = ollama_llm()
respond = history_responder(llm)
chat_loop(
    respond,
    prompt="User: ",
    exit_words=frozenset({"bye", "done", "exit"}),
    farewell="Tata bhai ji",
)
print(respond.history)