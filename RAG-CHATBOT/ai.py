from genai_shared.llms import ollama_embeddings, ollama_llm
from genai_shared.chat import chat_loop
from genai_shared.rag import build_vector_store, format_docs, load_pdf_chunks

# LLM
llm = ollama_llm()

chunks = load_pdf_chunks("Vedant_Kapil_Resume.pdf")

# Embeddings
embeddings = ollama_embeddings()

# Vector Database
vectorstore = build_vector_store(chunks, embeddings, persist_directory="./chroma_db")

def respond(question):
    results = vectorstore.similarity_search(
        question,
        k=2
    )
    return format_docs(results, separator="\n")


chat_loop(
    respond,
    prompt="Ask: ",
    exit_words=frozenset({"bye"}),
    farewell="Thank you",
    answer_format="{answer}",
)