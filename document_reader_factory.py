from typing import List

from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document


def get_pdf_documents(file_path:str)-> List[Document]:
    print("Loading PDFs...")
    py_pdf_loader = PyPDFLoader(file_path)
    return py_pdf_loader.load()