import re

def get_regex_based_splitting():

    # 1. Sample text to be split into sections based on headers. This text contains multiple sections that we want to identify and  split
    text = """## What is RAG?
        RAG stands for Retrieval-Augmented Generation. It enhances language 
        models by retrieving relevant information from external sources before 
        generating responses.
        ## Components of RAG
        - Retriever: Finds relevant documents.
        - Generator: Uses the retrieved context to generate answers.
        - Vector Store: Stores document embeddings for efficient search.
        ## Benefits
        - Improved accuracy
        - Current information access
        - Cost-effective context handling
        """
    # 2. Define a regex pattern to match headers. This pattern matches lines that start with '## ' followed by the header text
    pattern = r"^\s*##\s+(.*)$"
    sections = re.split(pattern, text, flags=re.MULTILINE)
    # 3. Remove empty chunks,Create chunks by pairing headers with their content This will create a list of chunks where each chunk contains a  header and its corresponding content
    filtered_sections = [section for section in sections if len(section)>0]
    chunks = []
    for i in range(0, len(filtered_sections), 2):
        header = filtered_sections[i].strip()
        content = filtered_sections[i + 1].strip()
        chunks.append(f"{header}\n{content}")
    # 4. Print the resulting chunks, Each chunk is printed with a header indicating its index
    for i, chunk in enumerate(chunks, 1):
        print(f"\n--- Chunk {i} ---\n{chunk}")

if __name__ == "__main__":
    get_regex_based_splitting()
