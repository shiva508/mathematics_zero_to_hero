from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


def get_grouping_splitting_documents_by_metadata():
    docs = [
        Document(
            page_content="RAG combines retrieval with generation for better answers.",
            metadata={"source": "rag_with_python_cookbook.txt"}
        ),
        Document(
            page_content="LangChain supports many loaders and chunking strategies.",
            metadata={"source": "langchain_guide.md"}
        ),
        Document(
            page_content="You can use FAISS or Chroma for vector storage.",
            metadata={"source": "vector_stores.pdf"}
        ),
    ]

    # 2. Initialize the RecursiveCharacterTextSplitter with desired parameters Here, chunk_size=60 means each chunk will have a maximum of 60 characters,
    recursive_character_text_splitter = RecursiveCharacterTextSplitter(chunk_size=60, chunk_overlap=0)
    grouped_by_source = {}
    for doc in docs:
        source = doc.metadata["source"]
        grouped_by_source.setdefault(source, []).append(doc)

    # 4. Split each document into chunks and group by source, This will ensure that chunks from the same source are processed together
    all_chunks = []
    for source, group in grouped_by_source.items():
        for doc in group:
            chunk = recursive_character_text_splitter.split_documents([doc])
            all_chunks.append(chunk)
    # 5. Print the resulting chunks with their metadata, Each chunk will retain the source metadata for context
    for i, chunk in enumerate(all_chunks, 1):
        print(f"\n--- Chunk {i} (Source: {chunk[0].metadata.get("source")}) ---")
        print(chunk[0].page_content)

if __name__ == "__main__":
    get_grouping_splitting_documents_by_metadata()