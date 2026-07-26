from langchain_community.document_loaders import UnstructuredWordDocumentLoader
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter, CharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama, embeddings
from langchain_core.output_parsers import StrOutputParser


# Retrieve text chunks from a Chroma vector store using LangChain's Hugging Face
def retrieval_from_chrome_store():
    texts_blocks = []

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

    for chunk in range(len(word_document_chunks)):
        content = word_document_chunks[chunk].page_content
        texts_blocks.append(content)
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
    results = vector_store.similarity_search(query, k=3)

    for result in results:
        print("")
        print(result.page_content)


# Similarity search with scores using LangChain and FAISS:

def retrieval_from_faiss_store():
    # Load file
    unstructured_word_document_loader = UnstructuredWordDocumentLoader(
        "01_Foundation_of_Retrieval_Augmented_Generation/4 Dogs.docx")
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
    results_with_score = faiss_index.similarity_search_with_score(query, k=3)
    for i, (doc, score) in enumerate(results_with_score, 1):
        print(f"\nResult {i}:")
        print(f"Score: {score:.4f}")
        print("Content:")
        print(doc.page_content)


#  retrieve relevant text chunks from a Chroma vector store and uses them to answer a query using LLM.
def retrieval_from_chrome_store_llm():
    texts_blocks = []

    # Load file
    unstructured_word_document_loader = UnstructuredWordDocumentLoader("01_Foundation_of_Retrieval_Augmented_Generation/4 Dogs.docx")
    word_documents = unstructured_word_document_loader.load()

    # splitting documents
    recursive_character_text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,  # max characters (≈ 120150 tokens) per chunk
        chunk_overlap=50,  # characters of overlap to preserve context
        separators=["\n\n", "\n", ".", " ", ""],  # split on these char
    )
    word_document_chunks = recursive_character_text_splitter.split_documents(word_documents)

    for chunk in range(len(word_document_chunks)):
        content = word_document_chunks[chunk].page_content
        texts_blocks.append(content)

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
    retrieved_docs = vector_store.similarity_search(query, k=3)
    # Retrieve relevant documents(top 3 chunks), This will find the most relevant text chunks for the given query. Adjust 'k' to retrieve more or fewer documents as needed.
    context = "\n\n".join([doc.page_content for doc in retrieved_docs])
    # Create a prompt template, This template will format the context and question for the LLM.
    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template="""
You are an expert assistant. Use the context below to answer the 
question from context.
Context:
{context}
Question:
{question}
Answer:
"""
    )
    # Load the LLM model
    llm = ChatOllama(model="llama3.2:3b", temperature=0.3)
    # Create Runnable pipeline
    parser = StrOutputParser()
    rag_chain = prompt | llm | parser
    # Invoke chain
    answer = rag_chain.invoke({"context": context, "question": query})
    # Print the Query and the answer generated by the LLM based on the retrieved context.
    print("Query:", query)
    print("Answer:", answer)



# Similarity search with metadata filtering using LangChain and FAISS:

def metadata_filtering_using_langChain_faiss():
    raw_docs = [
        {
            "text": "In RAG LangChain supports various vector stores including FAISS and Chroma.",
            "metadata": {"source": "content1", "category": "LangChain"}
        },
        {
            "text": "In RAG LangChain is used to build RAG applications.",
            "metadata": {"source": "content2", "category": "LangChain"}
        },
        {
            "text": "In RAG FAISS is a library for efficient similarity search.",
            "metadata": {"source": "content3", "category": "FAISS"}
        },
    ]
    raw_documents = [Document(page_content=raw_doc["text"], metadata=raw_doc["metadata"]) for raw_doc in raw_docs]
    print(raw_documents)
    character_text_splitter = CharacterTextSplitter(chunk_size=300, chunk_overlap=50)
    raw_doc_chunk = character_text_splitter.split_documents(raw_documents)
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    faiss_index = FAISS.from_documents(raw_doc_chunk, embeddings)
    query = "What is RAG?"
    results = faiss_index.similarity_search(query= query, k=5, filter={"category": "LangChain"})
    print("\nFiltered Similarity Search Results:")
    for i, doc in enumerate(results, 1):
        print(f"\nResult {i}:")
        print(f"Source: {doc.metadata.get('source')}")
        print(f"Category: {doc.metadata.get('category')}")
        print(f"Content: {doc.page_content}")


if __name__ == "__main__":
    #retrieval_from_chrome_store()
    #retrieval_from_faiss_store()
    #retrieval_from_chrome_store_llm()
    metadata_filtering_using_langChain_faiss()