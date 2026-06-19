from vector_store import load_vector_store
from langchain_ollama import ChatOllama


def ask_question(query):
    db = load_vector_store()

    # 🔥 Custom similarity search
    # docs_with_scores = db.similarity_search_with_score(query, k=5)

    # # 🔥 Sort by score (lower = better)
    # docs_with_scores = sorted(docs_with_scores, key=lambda x: x[1])

    # # 🔥 Take top 3 (no strict threshold)
    # docs = [doc for doc, _ in docs_with_scores[:3]]
    docs_with_scores = db.similarity_search_with_score(query, k=10)

# 🔥 Keyword boosting
    boosted_docs = []
    for doc, score in docs_with_scores:
        content = doc.page_content.lower()

        if "dcl" in content or "data control language" in content:
            boosted_docs.insert(0, (doc, score))
        else:
            boosted_docs.append((doc, score))

    # Sort
    boosted_docs = sorted(boosted_docs, key=lambda x: x[1])

    # Diversity selection
    docs = []
    seen_pages = set()

    for doc, score in boosted_docs:
        page = doc.metadata.get("page", 0)

        if page not in seen_pages:
            docs.append(doc)
            seen_pages.add(page)

        if len(docs) == 3:
            break 
    # ❗ STRICT FILTER
    if not docs:
        return {
            "answer": "Answer not found in provided documents.",
            "pages": []
        }

    # 🔍 Debug
    print("\n--- Retrieved Docs ---")
    for doc, score in docs_with_scores[:3]:
        print(f"Page: {doc.metadata.get('page', 0) + 1} | Score: {score}")
        print(doc.page_content[:200])
        print("------")

    # 🔥 Build context (trim for memory safety)
    context = "\n\n".join([d.page_content for d in docs])
    context = context[:1500]   # 🔥 IMPORTANT (avoid RAM crash)

    pages = list(set([(d.metadata.get("page", 0) + 1) for d in docs]))

    # Extra guard
    if len(context.strip()) < 50:
        return {
            "answer": "Answer not found in provided documents.",
            "pages": []
        }

    # 🔥 Mistral (memory optimized)
    llm = ChatOllama(
        model="mistral",
        temperature=0,
        num_ctx=512,
        num_predict=100
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