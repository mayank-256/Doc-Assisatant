from pathlib import Path
import shutil
from document_loader_ import load_document
from chunking_ import split_documents, store_chunks

def list_documents(collection):
    documents_dir = Path("documents")

    files = [
        file for file in documents_dir.iterdir()
        if file.is_file() and file.suffix.lower() in [".pdf", ".doc", ".md"]
    ]

    results = collection.get(include=["metadatas"])

    print("\nDEBUG: Sources stored in ChromaDB")

    for metadata in results["metadatas"]:
        print(metadata.get("source"))
        
    chunk_counts = {}

    for metadata in results["metadatas"]:
        source = metadata.get("source")

        if source:
            chunk_counts[source] = chunk_counts.get(source, 0) +1

    print("\n========== AVAILABLE DOCUMENTS ==========")

    if not files:
        print("No documents found.")
        return

    for index, file in enumerate(sorted(files), start=1):
        source = str(file.resolve()) #for absolute path we use resolve
        chunks = chunk_counts.get(source,0)

        print(f"\n{index}.{file.name}")
        print(f"   Type: {file.suffix.lower()}")
        print(f"   Indexed chunks: {chunks}")

        

    print("\n=========================================")

def add_documents(file_path, collection):
    file_path = Path(file_path)
    document__dir = Path("documents")

    supported_extensions = ['.pdf', '.doc', '.md']

    if not file_path.exists() or not file_path.is_file():
        print("File does not exists")
        return

    if file_path.suffix.lower() not in supported_extensions:
        print("Unsopported format")
        return 

    destination = document__dir / file_path.name

    if destination.exists():
        print("Document already exists")
        return

    shutil.copy2(file_path, destination)

    documents = load_document(destination)

    if not documents:
        print("No text found in document.")
        destination.unlink()
        return

    chunks = split_documents(documents)
    store_chunks(chunks, collection)
    print(f"Document added successfully: {destination.name}")

def update_document(document_name, new_file_path, collection):
    document_str = Path("documents")

    destination = document_str / document_name

    if not destination.exists() or not destination.is_file():
        print("Document does not exist.")
        return

    new_file_path = Path(new_file_path)

    if not new_file_path.exists() or not new_file_path.is_file():
        print("Updated file does not exist.")
        return

    if new_file_path.suffix.lower() not in [".pdf", ".docx", ".md"]:
        print("Unsupported file format.")
        return

    if destination.suffix.lower() != new_file_path.suffix.lower():
        print("Updated file must have the same format.")
        return

    documents = load_document(new_file_path)

    if not documents:
        print("Updated document contains no readable text.")
        return

    
    for document in documents:
        document.metadata["source"] = str(destination.resolve())
        document.metadata["file_name"] = destination.name

    chunks = split_documents(documents)

    if not chunks:
        print("No chunks generated.")
        return

    
    source = str(destination.resolve())

    collection.delete(
        where={"source": source}
    )

    shutil.copy2(new_file_path, destination)

    store_chunks(chunks, collection)

    print(f"Document updated successfully: {document_name}")


def delete_document(document_name, collection):
    documents_dir = Path("documents")

    file_path = documents_dir / document_name

    if not file_path.exists() or not file_path.is_file():
        print("Document does not exist.")
        return

    source = str(file_path.resolve())

    collection.delete(
        where={"source": source}
    ) #deletes data from chromadb

    file_path.unlink() # to delete local document

    print(f"Document deleted successfully: {document_name}")
