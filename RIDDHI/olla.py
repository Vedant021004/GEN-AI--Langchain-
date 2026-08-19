from genai_shared.llms import ollama_llm

llm = ollama_llm(model="llama3.2:latest")

while True:
    user = input("please ask your queston..")

    data = llm.invoke(user)

    print(data.content)
