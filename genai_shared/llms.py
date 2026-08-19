"""Factories for the language models and embedding models used by the scripts."""

from __future__ import annotations

from typing import Any

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import ChatOllama, OllamaEmbeddings

load_dotenv()


def groq_llm(model: str = "openai/gpt-oss-20b", **kwargs: Any) -> ChatGroq:
    """Create a Groq chat model."""
    return ChatGroq(model=model, **kwargs)


def ollama_llm(model: str = "llama3.2", **kwargs: Any) -> ChatOllama:
    """Create an Ollama chat model."""
    return ChatOllama(model=model, **kwargs)


def ollama_embeddings(model: str = "nomic-embed-text") -> OllamaEmbeddings:
    """Create Ollama embeddings."""
    return OllamaEmbeddings(model=model)


def hf_embeddings(
    model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
) -> HuggingFaceEmbeddings:
    """Create Hugging Face embeddings."""
    return HuggingFaceEmbeddings(model_name=model_name)
