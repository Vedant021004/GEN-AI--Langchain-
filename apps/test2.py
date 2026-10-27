from langchain_ollama import ChatOllama


model = ChatOllama(
    model="llama3.2"
)

response = model.invoke("hi my anem is vedant kapil")

print(response.content)