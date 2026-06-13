from vector_store import load_vector_store
from langchain_openai import ChatOpenAI
from config import LLM_MODEL
import os


def ask_question(query):
    db = load_vector_store()

    retriever = db.as_retriever(search_kwargs={"k": 3})

    docs = retriever.invoke(query)

    # ❗ STRICT FILTER
    if not docs:
        return {
            "answer": "Answer not found in provided documents.",
            "pages": []
        }

    context = "\n\n".join([d.page_content for d in docs])
    pages = list(set([d.metadata.get("page") for d in docs]))

    # extra guard
    if len(context.strip()) < 50:
        return {
            "answer": "Answer not found in provided documents.",
            "pages": []
        }

    llm = ChatOpenAI(model=LLM_MODEL, temperature=0)

    prompt = f"""
You are a strict document QA system.

Rules:
- Answer ONLY from the context
- If answer is not present, say: "Answer not found in provided documents."
- Always be concise

Context:
{context}

Question:
{query}
"""

    response = llm.invoke(prompt)

    return {
        "answer": response.content,
        "pages": pages
    }


if __name__ == "__main__":
    while True:
        q = input("\nAsk: ")
        result = ask_question(q)

        print("\nAnswer:", result["answer"])
        print("Pages:", result["pages"])