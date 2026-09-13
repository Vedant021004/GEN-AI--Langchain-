from llama_cloud import LlamaCloud
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

# Connect to LlamaCloud
client = LlamaCloud(
    api_key=os.getenv("LLAMA_CLOUD_API_KEY"),
    timeout=120.0
)

# Get the file path
path = input("Enter the path of your file: ")

# Upload the file to LlamaCloud
file = client.files.create(
    file=Path(path),
    purpose="parse"
)

print("File uploaded!")
print("File ID:", file.id)

# Parse the uploaded file
result = client.parsing.create(
    tier="agentic",
    version="latest",
    file_id=file.id
)

print("Parsing started!")
print("Parsing ID:", result.id)

# Get the parsed result
parsed = client.parsing.get(
    result.id,
    expand="markdown"
)

# Print the parsed content
for page in parsed.markdown.pages:
    print("\n--- PAGE ---\n")
    print(page.markdown)