"""Reusable prompt and response helpers for command-line chats."""

from collections.abc import Callable
from typing import Any

DEFAULT_EXIT_WORDS = frozenset({"bye", "exit", "quit", "done"})


def chat_loop(
    respond: Callable[[str], str],
    prompt: str = "You: ",
    exit_words: frozenset[str] | set[str] | list[str] = DEFAULT_EXIT_WORDS,
    farewell: str | None = None,
    answer_prefix: str = "AI:",
) -> None:
    """Read prompts until an exit word and print each response."""
    while True:
        text = input(prompt)
        if text.lower().strip() in exit_words:
            if farewell is not None:
                print(farewell)
            break
        answer = respond(text)
        print(f"{answer_prefix} {answer}" if answer_prefix else answer)


def user_message(text: str) -> dict[str, list[dict[str, str]]]:
    """Build the message payload accepted by LangChain agents."""
    return {"messages": [{"role": "user", "content": text}]}


def thread_config(thread_id: str = "1") -> dict[str, dict[str, str]]:
    """Build a LangGraph thread configuration."""
    return {"configurable": {"thread_id": thread_id}}


def last_message_text(result: dict[str, Any]) -> str:
    """Return the content of the final message in an agent result."""
    return result["messages"][-1].content


def agent_responder(agent: Any, thread_id: str = "1") -> Callable[[str], str]:
    """Adapt an agent's invoke method to the command-line chat loop."""
    def respond(text: str) -> str:
        result = agent.invoke(user_message(text), config=thread_config(thread_id))
        return last_message_text(result)

    return respond


def history_responder(llm: Any) -> Callable[[str], str]:
    """Adapt an LLM to a manually maintained conversation history."""
    history: list[dict[str, str]] = []

    def respond(text: str) -> str:
        history.append({"role": "user", "content": text})
        response = llm.invoke(history)
        content = response.content
        history.append({"role": "assistant", "content": content})
        return content

    respond.history = history
    return respond
