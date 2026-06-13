from qdrant_client import QdrantClient
from langchain_qdrant import QdrantVectorStore
# from langchain_openai import OpenAIEmbeddings
from config import QDRANT_URL, COLLECTION_NAME
from langchain_huggingface import HuggingFaceEmbeddings

def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )


def get_qdrant_client():
    return QdrantClient(url=QDRANT_URL)


def create_vector_store(docs):
    embeddings = get_embeddings()
    # embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)

    db = QdrantVectorStore.from_documents(
        docs,
        embeddings,
        url=QDRANT_URL,
        collection_name=COLLECTION_NAME
    )

    return db


def load_vector_store():
    client = get_qdrant_client()
    embeddings = get_embeddings()
    # embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)

    db = QdrantVectorStore(
        client=client,
        collection_name=COLLECTION_NAME,
        embedding=embeddings
    )

    return db