from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents import create_agent

load_dotenv()

# Database
db = SQLDatabase.from_uri("sqlite:///my_tasks.db")

db.run("""
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    status TEXT CHECK(status IN ('pending','in_progress','completed')) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""")

# LLM
model = ChatOllama(
    model="llama3.2"
)

# SQL Toolkit
toolkit = SQLDatabaseToolkit(
    db=db,
    llm=model
)

tools = toolkit.get_tools()

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
agent = create_agent(
    model=model,
    tools=tools,
    system_prompt=system_prompt,
    checkpointer=memory
)

print("=" * 60)
print("TaskBot - Manage Your Tasks")
print("Type 'exit' to quit.")
print("=" * 60)

thread_id = "user_1"

while True:

    prompt = input("\nYou: ")

    if prompt.lower() in ["exit", "quit"]:
        break

    response = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        },
        config={
            "configurable": {
                "thread_id": thread_id
            }
        }
    )

    print("\nAssistant:")
    print(response["messages"][-1].content)