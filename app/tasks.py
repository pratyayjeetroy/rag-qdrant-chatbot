from retriever import ask_question

def process_query(query):
    try:
        print(f"🔄 Processing: {query}")
        
        result = ask_question(query)
        
        print(f"✅ Completed: {query}")
        return result

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return {
            "answer": "Error processing request",
            "pages": []
        }