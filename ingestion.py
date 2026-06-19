import re
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


def clean_text(text):
    text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)
    text = re.sub(r'([A-Za-z])\(', r'\1 (', text)
    text = re.sub(r'\)([A-Za-z])', r') \1', text)
    text = re.sub(r'\s+', ' ', text)
    return text


def load_and_split(pdf_path):
    loader = PyMuPDFLoader(pdf_path)
    docs = loader.load()

    for doc in docs:
        doc.page_content = clean_text(doc.page_content)
        doc.metadata["page"] = doc.metadata.get("page", 0)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    return splitter.split_documents(docs)