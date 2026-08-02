from langchain.agents import create_agent
from langchain.tools import tool
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_chroma import Chroma

# Global Objects

llm = ChatOllama(
    model="llama3.2:latest"
)

embedding_model = OllamaEmbeddings(
    model="nomic-embed-text"
)

vector_store = None

# Tool 1 : Load PDF to Store into Vector DB

@tool
def load_pdf(file_path: str) -> str:
    """
    Load a PDF and store it into ChromaDB.
    """

    global vector_store

    loader = PyPDFLoader(file_path)

    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    chunks = splitter.split_documents(documents)

    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory="./vector_db"
    )

    return f"Successfully stored {len(chunks)} chunks."

# Tool 2 : Retrieve Context

@tool
def retrieve_context(question: str) -> str:
    """
    Search the uploaded PDF and return the relevant context.
    """

    global vector_store

    if vector_store is None:
        return "No PDF has been uploaded."

    docs = vector_store.similarity_search(
        question,
        k=3
    )

    context = "\n\n".join(
        doc.page_content
        for doc in docs
    )

    return context

# Create Agent

agent = create_agent(
    model=llm,
    tools=[
        load_pdf,
        retrieve_context
    ],
    system_prompt="""
You are an AI PDF Assistant.

Rules:

1. If the user asks anything about the uploaded PDF,
   ALWAYS call retrieve_context.

2. Never make up information.

3. If the answer is not found in the retrieved context,
   reply:
   'I couldn't find that information in the uploaded PDF.'

4. Be concise.
"""
)

# Upload PDF

pdf_path = ("Vedant_Kapil_Resume.pdf")

print(
    load_pdf.invoke(
        {
            "file_path": pdf_path
        }
    )
)

# Chat

while True:

    prompt = input("\nYou : ")

    if prompt.lower() in ["exit", "quit"]:
        break

    response = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        },
        config={
            "configurable": {
                "thread_id": 1
            }
        }
    )