import json

from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage

# Load LLM
llm = ChatOllama(
    model="qwen3:latest",
    temperature=0
)

# System Prompt
system_prompt = """
You are an AI Document Classifier.

Classify the document into ONE of these categories:

1. structured
   - Mostly tables, rows, columns or records.

2. unstructured
   - Mostly paragraphs, reports, policies or plain text.

3. mixed
   - Contains both tables and paragraphs.

Return ONLY valid JSON.

Example:

{
    "document_type": "mixed",
    "store_sql": true,
    "store_rag": true,
    "reason": "The document contains both tables and descriptive text."
}
"""

# Classification Function
def classify_document(text):

    response = llm.invoke(
        [
            SystemMessage(content=system_prompt),
            HumanMessage(content=text[:3000])   # Send first 3000 characters
        ]
    )

    # Convert JSON string to Python Dictionary. A model that ignores the
    # "JSON only" instruction otherwise fails with a bare JSONDecodeError
    # that does not show what was actually returned.
    try:
        result = json.loads(response.content)
    except json.JSONDecodeError as e:
        raise ValueError(
            f"Classifier did not return valid JSON. Raw response: {response.content!r}"
        ) from e

    missing = [
        key
        for key in ("document_type", "store_sql", "store_rag", "reason")
        if key not in result
    ]
    if missing:
        raise ValueError(
            f"Classifier response is missing key(s) {missing}. Raw response: {response.content!r}"
        )

    return result


# Sample Document
sample = """
Employee Details

Name      Salary      Department

John      50000       IT
Alice     65000       HR

----------------------------------

Company Policy

Employees receive 20 paid leaves every year.
Remote work is allowed twice a week.
"""

# Run Classifier
result = classify_document(sample)

print(result)

print("\nDocument Type :", result["document_type"])
print("Store SQL     :", result["store_sql"])
print("Store RAG     :", result["store_rag"])
print("Reason        :", result["reason"])