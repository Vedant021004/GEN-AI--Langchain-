from langchain_community.utilities import SQLDatabase
from langchain_ollama import ChatOllama
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents import create_agent

db = SQLDatabase.from_uri(
    "mysql+pymysql://root:ved%40nt@127.0.0.1:3306/analyzer_ai"
)

print(db.get_usable_table_names())

db.run(
    """CREATE TABLE employees (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    department VARCHAR(50),
    salary INT
);
"""
)


#LLM
llm = ChatOllama(
    model="qwen3:latest"
)

# SQL Toolkit
toolkit = SQLDatabaseToolkit(
    db=db,
    llm=llm
)

tools = toolkit.get_tools()

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


# Agent
agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt=system_prompt,
    checkpointer=memory
)

print("=" * 60)
print("TaskBot - Manage Your Tasks")
print("Type 'exit' to quit.")
print("=" * 60)

thread_id = "vedant"
thread_id = "rahul"
thread_id = "priya"
thread_id = "amit"


thread_id = input("Enter your User ID: ")

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