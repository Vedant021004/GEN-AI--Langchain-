"""Shared PDF loading, splitting, embedding, and formatting helpers."""

from __future__ import annotations

from typing import Any

from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


def load_pdf_chunks(
    file_path: str,
    chunk_size: int = 500,
    chunk_overlap: int = 100,
) -> list[Document]:
    """Load a PDF and split it into document chunks."""
    documents = PyPDFLoader(file_path).load()
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    return splitter.split_documents(documents)


def build_vector_store(
    chunks: list[Document],
    embedding: Any,
    persist_directory: str | None = None,
    collection_name: str | None = None,
) -> Chroma:
    """Create a Chroma store, passing only explicitly configured options."""
    kwargs = {"documents": chunks, "embedding": embedding}
    if persist_directory is not None:
        kwargs["persist_directory"] = persist_directory
    if collection_name is not None:
        kwargs["collection_name"] = collection_name
    return Chroma.from_documents(**kwargs)


def format_docs(docs: list[Document], separator: str = "\n\n") -> str:
    """Join document page contents into a context string."""
    return separator.join(doc.page_content for doc in docs)
