# 🤖 LangGraph Tool-Calling Agent

<p align="center">
  <b>LLM → Tool Calling → Conditional Routing → ToolNode → Agent Loop → LangSmith</b>
</p>

<p align="center">
  An interactive LangGraph project for understanding how an LLM-powered agent selects tools,
  executes them, processes results, and continues through a graph-based workflow.
</p>

---

## 🎮 Interactive Simulator

> **Don't just read the architecture — run it visually.**

The project includes an interactive simulator that demonstrates how a LangGraph agent moves through each stage of execution.

### Agent Flow

```text
                         USER
                           │
                           ▼
                     ┌──────────┐
                     │ CHATBOT  │
                     └────┬─────┘
                          │
                          ▼
                  ┌───────────────┐
                  │ TOOL REQUIRED?│
                  └───────┬───────┘
                          │
                    ┌─────┴─────┐
                    │           │
                   NO          YES
                    │           │
                    ▼           ▼
                   END       TOOL NODE
                                │
                    ┌───────────┼───────────┐
                    ▼           ▼           ▼
                   ADD       SUBTRACT     SEARCH
                    │           │           │
                    └───────────┼───────────┘
                                │
                                ▼
                             CHATBOT
                                │
                                ▼
                              END
````

### What the simulator demonstrates

| Stage        | What happens                             |
| ------------ | ---------------------------------------- |
| 👤 User      | Sends a request                          |
| 🧠 Chatbot   | Sends the request to the LLM             |
| 🔀 Condition | Checks whether a tool call was requested |
| 🔧 ToolNode  | Executes the requested tool              |
| ⚙️ Tool      | Performs the operation                   |
| 🔄 Loop      | Sends the result back to the LLM         |
| ✅ End        | Produces the final response              |
| 📊 LangSmith | Traces the execution                     |

### Example

```text
User
│
│ "Calculate 25 + 15"
▼
CHATBOT
│
│ LLM decides:
│ add(25, 15)
▼
TOOL CONDITION
│
│ Tool call detected
▼
TOOL NODE
│
▼
add(25, 15)
│
│ Result = 40
▼
CHATBOT
│
│ "The answer is 40."
▼
END
```

---

## 🧠 Why a Simulator?

A LangGraph workflow can initially look confusing because several concepts interact:

```text
LLM
 │
 ├── Tools
 │
 ├── Tool Binding
 │
 ├── ToolNode
 │
 ├── State
 │
 ├── Conditional Edges
 │
 └── Loops
```

The simulator makes the execution order visible.

Instead of only seeing:

```python
graph.invoke(...)
```

you can understand what is happening internally:

```text
INPUT
  ↓
STATE
  ↓
CHATBOT
  ↓
LLM
  ↓
TOOL CALL?
  ↓
TOOL NODE
  ↓
TOOL EXECUTION
  ↓
TOOL RESULT
  ↓
CHATBOT
  ↓
FINAL RESPONSE
```

---

# 🔬 Simulator Concepts

## Tool Binding

```python
llm_with_tools = llm.bind_tools(tools)
```

Simulator:

```text
LLM
 │
 ▼
AVAILABLE TOOLS
 ├── add
 ├── subtract
 ├── search
 └── get_weather
```

The model knows which tools are available.

---

## Conditional Routing

```python
graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition
)
```

Simulator:

```text
                 CHATBOT
                    │
                    ▼
             TOOL CALL EXISTS?
                /          \
              NO            YES
              │              │
              ▼              ▼
             END          TOOL NODE
```

---

## ToolNode

```python
ToolNode(tools)
```

Simulator:

```text
TOOL NODE
    │
    ├── add()
    ├── subtract()
    ├── search()
    └── get_weather()
```

The ToolNode is responsible for executing the tool requested by the LLM.

---

## Agent Loop

```python
graph_builder.add_edge(
    "tools",
    "chatbot"
)
```

Simulator:

```text
CHATBOT
   ↓
TOOL
   ↓
TOOL RESULT
   ↓
CHATBOT
   ↓
FINAL ANSWER
```

This is what makes the workflow agentic rather than simply:

```text
INPUT → LLM → OUTPUT
```

---

# 📊 LangSmith Layer

The simulator explains the **LangGraph execution**.

LangSmith explains what happened during that execution.

```text
                LANGGRAPH
                    │
        ┌───────────┼───────────┐
        ▼           ▼           ▼
     CHATBOT      TOOLS       STATE
        │           │           │
        └───────────┼───────────┘
                    │
                    ▼
                LANGSMITH
                    │
        ┌───────────┼───────────┐
        ▼           ▼           ▼
      TRACE       DEBUG       EVALUATE
```

So the roles are:

```text
LANGGRAPH
→ Builds and executes the workflow.

SIMULATOR
→ Helps understand the workflow visually.

LANGGRAPH STUDIO
→ Interactively develops and inspects the graph.

LANGSMITH
→ Traces, debugs, evaluates and monitors executions.
```

---

# 🚀 Learning Path

```text
Python
  ↓
LangChain
  ↓
Tools
  ↓
bind_tools()
  ↓
ToolNode
  ↓
LangGraph
  ↓
State
  ↓
Conditional Edges
  ↓
Agent Loop
  ↓
LangGraph Studio
  ↓
LangSmith
  ↓
RAG Agents
  ↓
SQL Agents
  ↓
Multi-Agent Systems
  ↓
Production AI
```

```

