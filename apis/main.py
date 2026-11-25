import os

import chromadb

from pathlib import Path

from dotenv import load_dotenv
load_dotenv()

from langchain_groq import ChatGroq

from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

from document_loader_ import load_document
from chunking_ import split_documents, store_chunks
from doc_management import list_documents,add_documents,update_document,delete_document

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# EMBEDDING_MODEL = "sentence-transformer/all-MiniLM-L6-v2"

LLM_MODEL = "openai/gpt-oss-120b"

CHROMA_DIR = "chroma_db"
COLLECTION_NAME = "documents"

def initialize_embeddings():
    embedding_function = SentenceTransformerEmbeddingFunction(
        # model_name=EMBEDDING_MODEL
    )
    print("Embedding model initialized...")
    return embedding_function

def initialize_chroma(embedding_function):
    client = chromadb.PersistentClient(
        path=CHROMA_DIR
    )
    collection = client.get_or_create_collection(
        name = COLLECTION_NAME,
        embedding_function=embedding_function,
        metadata={"hnws:space":"cosine"}
    )
    print("ChromaDB initialized...")
    return collection

def initialize_llm():
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY is not available/missing")
    llm=ChatGroq(
        model=LLM_MODEL ,
        api_key=GROQ_API_KEY,
        temperature=0.1
    )
    print("LLM initialized...")
    return llm


def main():
    embedding_function = initialize_embeddings()
    collection = initialize_chroma(embedding_function)

    print("\nBefore deletion:")
    list_documents(collection)

    print("\nDeleting python.md...")

    delete_document(
        document_name="python.md",
        collection=collection
    )

    print("\nAfter deletion:")
    list_documents(collection)

    print("\nTotal ChromaDB records:", collection.count())


# def main():

#     embedding_function = initialize_embeddings()
#     collection = initialize_chroma(embedding_function)
#     add_documents("test_files/python.md", collection)
#     list_documents(collection)

    # files = [
    #     "documents/sample.md",
    #     "documents/untitled.pdf"
    # ]

    # for file_path in files:
    #     print(f"\nProcessing: {file_path}")

    #     documents = load_document(file_path)
    #     chunks = split_documents(documents)

    #     print("Extracted documents:", len(documents))
    #     print("Generated chunks:", len(chunks))

    #     store_chunks(chunks, collection)

    # print("\nTotal records in ChromaDB:", collection.count())

    # list_documents(collection)


if __name__ == "__main__":
    main()
