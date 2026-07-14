from dotenv import load_dotenv
import os

load_dotenv()
from langchain_ollama import ChatOllama

llm = ChatOllama(model="llama3.2")

system_prompt = input("Enter system prompt: ")
user_prompt = input("Enter your question: ")

prompts = [
    ("system", system_prompt),
    ("human", user_prompt)
]

res = llm.invoke(prompts)
print(res.content)
