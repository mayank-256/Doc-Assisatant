from langchain_text_splitters import RecursiveCharacterTextSplitter
import uuid

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
# chunking
def split_documents(documents):

    splitter = RecursiveCharacterTextSplitter(

        chunk_size=CHUNK_SIZE,

        chunk_overlap=CHUNK_OVERLAP,

        separators=[
            "\n# ",
            "\n## ",
            "\n### ",
            "\n\n",
            "\n",
            " ",
            ""
        ],

        add_start_index=True
    )

    chunks = splitter.split_documents(documents)

    return chunks


# to store the chunks into chromadb
def store_chunks(chunks, collection):
    if not chunks:
        print("No chunks available to store")
    ids = []
    texts = []
    metadatas = []

    for index, chunk in enumerate(chunks):
        source = chunk.metadata["source"]

        chunk_id = str(
            uuid.uuid5(
                uuid.NAMESPACE_URL,
                f"{source}:{index}"
            )
        )

        metadata = {
            **chunk.metadata,
            "chunk_index": index
        }

        ids.append(chunk_id)
        texts.append(chunk.page_content)
        metadatas.append(metadata)

    collection.add(
        ids=ids,
        documents=texts,
        metadatas=metadatas
    )

    print(f"Successfully stored {len(chunks)} chunks!")
