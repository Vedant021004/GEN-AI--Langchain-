from langchain_ollama import ChatOllama

llm = ChatOllama(
    model = "llama3.2",
    streaming = True
)

res = llm.stream("my name is vedant kapil and please introduce me in front of a interviewer")

print(res)

for chunk in res:
    print(chunk.content, end = "")