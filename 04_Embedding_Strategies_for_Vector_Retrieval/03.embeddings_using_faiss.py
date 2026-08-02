from langchain_community.document_loaders import PyPDFLoader
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import warnings
warnings.filterwarnings("ignore", category=FutureWarning, module="torch")


def get_embeddings_using_faiss():
    # Load the pre-trained model
    sentence_transformer = SentenceTransformer("all-MiniLM-L6-v2")

    # 2. Define a list of documents to be embedded Each document is a string that will be transformed into a vector representation.
    py_pdf_loader = PyPDFLoader("/home/shiva/PycharmProjects/mathematics_zero_to_hero/Mudra_Yoga-_Mudras__Yoga_in_your_Hands.pdf")
    pdf_pages = py_pdf_loader.load()
    documents = []
    for page in pdf_pages:
        documents.append(page.page_content)

    # Embed the documents The model.encode method generates embeddings for the list of documents.
    embeddings = sentence_transformer.encode(documents, convert_to_numpy=True)

    # Create a FAISS index The index will store the embeddings and allow for efficient similarity search.
    dimension = embeddings.shape[1]
    faiss_index = faiss.IndexFlatL2(dimension)

    # Add embeddings to the FAISS index The embeddings are added to the index for later retrieval.
    faiss_index.add(embeddings)

    # Example query to search the FAISS index
    query = "Mudra for hair"
    query_vector = sentence_transformer.encode([query])

    # Search the index The search method retrieves the k nearest neighbors for the query vector.
    distances, indices = faiss_index.search(query_vector, 2)

    # Print the results  The results show the documents that are most similar to the query along with their distances.
    print(f"\nQuery: {query}")
    for i, idx in enumerate(indices[0]):
        print(f"Match {i + 1}: '{documents[idx]}' (distance: {distances[0][i]:.4f})")


if __name__ == "__main__":
    get_embeddings_using_faiss()



