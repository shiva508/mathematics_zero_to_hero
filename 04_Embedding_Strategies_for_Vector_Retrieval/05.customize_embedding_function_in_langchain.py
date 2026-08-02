from langchain.embeddings.base import Embeddings
from typing import List
from sentence_transformers import SentenceTransformer
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
import warnings

from document_reader_factory import get_pdf_documents

warnings.filterwarnings("ignore", category=FutureWarning, module="torch")

# Custom embedding class that uses Sentence Transformers, This class implements the LangChain Embeddings interface.
class CustomSentenceTransformerEmbedding(Embeddings):
    def __init__(self, model_name:str="all-MiniLM-L6-v2" ):
        self.model = SentenceTransformer(model_name)

    def embed_documents(self, texts: List[str])-> List[List[float]]:
        return self.model.encode(texts).tolist()

    def embed_query(self, text:str)-> List[float]:
        return self.model.encode([text])[0].tolist()


def get_customize_embedding_function_in_langchain(docs: List[Document]):

    # Create an instance of the custom embedding function, This initializes the SentenceTransformer model for generating embeddings.
    embedding_fn = CustomSentenceTransformerEmbedding(model_name="all-MiniLM-L6-v2")

    # Create a FAISS vector store using the custom embedding function, The vector store will use the embeddings to allow for efficient similarity search.
    vector_store = FAISS.from_documents(docs, embedding_fn)

    # Example query to search the vector store, This query will find documents similar to the input text based on their embeddings.
    #query = "What is LangChain used for?"
    #query = "Where Maha Bandha can be used ?"
    query = "USHAS MUDRA"
    results = vector_store.similarity_search(query, 1)
    for i, doc in enumerate(results):
        print(doc)



if __name__ == "__main__":
    # Define a list of documents to be embedded, Each document is a string that will be transformed into a vector representation.
    file_path = "/home/shiva/PycharmProjects/mathematics_zero_to_hero/Mudra_Yoga-_Mudras__Yoga_in_your_Hands.pdf"
    pdf_docs = get_pdf_documents(file_path)
    #pdf_docs.append(Document(page_content="LangChain is powerful for building RAG."))
    #pdf_docs.append(Document(page_content="Embeddings turn text into vectors."))
    get_customize_embedding_function_in_langchain(pdf_docs)