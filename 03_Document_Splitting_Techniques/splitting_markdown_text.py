import re
import textwrap
def get_splitting_markdown_text():
    markdown_text = textwrap.dedent("""
    # RAG with Python
    This explains use of RAG
    ## What is RAG?
    RAG (Retrieval-Augmented Generation) enhances LLMs by injecting external information 
    into prompts.
    ## Components
    Components of RAG
    ### Retriever
    This fetches relevant documents from a knowledge base.
    ### Generator
    The LLM uses retrieved docs to answer the query.
    ## Use Cases
    - Customer support bots
    - Legal document assistants
    - Research assistants
    """)
    pattern = r'(?=^#{2,3}\s+)'
    sentences = re.split(pattern, markdown_text, re.MULTILINE)

    for i, chunk in enumerate(sentences, 1):
        cleaned = chunk.strip()
        # 4. Only print non-empty chunks
        if cleaned:
            print(f"\n--- Chunk {i} ---\n{cleaned}")



if __name__ == "__main__":
    get_splitting_markdown_text()
