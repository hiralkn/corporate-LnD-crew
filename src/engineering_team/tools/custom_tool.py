import os
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from crewai.tools import tool

# Global storage variable for our runtime vector database
_training_vector_store = None

def initialize_training_rag(file_path: str):
    """Parses user-uploaded training guidelines or architecture documents into dynamic Chroma vector indices."""
    global _training_vector_store
    
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
        
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=120)
    chunks = text_splitter.split_text(text)
    
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    _training_vector_store = Chroma.from_texts(chunks, embeddings)

@tool("Query Internal Architecture and Training Requirements")
def query_learning_tool(query: str) -> str:
    """Useful to search internal corporate infrastructure profiles, legacy codebase rules, and training standards."""
    global _training_vector_store
    if _training_vector_store is None:
        return "Operational Warning: No core instruction files have been initialized in the RAG container."
    
    docs = _training_vector_store.similarity_search(query, k=3)
    return "\n\n--- Corporate Training Clause Chunk ---\n".join([doc.page_content for doc in docs])
