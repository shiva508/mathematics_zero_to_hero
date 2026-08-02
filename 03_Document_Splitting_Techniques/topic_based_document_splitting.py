from sentence_transformers import SentenceTransformer, util
import numpy as np
import warnings
warnings.filterwarnings("ignore", category=FutureWarning, module="torch")

def get_topic_based_document_splitting():
    # 1. Initialize the SentenceTransformer model, This model will be used to encode sentences into embeddings
    model = SentenceTransformer("all-MiniLM-L6-v2")

    # 2. Sample text to be split into topic-based chunks, This text contains multiple topics that we want to identify and split
    text = """
    LangChain is a powerful framework for working with large language 
    models.
    It provides tools for loading documents, creating embeddings, and 
    building retrieval pipelines.
    You can integrate it with FAISS, Chroma, and other vector stores.
    Transformers are deep learning models that understand language context.
    Popular models include BERT, GPT, and T5.
    They are used for text generation, classification, and summarization.
    Python is a popular programming language.
    It is used in machine learning, web development, and automation.
    Python supports libraries like Pandas, NumPy, and Scikit-learn.
    """

    # 3. Split text into sentences, This is a simple split by new lines, but you can use more sophisticated methods if needed
    sentences = [s.strip() for s in text.strip().split("\n") if s.strip()]
    # 4. Encode sentences to get embeddings, Each sentence is converted into a vector representation This allows us to measure similarity between sentences
    embedding =  model.encode(sentences)
    # 5. Calculate cosine similarity matrix, This will give us a matrix where each cell (i, j) is the similarity between
    similarity_matrix = util.cos_sim(embedding, embedding).numpy()
    # 6. Cluster sentences based on similarity Here we will use a simple heuristic to group sentences into 3 topics
    clusters = [[] for _ in range(4)]
    assigned = set()
    # 7. Define centers for each topic based on sentence indices
    centers = [0, 3, 6, 9]
    # 8. We iterate over each center and assign sentences that are similar enough
    for i, center in enumerate(centers):
        for j in range(len(sentences)):
            if j is not assigned and similarity_matrix[center][j] > 0.5:
                clusters[i].append(sentences[j])
                assigned.add(j)
    print(clusters)
    # 9. Create topic-based chunks # Each cluster represents a topic, and we join sentences in each  # cluster to form a chunk
    topic_chunks = [" ".join(cluster) for cluster in clusters]

    # 10. Print the topic-based chunks
    for idx, chunk in enumerate(topic_chunks, 1):
        print(f"--- Topic Chunk {idx} ---\n{chunk}\n")

if __name__ == "__main__":
    get_topic_based_document_splitting()