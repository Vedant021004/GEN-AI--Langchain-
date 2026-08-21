from dotenv import load_dotenv
load_dotenv()

from langchain_groq import ChatGroq


llm = ChatGroq(
    model="openai/gpt-oss-20b"
)

response = llm.invoke("What is force")

print(response.content)
