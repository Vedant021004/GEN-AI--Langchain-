from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_core.documents import Document
from langchain_classic.retrievers import MultiQueryRetriever
from langchain_groq import ChatGroq

load_dotenv()

docs = [
    Document(
        page_content="Regular walking boosts heart health and can reduce symptoms of depression.",
        metadata={"source": "H1"},
    ),
    Document(
        page_content="Consuming leafy greens and fruits helps detox the body and improve longevity.",
        metadata={"source": "H2"},
    ),
    Document(
        page_content="Deep sleep is crucial for cellular repair and emotional regulation.",
        metadata={"source": "H3"},
    ),
    Document(
        page_content="Mindfulness and controlled breathing lower cortisol and improve mental clarity.",
        metadata={"source": "H4"},
    ),
    Document(
        page_content="Drinking sufficient water throughout the day helps maintain metabolism and energy.",
        metadata={"source": "H5"},
    ),
    Document(
        page_content="Python balances readability with power, making it a popular system design language.",
        metadata={"source": "I2"},
    ),
    Document(
        page_content="Photosynthesis enables plants to produce energy by converting sunlight.",
        metadata={"source": "I3"},
    ),
    Document(
        page_content="The 2022 FIFA world Cup was held in Qatar and drew global energy and excitement.",
        metadata={"source": "I4"},
    ),
    Document(
        page_content="Black holes bend spacetime and store immense gravitational energy.",
        metadata={"source": "I5"},
    ),
]

embedding = OllamaEmbeddings(model="nomic-embed-text")

vdb = Chroma.from_documents(
    documents=docs,
    embedding=embedding,
    persist_directory="mqr_db",
)

print("Similarity search results:")
similarity_search = vdb.similarity_search(
    query="how to maintain balance and energy",
    k=5,
)
for answer in similarity_search:
    print(answer.page_content)

retriever = vdb.as_retriever(search_kwargs={"k": 2})

multi_query_retriever = MultiQueryRetriever.from_llm(
    retriever=retriever,
    llm=ChatGroq(model="openai/gpt-oss-120b"),
)

result = multi_query_retriever.invoke(
    "how to improve balance and eneergy level in human"
)

print("\nMulti-query retriever results:")
for answer in result:
    print(answer.page_content)
