from langchain_community.document_loaders import TextLoader, UnstructuredWordDocumentLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter

def create_embeddings():
    # Load model
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    # Text input
    texts = [
        "Retrieval Augmented Generation (RAG) is an architecture that combines the ability of large language models (LLMs) with a retrieval system.",
        "Traditional generative models rely solely on internal parameters f			or producing responses.",
        "RAG mitigates this by augmenting the generation process with real-time retrieval from external knowledge sources."
    ]
    # embedding
    embeddings = embedding_model.embed_documents(texts)
    for i, vector in enumerate(embeddings):
        print(f"--- Embedding {i + 1} (first 5 dims) ---")
        print(vector[:5])  # Show only first 5 dimensions for brevity
        print()
def get_embeddings_huggingface():
    # Text to created embedding
    texts = [
        "Retrieval Augmented Generation (RAG) is an architecture that combines the ability of large language models (LLMs) with a retrieval system to enhance the factual accuracy.",
        "Traditional generative models rely solely on internal parameters for producing responses, which limits their ability to provide up-to-date or domain-specific knowledge.",
        "RAG mitigates this by augmenting the generation process with real-time retrieval from external knowledge sources.",
        "Traditional generative models are now mostly replaced or augmented by deep learning-based transformer models, which offer greater accuracy, coherence, and scalability."
    ]
    # Load model
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    # Create a FAISS index from the embeddings, This will convert the list of texts into their corresponding vector
    vector_store = FAISS.from_texts(texts, embedding=embedding_model)
    query = "benefit of using RAG?"
    results = vector_store.similarity_search(query, k=3)  # top 3 matches
    for result in results:
        print(result.page_content)

def build_embeddings_huggingface_txt_file():
    texts = []
    # Load doc
    unstructured_word_document_loader = UnstructuredWordDocumentLoader("4 Dogs.docx")
    word_documents = unstructured_word_document_loader.load()

    #Split
    recursive_character_text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,  # max characters (≈ 120150 tokens) per chunk
        chunk_overlap=50,  # characters of overlap to preserve context
        separators=["\n\n", "\n", ".", " ", ""],  # split on these char
    )
    word_documents_chunks = recursive_character_text_splitter.split_documents(word_documents)

    # Gathering
    for chunk in range(len(word_documents_chunks)):
        print(word_documents_chunks[chunk].page_content)
        texts.append(word_documents_chunks[chunk].page_content)
    print(len(texts))

    # Loading model
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    # Create a FAISS index from the embeddings, This will convert the list of texts into their corresponding vector
    vector_store = FAISS.from_texts(texts, embedding=embedding_model)
    query = "What was the time?"
    results = vector_store.similarity_search(query, k=2)
    for result in results:
        print(result.page_content)

if __name__ == "__main__":
    create_embeddings()
    #get_embeddings_huggingface()
    #build_embeddings_huggingface_txt_file()