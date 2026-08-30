from langchain_groq import ChatGroq
from llama_cloud import LlamaCloud
from langchain_core.documents import Document
from langchain_experimental.text_splitter import SemanticChunker
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain.agents import create_agent
from langgraph.checkpoint.memory import MemorySaver
from pathlib import Path
import os
from dotenv import load_dotenv
load_dotenv()

llm = ChatGroq(model="openai/gpt-oss-20b")
memory = MemorySaver()
agent = create_agent(
    model=llm,
    checkpointer=memory
)

path = input("Enter the path of file: ")

client = LlamaCloud(
    api_key=os.getenv("LLAMA_CLOUD_API_KEY"),
    timeout=120.0)

file = client.files.create(
    file=Path(path),
    purpose="parse")

result = client.parsing.create(
    tier="agentic",
    version="latest",
    file_id=file.id)

parsed = client.parsing.get(
    result.id,
    expand="markdown" )

documents = [
    Document(
        page_content=doc.markdown)
    for doc in parsed.markdown.pages]




embedding = OllamaEmbeddings(model="nomic-embed-text:latest")
splitter = SemanticChunker(embeddings=embedding)

chunks = splitter.split_documents(documents)

vdb = Chroma.from_documents(
    documents=chunks,
    embedding= embedding,
    persist_directory="./advncrag_db"
)

while True:
    query = input("\nYou: ")
    if query.lower() in ["exit", "quit", "terminate"]:
        print("Terminating conversation.. Thank you")
        break

    response = vdb.similarity_search(
        query= query,
        k=5
    )
    context = "\n\n".join(
            doc.page_content
            for doc in response)
                
    prompt = f"""
    You are a helpful  assistant.
    You answer questions about the uploaded document.
    Use the document context below when it is relevant.
    
    Document context:
    {context}
    
    Current question:
    {query}
    
    Rules:
    1. If the answer is available in the document context, answer using the document.
    2. If the exact answer is NOT available in the document, but the question
    is related to the same topic, you may answer using your general knowledge.
    3. If the question is completely unrelated to the document/topic, say:
    
    "I could not find this information."
    
    Give simple and clear answers suitable for the person."""

    result = agent.invoke({
            "messages":[{"role":"user","content":prompt}]
    }, config={"configurable":{"thread_id":"1"}})

    print("Assistant: ", result['messages'][-1].content)
    
    