from langchain_chroma import Chroma
from langchain_community.document_loaders import UnstructuredWordDocumentLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


# retrieve text chunks from a Chroma vector store using LangChain's Hugging Face
def retrieval_from_chrome_store():
    texts_blocks = []

    # Load file
    unstructured_word_document_loader = UnstructuredWordDocumentLoader("4 Dogs.docx")
    word_documents = unstructured_word_document_loader.load()

    # splitting documents
    recursive_character_text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,  # max characters (≈ 120150 tokens) per chunk
        chunk_overlap=50,  # characters of overlap to preserve context
        separators=["\n\n", "\n", ".", " ", ""],  # split on these char
    )
    recursive_character_text_splitter.split_documents(word_documents)
    word_document_chunks = recursive_character_text_splitter.split_documents(word_documents)

    for chunk in range(len(word_document_chunks)):
        content = word_document_chunks[chunk].page_content
        texts_blocks.append(content)
        print(f"Chunk {chunk}: {content}")

    # Load embedding model
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # Create a Chroma vector store from the embeddings, This will convert the list of texts into their corresponding vector embeddings and create an index.
    vector_store = Chroma(
        persist_directory="chroma_vector_store",
        embedding_function=embedding_model
    )

    # Persist the vector store
    vector_store.add_texts(texts_blocks)

    # This will find the top-k most similar texts to the query based on their embeddings.
    query = "If you love something what would you do ?"
    results = vector_store.similarity_search(query, k=1)

    for result in results:
        print(result.page_content)


if __name__ == "__main__":
    retrieval_from_chrome_store()