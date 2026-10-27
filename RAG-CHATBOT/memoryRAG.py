from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from langgraph.checkpoint.memory import MemorySaver
from langchain.agents import create_agent
from dotenv import load_dotenv

load_dotenv()


llm = ChatGroq(
    model="openai/gpt-oss-20b"
)

memory = MemorySaver()

agent = create_agent(
    model=llm,
    checkpointer=memory
)


# PDF
doc = PyPDFLoader("carteye.pdf")
data = doc.load()


# Chunking
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

chunk = splitter.split_documents(data)

print("Number of chunks:", len(chunk))


# Embeddings
embedding = OllamaEmbeddings(
    model="nomic-embed-text:latest"
)

print("Testing embedding...")

test = embedding.embed_query("Hello")

print("Embedding created:", len(test))


# Chroma
vdb = Chroma.from_documents(
    documents=chunk,
    embedding=embedding,
    persist_directory="./rv_db"
)


# Questions
while True:

    query = input("Ask: ")

    if query.lower() in ["exit", "terminate"]:

        print("Terminating... Thank youuu")
        break


    result = vdb.similarity_search(
        query=query,
        k=3
    )


    context = "\n\n".join(
        doc.page_content
        for doc in result
    )


    prompt = f"""
You are an assistant that answers questions about the PDF.

Use the PDF context below to answer questions about the book.

PDF context:

{context}

Current question:

{query}

You can also use previous conversation messages when the user asks about
something discussed earlier in this conversation.

If the answer is not available in the PDF and it was not discussed earlier,
say:

"I could not find this information."
"""


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
                "thread_id": "1"
            }
        }
    )


    print("\nAnswer:")
    print(response["messages"][-1].content)
    print()
