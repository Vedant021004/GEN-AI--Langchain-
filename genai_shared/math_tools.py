"""Arithmetic tools shared by the agent examples."""

from langchain_core.tools import tool


@tool
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b


@tool
def subtract(a: int, b: int) -> int:
    """Subtract b from a."""
    return a - b


@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b


@tool
def divide(a: int, b: int) -> int | float | str:
    """Divide a by b."""
    if b == 0:
        return "Division by zero is not allowed."
    return a / b


MATH_TOOLS = [add, subtract, multiply, divide]
