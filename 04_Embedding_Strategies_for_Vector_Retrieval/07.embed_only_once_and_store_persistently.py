
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langchain_community. vectorstores import FAISS
import os
import warnings

from langchain_text_splitters import RecursiveCharacterTextSplitter

warnings.filterwarnings("ignore", category=FutureWarning, module="torch")

def get_embed_only_once_and_store_persistently():
    # Create a large document and split it into chunks This simulates a large document by repeating a phrase multiple times.
    large_text = "Generative models laid the foundation for today’s LLMs.\n" * 2

    # Split the large text into smaller chunks for embedding, This is necessary because large documents can be too big for embedding models.
    recursive_character_text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=50)
    chunks = recursive_character_text_splitter.split_text(large_text)
    documents = [Document(page_content=chunk) for chunk in chunks]

    # Initialize the embedding model, This uses the HuggingFaceEmbeddings class to create embeddings for the text chunks.
    embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vector_store = FAISS.from_documents(documents, embedding=embedding_model)

    # Save the FAISS index to disk, This allows reusing the stored embeddings later without recomputation.
    faiss_index_path = "embed_faiss_index"
    vector_store.save_local(faiss_index_path)
    print("Embeddings created and saved to disk.")

def load_local_model():

    # Initialize the embedding model, This uses the same embedding model as in the previous script to ensure compatibility.
    embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    # Load the FAISS index from the saved path, This assumes the index was saved in the previous step.
    faiss_index_path = "embed_faiss_index"
    vectorstore = FAISS.load_local(faiss_index_path, embedding_model, allow_dangerous_deserialization=True)

    # 3. Perform a similarity search, This query will find documents similar to the input text based on their embeddings.
    results = vectorstore.similarity_search("What does Generative models do?", k=1)
    print("\nBest Match:", results[0].page_content)
if __name__ == "__main__":
    #get_embed_only_once_and_store_persistently()
    load_local_model()

