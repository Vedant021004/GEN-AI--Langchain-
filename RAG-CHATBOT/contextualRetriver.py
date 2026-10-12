from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_classic.retrievers import ContextualCompressionRetriever
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_classic.retrievers.document_compressors import LLMChainExtractor
from langchain_groq import ChatGroq

load_dotenv()

docs = [
    Document(
        page_content="Apples are red in colour. Mangoes are yellow in colour. Harry potter's First movie was THE SORCERER'S STONE. Lychee are pink in colour"
    ),
    Document(
        page_content="Green vegetables are nutricious and we must eat it. Harry Potter second movie was CHAMBER OF SECRETS."
    ),
    Document(page_content="Harry potter last movie was DEATHLY HALLOWS PARRT 2"),
    Document(page_content="Emma Watson played role of Hermioner Granger in Harry potter movies."),
    Document(page_content="I love MANGOESS. Harry POtter also likes mangoes"),
]

embedding = OllamaEmbeddings(model="nomic-embed-text")

vdb = Chroma.from_documents(
    embedding=embedding,
    documents=docs,
    persist_directory="contextualRetriever_db",
)

llm = ChatGroq(model="openai/gpt-oss-20b")

retriever = vdb.as_retriever(search_kwargs={"k": 5})
compressor = LLMChainExtractor.from_llm(llm)

contextual_retriever = ContextualCompressionRetriever(
    base_retriever=retriever,
    base_compressor=compressor,
)

result = contextual_retriever.invoke("Tell me about harry potter")

for doc in result:
    print(doc.page_content)
