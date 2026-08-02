from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from typing import List
import warnings

from transformers import pipeline

warnings.filterwarnings("ignore", category=FutureWarning, module="torch")

def get_embed_only_summaries():
    documents = [
        Document(page_content="""
    LangChain is an open-source framework that helps developers create 
    applications powered by large language models (LLMs).
    It provides components and integrations to connect LLMs to external 
    data, manage memory, and create agents.
    """),
        Document(page_content="""
    FAISS (Facebook AI Similarity Search) is a library that enables fast 
    similarity search and clustering of dense vectors.
    It's widely used in AI applications that need to search through 
    vectorized text or image data efficiently.
    """),
        Document(page_content="""
    Transformers are a type of deep learning model that revolutionized NLP.
    Based on self-attention, they allow for parallel processing and improved performance 
    in text classification, translation, and more.
    """)
    ]

    # Initialize the summarization pipeline This uses a pre-#rained model to generate summaries of the documents.
    summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

    # Generate summaries for the documents, This will create concise summaries for each document
    summaries = generate_summaries(documents, summarizer)


    # Create a FAISS vector store from the summaries ,The FAISS vector store will allow for efficient similarity search on the embedded summaries.
    embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vector_store = FAISS.from_texts(texts=summaries, embedding=embedding_model, metadatas=[doc.metadata for doc in documents])

    # Perform semantic search on the vector store This query will find documents similar to the input text based on their embeddings.
    query = "What are transformers used for?"
    results = vector_store.similarity_search(query, k=1)
    # 6. Print the results with summaries
    print("\nBest Match (from Summary):", results[0].page_content)



def generate_summaries(docs: List[Document], summarizer) -> List[str]:
    summaries = []
    for doc in docs:
        summary = summarizer(doc.page_content, max_length=50, min_length=20, do_sample=False)[0]['summary_text']
        summaries.append(summary)
    return summaries

if __name__ == "__main__":
    import transformers

    print(transformers.__version__)
    get_embed_only_summaries()