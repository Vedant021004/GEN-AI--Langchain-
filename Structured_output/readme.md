# 🎬 Structured Output with LangChain & Pydantic

This project demonstrates how to use **LangChain's Structured Output** feature with **Pydantic** models to force an LLM to return responses in a predefined schema instead of plain text.

---

# 📌 What is Structured Output?

Normally, Large Language Models (LLMs) return text responses.

Example:

```python
response = llm.invoke("Give me three movies released in 2002")
print(response.content)
```

Output:

```
Spider-Man (2002)
The Lord of the Rings: The Two Towers (2002)
Catch Me If You Can (2002)
```

Although this looks good, it is difficult to use directly in applications because it is unstructured text.

With **Structured Output**, the LLM returns a **Python object** that follows a schema defined using **Pydantic**.

Example Output:

```python
{
    "movies": [
        {
            "title": "Spider-Man",
            "year": 2002
        },
        {
            "title": "The Lord of the Rings: The Two Towers",
            "year": 2002
        },
        {
            "title": "Catch Me If You Can",
            "year": 2002
        }
    ]
}
```

This makes the output easy to process in APIs, databases, chatbots, and AI applications.

---

# 📦 Imports Used

```python
from typing import List
from pydantic import BaseModel, Field
```

---

## 1️⃣ BaseModel

`BaseModel` is the parent class provided by **Pydantic**.

Every schema must inherit from it.

Example:

```python
class Movie(BaseModel):
    title: str
    year: int
```

### Why BaseModel?

It provides:

- Data Validation
- Type Checking
- JSON Serialization
- model_dump()
- model_validate()
- Error Handling

Without `BaseModel`, Pydantic cannot validate your data.

---

## 2️⃣ Field()

`Field()` adds metadata to each attribute.

Example:

```python
title: str = Field(description="Movie Title")
```

It helps the LLM understand what information is expected.

Example:

```python
year: int = Field(description="Release Year")
```

Benefits:

- Better structured output
- Documentation
- Validation
- More accurate responses

---

## 3️⃣ List

Imported from

```python
from typing import List
```

It specifies that a variable contains multiple objects.

Example:

```python
movies: List[Movie]
```

Meaning:

```
Movies
│
├── Movie
├── Movie
└── Movie
```

---

# 📖 Understanding the Models

## Movie Model

```python
class Movie(BaseModel):
    title: str
    year: int
```

Represents one movie.

Example:

```python
Movie(
    title="Spider-Man",
    year=2002
)
```

---

## Movies Model

```python
class Movies(BaseModel):
    movies: List[Movie]
```

Represents multiple movies.

Example:

```python
Movies(
    movies=[
        Movie(title="Spider-Man", year=2002),
        Movie(title="Catch Me If You Can", year=2002)
    ]
)
```

---

# 🧠 Inheritance vs Composition

Many beginners confuse these concepts.

## Inheritance

```python
class Movie(BaseModel):
```

Movie inherits from BaseModel.

Diagram:

```
BaseModel
     ▲
     │
   Movie
```

Movie receives all functionality of BaseModel.

Examples:

- Validation
- model_dump()
- JSON conversion

---

## Composition

```python
movies: List[Movie]
```

This is **NOT inheritance**.

It means:

```
Movies
    │
    ▼
List of Movie objects
```

Movies **contains** Movie objects.

Relationship:

```
Movies
   has many
      │
      ▼
   Movie
```

This is called **Composition (Has-A Relationship)**.

---

# 🚀 Creating Structured Output

```python
structured = llm.with_structured_output(Movies)
```

Instead of returning an `AIMessage`, LangChain now returns a `Movies` object.

---

# 🔍 Invoking the LLM

```python
response = structured.invoke(
    "Give me three movies released in 2002"
)
```

The LLM generates output matching the schema.

---

# ❌ Why .content Doesn't Work

Normally:

```python
response = llm.invoke(...)
```

returns

```
AIMessage
```

Use

```python
response.content
```

---

With Structured Output

```python
structured = llm.with_structured_output(Movies)
```

returns

```
Movies (Pydantic Object)
```

There is no `.content`.

Instead use:

```python
response.model_dump()
```

or

```python
response.movies
```

---

# 📤 model_dump()

Converts the Pydantic object into a Python dictionary.

Example:

```python
print(response.model_dump())
```

Output:

```python
{
    "movies": [
        {
            "title": "Spider-Man",
            "year": 2002
        }
    ]
}
```

---

# 🏗 Complete Workflow

```
User Prompt
      │
      ▼
LangChain
      │
      ▼
LLM
      │
      ▼
Structured Output
      │
      ▼
Pydantic Model
      │
      ▼
Python Object
      │
      ▼
Dictionary (model_dump())
```

---

# 📚 Technologies Used

- Python
- LangChain
- Pydantic
- LLM (OpenAI / Ollama / Gemini)
- Structured Output

---

# 🎯 Learning Outcomes

By completing this project, you will understand:

- Structured Output
- Pydantic Models
- BaseModel
- Field()
- Type Annotations
- List
- Inheritance
- Composition
- model_dump()
- LangChain Structured Output
- LLM Response Validation

---

# 🚀 Future Improvements

- Add Nested Models
- JSON Schema Validation
- FastAPI Integration
- LangGraph Support
- ChromaDB Integration
- RAG-based Structured Responses

---

## ⭐ Example Use Cases

- AI Chatbots
- Resume Parser
- Invoice Extraction
- Medical Report Analysis
- Movie Recommendation Systems
- Document Understanding
- AI Agents
- RAG Applications
