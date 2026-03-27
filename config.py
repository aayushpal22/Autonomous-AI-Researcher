import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("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")
TAVILY_API_KEY = os.getenv("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")
LLM_MODEL = os.getenv("LLM_MODEL", "llama3.1-70b-versatile")
KNOWLEDGE_BASE_DIR = os.getenv("KNOWLEDGE_BASE_DIR", "./knowledge_base")
