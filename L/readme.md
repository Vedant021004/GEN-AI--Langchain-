# 🤖 LangGraph Tool-Calling Agent

<p align="center">
  <b>LLM + Tools + LangGraph + LangSmith</b>
</p>

<p align="center">
  A simple agentic AI project demonstrating how an LLM decides when to use tools,
  executes them through LangGraph, and continues the conversation.
</p>

---

## 🧠 How It Works

```text
                         👤 USER
                            │
                            ▼
                     🧠 CHATBOT
                            │
                            ▼
                  🔀 TOOL REQUIRED?
                     /          \
                   NO            YES
                   │              │
                   ▼              ▼
                  END         🔧 TOOL NODE
                                  │
                    ┌─────────────┼─────────────┐
                    ▼             ▼             ▼
                  ➕ ADD       ➖ SUBTRACT     🔎 SEARCH
                    │             │             │
                    └─────────────┼─────────────┘
                                  │
                                  ▼
                              🧠 CHATBOT
                                  │
                                  ▼
                                 END

The core idea:

The LLM decides what to do → ToolNode executes it → the result goes back to the LLM.

🎯 What This Project Demonstrates
🧠 LLM tool calling
🔧 Custom LangChain tools
🔗 bind_tools()
🧩 ToolNode
🔀 Conditional edges
🔄 Agent loops
🗂️ LangGraph state
💾 In-memory checkpointing
🧪 LangGraph Studio
📊 LangSmith tracing
🔧 Tools

The agent currently has four tools:

➕ add()
➖ subtract()
🔎 search()
🌤️ get_weather()

Example:

@tool
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

These tools are intentionally simple so the agent workflow is easy to understand.

🔗 Tool Binding

Tools are provided to the LLM using:

tools = [
    add,
    subtract,
    search,
    get_weather
]

llm_with_tools = llm.bind_tools(tools)

Think of bind_tools() as:

LLM
 │
 ├── add()
 ├── subtract()
 ├── search()
 └── get_weather()

The LLM now knows which tools are available.

🔨 ToolNode

ToolNode is responsible for executing the tool requested by the LLM.

graph_builder.add_node(
    "tools",
    ToolNode(tools)
)
Simple distinction
@tool
   ↓
Creates a capability

ToolNode
   ↓
Executes that capability inside LangGraph
🔀 Conditional Edge

The agent should not use a tool for every message.

graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition
)

It creates this decision:

                 CHATBOT
                    │
                    ▼
             TOOL REQUIRED?
               /         \
             NO           YES
             │             │
             ▼             ▼
            END        TOOL NODE

So:

"Hello"
   ↓
No tool
   ↓
END

But:

"Calculate 25 + 15"
   ↓
Tool required
   ↓
add(25, 15)
🔄 Agent Loop

After the tool executes:

graph_builder.add_edge(
    "tools",
    "chatbot"
)

The result goes back to the LLM.

USER
 ↓
CHATBOT
 ↓
LLM
 ↓
TOOL CALL
 ↓
TOOL NODE
 ↓
TOOL RESULT
 ↓
CHATBOT
 ↓
FINAL ANSWER

Example:

User
 ↓
"Calculate 25 + 15"
 ↓
LLM
 ↓
add(25, 15)
 ↓
40
 ↓
LLM
 ↓
"The answer is 40."
🗂️ State

LangGraph keeps the conversation inside a shared state.

class State(TypedDict):
    messages: Annotated[
        list[BaseMessage],
        add_messages
    ]

Think of it as:

USER
 ↓
STATE
 ↓
CHATBOT
 ↓
TOOL
 ↓
STATE
 ↓
CHATBOT

The state carries the messages between graph steps.

💾 InMemorySaver

For local development, the graph can use:

memory = InMemorySaver()

It stores checkpoints temporarily in memory.

LangGraph
    ↓
InMemorySaver
    ↓
   RAM

Useful for:

Learning
Testing
Prototyping
📊 LangSmith

LangSmith is not a node in the graph.

It works as the observability layer.

              LANGGRAPH
                  │
       ┌──────────┼──────────┐
       ▼          ▼          ▼
      LLM       TOOLS      STATE
       │          │          │
       └──────────┼──────────┘
                  ▼
              LANGSMITH
                  │
        ┌─────────┼─────────┐
        ▼         ▼         ▼
      TRACE     DEBUG    EVALUATE
Without LangSmith

You mainly see:

Input → Agent → Answer
With LangSmith

You can inspect:

Input
 ↓
Chatbot
 ↓
LLM Call
 ↓
Tool Call
 ↓
Tool Execution
 ↓
Tool Result
 ↓
LLM
 ↓
Final Answer

This helps with:

🔍 Debugging
📈 Monitoring
🧪 Evaluation
⏱️ Latency analysis
🔧 Tool-call inspection
🧠 LLM-call inspection
Simple way to remember

LangGraph runs the agent. LangSmith shows you what happened inside the agent.

🖥️ LangGraph Studio

The graph can be run locally using LangGraph CLI.

Install:

pip install -U "langgraph-cli[inmem]"

Create langgraph.json:

{
  "dependencies": ["."],
  "graphs": {
    "agent": "./agent.py:graph"
  },
  "env": ".env"
}

Run:

langgraph dev

Studio allows you to interact with the graph and inspect its execution visually.

🔐 Environment Variables

Create .env:

GROQ_API_KEY=your_groq_api_key

LANGSMITH_API_KEY=your_langsmith_api_key
LANGSMITH_TRACING=true
LANGSMITH_PROJECT=langgraph-tool-agent

Load them:

from dotenv import load_dotenv

load_dotenv()

⚠️ Never commit .env or expose API keys on GitHub.

Add this to .gitignore:

.env
📁 Project Structure
LangGraph-Tool-Agent/
│
├── agent.py
├── langgraph.json
├── .env
├── .gitignore
├── requirements.txt
└── README.md
⚙️ Installation
git clone <YOUR_REPOSITORY_URL>

cd LangGraph-Tool-Agent

python -m venv env

Windows:

.\env\Scripts\Activate.ps1

Install dependencies:

pip install langchain
pip install langchain-groq
pip install langgraph
pip install langsmith
pip install python-dotenv

Run:

python agent.py

Or start LangGraph Studio:

langgraph dev
🧪 Example

Input:

Calculate 40 + 3 + 5 - 6 - 7 - 8 - 9 * 3 + 4

The agent can decide which tools are required and execute them through the graph.

Another example:

Search for information about LangGraph

The LLM can select:

search()

The graph then executes:

CHATBOT
   ↓
TOOL CONDITION
   ↓
TOOL NODE
   ↓
search()
   ↓
CHATBOT
   ↓
ANSWER
🧭 Complete Mental Model
                    🤖 AGENT
                       │
                       ▼
                  LANGGRAPH
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
        STATE         NODES        EDGES
                       │
                 ┌─────┴─────┐
                 ▼           ▼
              CHATBOT     TOOLNODE
                 │           │
                 ▼           ▼
                LLM        TOOLS
                             │
                  ┌──────────┼──────────┐
                  ▼          ▼          ▼
                 ADD      SUBTRACT    SEARCH

                       │
                       ▼
                  LANGSMITH
                       │
             ┌─────────┼─────────┐
             ▼         ▼         ▼
           TRACE     DEBUG    EVALUATE
🚀 Next Steps

This project is the foundation for more advanced agentic AI systems:

Tool Calling
      ↓
LangGraph
      ↓
RAG Agent
      ↓
SQL Agent
      ↓
Memory
      ↓
Human-in-the-Loop
      ↓
Multi-Agent System
      ↓
LangSmith Evaluation
      ↓
Production AI
💡 Key Takeaway
TOOLS
  ↓
Give the LLM capabilities

bind_tools()
  ↓
Makes the LLM aware of those capabilities

ToolNode
  ↓
Executes requested tools

Conditional Edge
  ↓
Decides where the graph goes

State
  ↓
Carries information through the graph

LangGraph
  ↓
Controls the agent workflow

LangGraph Studio
  ↓
Helps develop and inspect the graph

LangSmith
  ↓
Helps trace, debug and evaluate the agent
