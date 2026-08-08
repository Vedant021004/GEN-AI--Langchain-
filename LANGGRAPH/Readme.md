# 🤖 Basic AI Chatbot using LangGraph & LangChain

A beginner-friendly chatbot built using **LangGraph**, **LangChain**, and **Groq LLM**. This project demonstrates how to create a stateful conversational AI using graph-based workflows instead of a simple sequential pipeline.

---

# 📖 Project Overview

This project teaches the fundamentals of **LangGraph** by building a conversational chatbot.

Instead of directly calling an LLM, the chatbot is designed as a **graph** where each node performs a specific task and shares a common state throughout the workflow.

The current workflow is intentionally simple:

```

START
│
▼
Chatbot Node
│
▼
END

```

As the project grows, additional nodes such as Retrieval (RAG), SQL Agents, Web Search, Memory, Human Approval, and Multi-Agent Systems can be added without changing the overall architecture.

---

# 🚀 Features

- Conversational AI using Groq LLM
- Graph-based workflow using LangGraph
- Stateful conversations
- Memory using `InMemorySaver`
- Automatic message history management
- Thread-based conversation tracking
- Beginner-friendly project structure

---

# 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| Python | Programming Language |
| LangChain | LLM Integration |
| LangGraph | Workflow Orchestration |
| Groq | Language Model Provider |
| Pydantic | State Validation |
| dotenv | Environment Variables |

---

# 📂 Project Structure

```

project/
│
├── model.py
├── .env
├── requirements.txt
└── README.md

```

---

# 🧠 Core Concepts

## 1. Large Language Model

```

ChatGroq

```

Responsible for generating AI responses.

```

User Message
│
▼
ChatGroq
│
▼
AI Response

```

---

## 2. State

The chatbot stores its conversation inside a state object.

```python
class ChatState(BaseModel):
    messages: Annotated[list, add_messages]
```

Current State

```

ChatState
│
└── messages
├── Human Message
├── AI Message
└── ...

```

Every node receives this state.

---

## 3. Node

A node is simply a Python function.

```python
def chatbotNode(state: ChatState):
```

Its responsibility is:

- Read the current state
- Call the LLM
- Return updated state

Workflow

```

Current State
│
▼
Node
│
▼
Updated State

```

---

## 4. Graph

The graph connects all nodes.

```

START
│
▼
chatbotNode
│
▼
END

```

Future graphs may look like:

```

START
│
▼
Classify Question
├─────────────┐
│             │
▼             ▼
SQL Node   RAG Node
│             │
└──────┬──────┘
▼
LLM
│
▼
Memory
│
▼
END

```

---

## 5. Memory

```

InMemorySaver()

```

Stores conversation history.

Without Memory

```

User: Hi

AI: Hello

User: Who am I?

↓

AI: I don't know.

```

With Memory

```

User: My name is Vedant

↓

User: Who am I?

↓

AI: Your name is Vedant.

```

---

## 6. Thread ID

Each conversation has its own ID.

```python
config={
    "configurable":{
        "thread_id":"1"
    }
}
```

```

Thread 1
Conversation A

Thread 2
Conversation B

```

Each thread maintains independent memory.

---

# ⚙️ Workflow

```

User
│
▼
Input Question
│
▼
Create Initial State
│
▼
graph.invoke()
│
▼
START
│
▼
chatbotNode
│
▼
llm.invoke(messages)
│
▼
AI Response
│
▼
Updated State
│
▼
END
│
▼
Display Answer

```

---

# 🔄 Request Flow

```

User

│

▼

"What is LangGraph?"

│

▼

ChatState

│

▼

messages

│

▼

chatbotNode()

│

▼

ChatGroq

│

▼

AIMessage

│

▼

Return Updated State

│

▼

Graph Ends

│

▼

Print Response

```

---

# ▶️ Running the Project

### Clone Repository

```bash
git clone <repository-url>
cd <repository-name>
```

---

### Create Virtual Environment

```bash
python -m venv env
```

Windows

```bash
env\Scripts\activate
```

Linux / macOS

```bash
source env/bin/activate
```

---

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

### Create `.env`

```
GROQ_API_KEY=your_api_key_here
```

---

### Run

```bash
python model.py
```

---

# Example

```
ASK: Hello

AI:
Hello! How can I help you today?

ASK: What is LangGraph?

AI:
LangGraph is a framework for building stateful AI applications...

ASK: exit
```

---

# 📚 Concepts Learned

- LangChain
- LangGraph
- State Management
- Nodes
- Edges
- Graph Compilation
- Memory
- Thread IDs
- LLM Invocation
- Stateful Chatbots

---

# 🚀 Future Improvements

- Retrieval-Augmented Generation (RAG)
- PDF Chat
- SQL Agent
- Web Search
- Human-in-the-Loop
- Multi-Agent Systems
- Streaming Responses
- Persistent Database Memory
- Tool Calling
- Authentication

---

# 📄 License

This project is created for learning LangGraph fundamentals and understanding graph-based AI application development.