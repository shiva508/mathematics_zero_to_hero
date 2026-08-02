from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.embeddings.base import Embeddings
from langchain_core.documents import Document
from sentence_transformers import SentenceTransformer
from langchain_community.vectorstores import FAISS
from tqdm import tqdm
import warnings
warnings.filterwarnings("ignore", category=FutureWarning, module="torch")

# 1. Define the embedding model, Using SentenceTransformer for batch processing
class BatchedSentenceTransformerEmbedding(Embeddings):
    def __init__(self, model_name: str= "all-MiniLM-L6-v2", batch_size: int= 32):
        self.model = SentenceTransformer(model_name)
        self.batch_size = batch_size

    def embed_documents(self, texts):
        embeddings = []
        for i in tqdm(range(0, len(texts), self.batch_size), desc="Embedding Batches"):
            batch = texts[i:i + self.batch_size]
            batch_embedding = self.model.encode(batch)
            embeddings.extend(batch_embedding.tolist())
        return embeddings

    def embed_query(self, text):
        return self.model.encode([text])[0]


def get_batch_embedding_of_large_documents_efficiently():
    # Create a large document, Simulating a large document by repeating a smaller text
    large_text = "LangChain is powerful.\n" * 50  # Simulate repetition

    # Split the large document into manageable chunks, RecursiveCharacterTextSplitter ensures that the document is broken into overlapping chunks small enough for the embedding model to handle #efficiently.
    recursive_character_text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=50)
    chunks = recursive_character_text_splitter.split_text(large_text)
    documents = [Document(page_content=chunk) for chunk in chunks]

    # Create the vector store with batched embeddings, Using FAISS for efficient similarity search
    embedding_model = BatchedSentenceTransformerEmbedding()
    vector_store = FAISS.from_documents(documents, embedding=embedding_model)

    # 5. Perform a similarity search, Searching for a specific query in the vector store
    query = "What is LangChain ?"
    result = vector_store.similarity_search(query, k=1)
    for doc in result:
        print(doc)


if __name__ == "__main__":
    get_batch_embedding_of_large_documents_efficiently()