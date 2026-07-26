import json

from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader, TextLoader, UnstructuredWordDocumentLoader
import nltk
from langchain_text_splitters import NLTKTextSplitter
from langchain_community.document_loaders import TextLoader
import  json
from langchain_text_splitters import CharacterTextSplitter, RecursiveCharacterTextSplitter, TokenTextSplitter

# LOADING PDF
def load_pdf_document():
    pdf_loader = PyPDFLoader("../Mudra_Yoga-_Mudras__Yoga_in_your_Hands.pdf")
    pdf_doc = pdf_loader.load()
    print("Loaded " + str(len(pdf_doc)) + " documents")
    for doc in range(len(pdf_doc)):
        print(pdf_doc[doc].page_content)
        print("=======")

# LOAD .docx and split text
def split_document():
    dex_doc_loader = UnstructuredWordDocumentLoader("4 Dogs.docx")
    dex_docs = dex_doc_loader.load()
    print("Loaded " + str(len(dex_docs)) + " documents")
    splitter = RecursiveCharacterTextSplitter(chunk_size=300,  # max characters (≈ 120150 tokens) per chunk
                                   chunk_overlap=50,  # characters of overlap to preserve context
                                   separators=["\n\n", "\n", ".", " ", ""])
    chunks = splitter.split_documents(dex_docs)
    print(len(chunks))
    for chunk in range(len(chunks)):
        print(chunks[chunk].page_content)

# Split plain text
def token_text_splitter():
    text = """ Retrieval Augmented Generation (RAG) is an architecture that combines the ability of large language models (LLMs) with a retrieval system to enhance the factual accuracy, contextual relevance, and quality of generated response against the query raised by user to a RAG system."""
    text_splitter = TokenTextSplitter(chunk_size=30, chunk_overlap=10)
    text_tokens = text_splitter.split_text(text)
    for token in range(len(text_tokens)):
        print(f"Chunk {token}:{text_tokens[token]}")

# Load .txt file and split
def get_text_loader():
    text_loader = TextLoader("RAG.txt")
    text_docs = text_loader.load()
    character_text_splitter = CharacterTextSplitter(separator="\n",       # Splits at newline characters
                                                    chunk_size=300,       # Max characters per chunk
                                                    chunk_overlap=50,     # Overlap to preserve context
                                                    length_function=len   # Optional, default is len()
                                                    )
    txt_chunks = character_text_splitter.split_documents(text_docs)
    for chunk in range(len(txt_chunks)):
        print(f"Chunk {chunk}: {txt_chunks[chunk].page_content}")

def get_nltk_text_splitter():
    nltk.download('punkt')
    text_loader = TextLoader("RAG.txt")
    text_docs = text_loader.load()
    nltk_text_splitter = NLTKTextSplitter(
                                            chunk_size=300,        # Max characters per chunk
                                            chunk_overlap=50       # Overlap between chunks
                                          )
    nltk_text_blocks = nltk_text_splitter.split_documents(text_docs)
    for chunk in range(len(nltk_text_blocks)):
        print(f"Chunk {chunk}: {nltk_text_blocks[chunk].page_content}")

if __name__ == "__main__":
    #load_pdf_document()
    #split_document()
    #token_text_splitter()
    #get_text_loader()
    get_nltk_text_splitter()