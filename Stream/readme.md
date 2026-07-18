# 🌊 LangChain Streaming (`.stream()`) & Python Generators

![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)
![LangChain](https://img.shields.io/badge/LangChain-Framework-green)
![LLM](https://img.shields.io/badge/LLM-Streaming-orange)

---

# 📖 Project Overview

This project explains how **LangChain's `.stream()`** works and why it is based on the concept of **Python Generators**.

Instead of waiting for the complete response, the LLM streams the answer **chunk by chunk**, creating a real-time typing experience similar to ChatGPT.

---

# 🏗 Overall Workflow

```mermaid
flowchart LR

A[User Prompt]
-->B[LangChain]

B-->C[LLM]

C-->D[Generate Chunk]

D-->E[Yield AIMessageChunk]

E-->F[Display Response]

F-->D
```

---

# 🖼 Without Streaming

```mermaid
flowchart LR

A[User]
-->B[invoke]

B-->C[LLM]

C-->D[Generate Complete Response]

D-->E[Display Answer]
```

Example

```python
response = llm.invoke("Explain AI")

print(response.content)
```

The user waits until the complete answer is generated.

---

# 🖼 With Streaming

```mermaid
flowchart LR

A[User]
-->B[stream]

B-->C[LLM]

C-->D[Generate Chunk]

D-->E[AIMessageChunk]

E-->F[Print Chunk]

F-->D
```

Example

```python
for chunk in llm.stream("Explain AI"):
    print(chunk.content, end="")
```

Output

```
Artificial Intelligence is the simulation of human intelligence...
```

The answer appears while the model is still generating.

---

# 🧠 Python Generator

A generator produces values **one at a time**.

```python
def numbers():

    yield 1
    yield 2
    yield 3
```

---

## Generator Workflow

```mermaid
flowchart TD

A[Generator Function]

A-->B[yield 1]

B-->C[Pause]

C-->D[yield 2]

D-->E[Pause]

E-->F[yield 3]
```

---

# Relationship Between Generator and Stream

Think of `stream()` as a generator.

Normal Generator

```python
def stream():

    yield "Artificial "

    yield "Intelligence "

    yield "is "

    yield "Amazing!"
```

LangChain internally behaves similarly.

---

## Comparison

| Generator | LangChain Stream |
|------------|------------------|
| yield 1 | yield AIMessageChunk |
| yield 2 | yield AIMessageChunk |
| yield 3 | yield AIMessageChunk |

---

# What Actually Happens?

```mermaid
sequenceDiagram

participant User

participant LangChain

participant LLM

User->>LangChain: Explain AI

LangChain->>LLM: Prompt

LLM-->>LangChain: Chunk 1

LangChain-->>User: Display

LLM-->>LangChain: Chunk 2

LangChain-->>User: Display

LLM-->>LangChain: Chunk 3

LangChain-->>User: Display
```

---

# `.invoke()` vs `.stream()`

| Feature | `.invoke()` | `.stream()` |
|----------|-------------|-------------|
| Returns | AIMessage | AIMessageChunk |
| Response | Complete | Incremental |
| Uses Generator | ❌ No | ✅ Yes |
| Best For | APIs | Chatbots |
| Real Time | ❌ | ✅ |

---

# Return Types

## invoke()

```python
response = llm.invoke("Hello")

print(type(response))
```

```
AIMessage
```

Access

```python
response.content
```

---

## stream()

```python
for chunk in llm.stream("Hello"):

    print(type(chunk))
```

```
AIMessageChunk
```

Access

```python
chunk.content
```

---

# Visual Comparison

```mermaid
flowchart LR

subgraph Invoke

A1[User]

A2[LLM]

A3[Complete Answer]

A1-->A2-->A3

end

subgraph Stream

B1[User]

B2[LLM]

B3[Chunk 1]

B4[Chunk 2]

B5[Chunk 3]

B1-->B2-->B3-->B4-->B5

end
```

---

# Why Streaming?

Without Streaming

```
⏳ Wait...
⏳ Wait...
⏳ Wait...
Complete Response
```

With Streaming

```
Artificial
Artificial Intelligence
Artificial Intelligence is
Artificial Intelligence is amazing...
```

---

# Real World Applications

- 🤖 ChatGPT
- 💬 AI Chatbots
- 📄 PDF Chatbots
- 📚 RAG Applications
- 🧠 AI Agents
- 👨‍💻 Coding Assistants
- 🎤 Voice Assistants

---

# Key Concepts Learned

- Python Generator
- yield
- next()
- Generator Object
- AIMessage
- AIMessageChunk
- invoke()
- stream()
- Real-Time Streaming
- LangChain

---

# Final Architecture

```mermaid
flowchart TB

User

↓

LangChain

↓

LLM

↓

Generator

↓

AIMessageChunk

↓

Display Response
```

---

# ⭐ Conclusion

`.stream()` is built on the same concept as **Python Generators**.

Instead of returning the entire response at once, it **yields AIMessageChunk objects one by one**, enabling real-time streaming just like ChatGPT.