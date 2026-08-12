from dotenv import load_dotenv
import os

load_dotenv()

print(os.getenv("TAVILY_API_KEY"))