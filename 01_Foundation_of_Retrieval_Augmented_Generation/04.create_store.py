from langchain_community.document_loaders import UnstructuredWordDocumentLoader
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Create a Chroma vector store from text embeddings using LangChain's HuggingFaceEmbeddings.
def create_chroma_store():
    # Sample texts to embed
    texts = [
        "Chroma is a popular vector database used to store embeddings (vectors).",
        "We are using sentence transformers for generating embeddings.",
        "RAG is a polpular framework to make Agentic AI applications.",
        "LangChain is a framework for builing applications using LLM.",
    ]
    # Load the embedding model
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    # Create a Chroma vector store from the embeddings, This will convert the list of texts into their corresponding vector embeddings and create an index.
    vector_store = Chroma.from_texts(
        texts,
        embedding=embedding_model,
        persist_directory="chroma_vector_store"
    )

    # Persist the vector store
    vector_store.add_texts(texts)

    # This will find the top-k most similar texts to the query based on their embeddings.
    query = "Which database is used to store embeddings?"
    results = vector_store.similarity_search(query, k=1)

    for result in results:
        print(result)

# Create a Chroma vector store from text embeddings using LangChain's HuggingFaceEmbeddings.
def create_chroma_store_file():
    texts_blocks = []

    # Load file
    unstructured_word_document_loader = UnstructuredWordDocumentLoader("01_Foundation_of_Retrieval_Augmented_Generation/4 Dogs.docx")
    word_documents = unstructured_word_document_loader.load()

    # splitting documents
    recursive_character_text_splitter = RecursiveCharacterTextSplitter(
                                    chunk_size = 300,# max characters (≈ 120150 tokens) per chunk
                                    chunk_overlap = 50, # characters of overlap to preserve context
                                    separators = ["\n\n", "\n", ".", " ", ""], # split on these char
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
    vector_store = Chroma.from_texts(
        texts_blocks,
        embedding=embedding_model,
        persist_directory="chroma_vector_store"
    )

    # Persist the vector store
    vector_store.add_texts(texts_blocks)

    # This will find the top-k most similar texts to the query based on their embeddings.
    query = "If you love something what would you do ?"
    results = vector_store.similarity_search(query, k=1)

    for result in results:
        print(result.page_content)


# Create a FAISS vector store using LangChain and Hugging Face embeddings
def create_faiss_store_file():

    # Load file
    unstructured_word_document_loader = UnstructuredWordDocumentLoader("01_Foundation_of_Retrieval_Augmented_Generation/4 Dogs.docx")
    word_documents = unstructured_word_document_loader.load()

    # splitting documents
    recursive_character_text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,  # max characters (≈ 120150 tokens) per chunk
        chunk_overlap=50,  # characters of overlap to preserve context
        separators=["\n\n", "\n", ".", " ", ""],  # split on these char
    )
    recursive_character_text_splitter.split_documents(word_documents)
    word_document_chunks = recursive_character_text_splitter.split_documents(word_documents)

    # Load embedding model
    embedding_model = HuggingFaceEmbeddings()

    # Create a FAISS vector store from the document chunks and embeddings, This allows for efficient similarity search.
    faiss_index = FAISS.from_documents(word_document_chunks, embedding_model)

    # 5. Perform a similarity search
    # This will find the most relevant chunks based on a query.
    query = "If you love something what would you do ?"
    results = faiss_index.similarity_search(query, k=1)
    for result in results:
        print(result.page_content)

if __name__ == "__main__":
    #create_chroma_store()
    #create_chroma_store_file()
    create_faiss_store_file()
