QDRANT_URL = "http://localhost:6333"
COLLECTION_NAME = "pdf_docs"

# EMBEDDING_MODEL = "text-embedding-3-small"
LLM_MODEL = "gpt-5"
from dotenv import load_dotenv

load_dotenv()

# print(os.getenv("OPENAI_API_KEY"))