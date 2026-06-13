from ingestion import load_and_split
from vector_store import create_vector_store
import os
print("API KEY:", os.getenv("OPENAI_API_KEY"))

if __name__ == "__main__":
    pdf_path = "C:/Users/pratyay roy/Downloads/SQL-Cheat-Sheet.pdf"

    docs = load_and_split(pdf_path)
    db = create_vector_store(docs)

    print("✅ Indexing completed in Qdrant")