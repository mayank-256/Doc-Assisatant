import os

import chromadb

from pathlib import Path

from dotenv import load_dotenv
load_dotenv()

from langchain_groq import ChatGroq

from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

from document_loader_ import load_document
from chunking_ import split_documents, store_chunks

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

# def test_chunking():
#     file_psth = Path("documents/sample.md")

#     documents = load_document(file_psth)

#     print("Original Documents: ", len(documents))

#     chunks = split_documents(documents)

#     print("total chunks: ", len(chunks))

#     for index, chunk in enumerate(chunks):

#         print("\n" + "=" * 50)

#         print(f"CHUNK {index}")

#         print("Metadata:", chunk.metadata)

#         print("Content:")
#         print(chunk.page_content)

#         print("Characters:", len(chunk.page_content))

def main():
    # test_chunking()

    
    embedding_function = initialize_embeddings()
    collection = initialize_chroma(
        embedding_function
    )

    # llm = initialize_llm()

    documents = load_document("documents/fastapi.pdf")

    chunks = split_documents(documents)

    print("Total chunks", len(chunks))

    store_chunks(chunks, collection)

    print(
        "Total records in ChromaDB:",
        collection.count()
    )
    # response = llm.invoke(
    #     "Explain what a document assistant does in one sentence."
    # )

    # print("\nGroq Response:")
    # print(response.content)

    # print("\nTotal stored chunks:", collection.count())




if __name__ == "__main__":
    main()
