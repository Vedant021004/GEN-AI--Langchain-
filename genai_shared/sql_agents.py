"""Shared SQL database and SQL-agent construction helpers."""

from typing import Any

from langchain.agents import create_agent
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.utilities import SQLDatabase


def build_sql_agent(
    db: SQLDatabase,
    llm: Any,
    system_prompt: str,
    checkpointer: Any = None,
) -> Any:
    """Create an agent backed by the database's SQL toolkit."""
    tools = SQLDatabaseToolkit(db=db, llm=llm).get_tools()
    return create_agent(
        model=llm,
        tools=tools,
        system_prompt=system_prompt,
        checkpointer=checkpointer,
    )


def connect_db(uri: str, setup_sql: str | None = None) -> SQLDatabase:
    """Connect to a database and optionally run setup SQL."""
    db = SQLDatabase.from_uri(uri)
    if setup_sql is not None:
        db.run(setup_sql)
    return db
