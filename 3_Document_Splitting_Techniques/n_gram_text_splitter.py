from typing import List, Any

from langchain_core.documents import Document
from langchain_text_splitters import TextSplitter


class NGramTextSplitter(TextSplitter):
    # Initialize with n-gram size and overlap
    def __init__(self, n: int=10, overlap: int=2):
        super().__init__()
        self.n = n
        self.overlap = overlap

    # Split text into n-grams with specified overlap
    def split_text(self, text: str) -> List[str]:
        words = text.split()
        chunks = []
        step = self.n - self.overlap
        for i in range(0, (len(words) - self.n + 1), step):
            chunk = " ".join(words[i:i + self.n])
            chunks.append(chunk)
        return chunks

    # Create LangChain-style documents from the text
    def create_documents(self, texts: List[str], metadata: List[dict[Any,Any]]=None)-> List[Document]:
        documents = []
        metadata = metadata or [ {} for _ in texts]
        for text, meta in zip(texts, metadata):
            splits = self.split_text(text)
            for split in splits:
                documents.append(Document(page_content=split, metadata=meta))
        return documents


if __name__ == "__main__":
    texts = []

    sample_text = (
        """
        Retrieval Augmented Generation (RAG) is an architecture that 
    combines
    the ability of large language models (LLMs) with a retrieval system to 
    enhance
    the factual accuracy, contextual relevance, and quality of generated 
    response
    against the query raised by user to a RAG system.
    """
    )
    splitter = NGramTextSplitter(n=8, overlap=0)
    docs = splitter.create_documents([sample_text])
    for i, doc in enumerate(docs, 1):
        print(f"\n--- Chunk {i} ---\n{doc.page_content}")
