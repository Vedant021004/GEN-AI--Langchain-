from genai_shared.llms import ollama_embeddings, ollama_llm
from genai_shared.rag import build_vector_store, load_pdf_chunks

# LLM
llm = ollama_llm()

chunks = load_pdf_chunks("Vedant_Kapil_Resume.pdf")

# Embeddings
embeddings = ollama_embeddings()

# Vector Database
vectorstore = build_vector_store(chunks, embeddings, persist_directory="./chroma_db")

while True:

    question = input("Ask: ")

    if question.lower() == "bye":
        print("Thank you")
        break

    results = vectorstore.similarity_search(
        question,
        k=2
    )

    for doc in results:
        print(doc.page_content)