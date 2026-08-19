from langgraph.checkpoint.memory import InMemorySaver
from genai_shared.chat import agent_responder, chat_loop
from genai_shared.llms import ollama_llm
from genai_shared.sql_agents import build_sql_agent, connect_db

db = connect_db("mysql+pymysql://root:ved%40nt@127.0.0.1:3306/analyzer_ai")

print(db.get_usable_table_names())

db.run("""CREATE TABLE employees (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    department VARCHAR(50),
    salary INT
);
"""
)


llm = ollama_llm(model="qwen3:latest")

# Memory
memory = InMemorySaver()

system_prompt = """
You are an Employee Management Assistant that interacts with a SQLite database.

The database contains a table named 'employees'.

Columns:
- id
- name
- department
- salary

Rules:
- Use SQL tools whenever database access is required.
- Limit SELECT queries to 10 rows unless the user requests otherwise.
- Order employee records by id ASC unless a different order is requested.
- After every INSERT, UPDATE, or DELETE operation, verify the changes with a SELECT query.
- Never make up employee information.
- If the requested employee does not exist, clearly inform the user.
- Use only the available columns in the 'employees' table.
- Generate safe and valid SQLite SQL queries.
"""


agent = build_sql_agent(db, llm, system_prompt, checkpointer=memory)

print("=" * 60)
print("TaskBot - Manage Your Tasks")
print("Type 'exit' to quit.")
print("=" * 60)

thread_id = input("Enter your User ID: ")


def respond(prompt):
    return f"\nAssistant:\n{agent_responder(agent, thread_id)(prompt)}"


chat_loop(
    respond,
    prompt="\nYou: ",
    exit_words=frozenset({"exit", "quit"}),
    answer_prefix="",
)