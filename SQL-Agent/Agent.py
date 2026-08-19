from langgraph.checkpoint.memory import InMemorySaver
from genai_shared.chat import agent_responder, chat_loop
from genai_shared.llms import ollama_llm
from genai_shared.sql_agents import build_sql_agent, connect_db

# Database
db = connect_db("sqlite:///my_tasks.db", """
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    status TEXT CHECK(status IN ('pending','in_progress','completed')) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""")

# LLM
model = ollama_llm()

# Memory
memory = InMemorySaver()

# System Prompt
system_prompt = """
You are a Task Management Assistant that interacts with a SQLite database.

The database contains a table named 'tasks'.

Columns:
- id
- title
- description
- status (pending, in_progress, completed)
- created_at

Rules:
- Use SQL tools whenever database access is required.
- Limit SELECT queries to 10 rows.
- Order results by created_at DESC.
- After INSERT, UPDATE, or DELETE, verify the result with a SELECT query.
- Never make up task data.
"""

# Agent
agent = build_sql_agent(db, model, system_prompt, checkpointer=memory)

print("=" * 60)
print("TaskBot - Manage Your Tasks")
print("Type 'exit' to quit.")
print("=" * 60)

thread_id = "amit"


chat_loop(
    agent_responder(agent, thread_id),
    prompt="\nYou: ",
    exit_words=frozenset({"exit", "quit"}),
    answer_format="\nAssistant:\n{answer}",
)