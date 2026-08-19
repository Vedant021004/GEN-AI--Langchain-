from langchain_ollama import ChatOllama

llm = ChatOllama(
    model = "llama3.2:latest"
)

while True:
    user = input("please ask your queston..")

    data = llm.invoke(user)

    print(data.content)
