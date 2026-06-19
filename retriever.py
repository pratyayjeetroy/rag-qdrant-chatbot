from vector_store import load_vector_store
from langchain_ollama import ChatOllama


def ask_question(query):
    db = load_vector_store()

    retriever = db.as_retriever(search_kwargs={"k": 3})
    docs = retriever.invoke(query)

    if not docs:
        return {
            "answer": "Answer not found in provided documents.",
            "pages": []
        }

    # Debug (VERY IMPORTANT)
    print("\n--- Retrieved Docs ---")
    for d in docs:
        print("Page:", d.metadata.get("page", 0) + 1)
        print(d.page_content[:200])

    context = "\n\n".join([d.page_content for d in docs])
    pages = list(set([(d.metadata.get("page", 0) + 1) for d in docs]))

    if len(context.strip()) < 50:
        return {
            "answer": "Answer not found in provided documents.",
            "pages": []
        }

    llm = ChatOllama(
        model="mistral",
        temperature=0,
        num_ctx=512
    )

    prompt = f"""
You are a strict document QA system.

Rules:
- Answer ONLY using the provided context
- If the answer is clearly present, return it
- If the answer is NOT present, say EXACTLY:
  "Answer not found in provided documents."
- Do NOT guess
- Ignore unrelated context

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