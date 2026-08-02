from sentence_transformers import SentenceTransformer
import warnings
warnings.filterwarnings("ignore", category=FutureWarning, module="torch")

def get_embedding_models_for_offline_use():

    # Load an offline, pre-trained SentenceTransformer model
    sentence_transformer = SentenceTransformer('all-MiniLM-L6-v2')

    # Sample texts to generate embeddings
    texts = [
        "LangChain enables RAG pipelines.",
        "Embedding converts text into vectors.",
        "You can run models offline with SentenceTransformers."
    ]

    # Generate embeddings for sample texts The model.encode method processes the texts and returns their embeddings
    embeddings = sentence_transformer.encode(texts)

    # Print the generated embeddings
    for i, emb in enumerate(embeddings):
        print(f"\nText {i + 1}: {texts[i]}")
        print(f"Embedding shape: {emb.shape}")
        print(f"First 5 dimensions: {emb[:5]}")


if __name__ == "__main__":
    get_embedding_models_for_offline_use()