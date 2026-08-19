from langchain.agents import create_agent
from langchain.tools import tool
from genai_shared.llms import groq_llm, hf_embeddings
from genai_shared.rag import build_vector_store, format_docs, load_pdf_chunks


# model
llm = groq_llm()

embedding_model = hf_embeddings()

vector_store = None

# Tool 1 : Load PDF to Store into Vector DB

@tool
def load_pdf(file_path: str) -> str:
    """
    Load a PDF and store it into ChromaDB.
    """

    global vector_store

    chunks = load_pdf_chunks(file_path)
    vector_store = build_vector_store(
        chunks,
        embedding_model,
        persist_directory="./hf_vector_db",
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

    return format_docs(docs)

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