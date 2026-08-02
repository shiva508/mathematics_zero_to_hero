from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
import warnings
warnings.filterwarnings("ignore", category=FutureWarning, module="torch")

def get_embedding_and_metadata_for_better_filtering():
    # Create documents with metadata These documents will be used to demonstrate metadata filtering in the FAISS vector store.
    docs = [
        Document(page_content="LangChain enables LLM applications.",
                 metadata={"source": "docs/langchain.md", "topic": "LangChain"}),
        Document(page_content="Hugging Face provides transformer models.", metadata={"source":
                                                                        "docs/huggingface.md",
                                                                                     "topic": "Transformers"}),
        Document(page_content="OpenAI offers GPT models for developers.", metadata={"source":
                                                                                        "docs/openai.md",
                                                                                    "topic": "OpenAI"}),
    ]

    # Initialize the embedding model This uses the HuggingFaceEmbeddings class to create embeddings for the text chunks.
    embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    # Create a FAISS vector store from the documents, The FAISS vector store will allow for efficient similarity search on the embedded documents.
    vector_store = FAISS.from_documents(documents=docs,embedding=embedding_model)

    # Run a similarity search to retrieve the top-k most similar chunks for the query.

    query = "How to use transformer models?"
    results = vector_store.similarity_search(query=query, k=2)

    for doc in results:
        print(doc.page_content)
        print(doc.metadata["source"])
        print(doc.metadata["topic"])



if __name__ == "__main__":
    get_embedding_and_metadata_for_better_filtering()



