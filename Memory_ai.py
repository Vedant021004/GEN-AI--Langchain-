from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="llama3.2"
)

history = []

while True:

    query = input("User: ")

    if query.lower() in ["bye", "done", "exit"]:
        print("Tata bhai ji")
        break

    history.append({
        "role": "user",
        "content": query
    })

    response = llm.invoke(history)

    print("AI:", response.content)

    history.append({
        "role": "assistant",
        "content": response.content
    })