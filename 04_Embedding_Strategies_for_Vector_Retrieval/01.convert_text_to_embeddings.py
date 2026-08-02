from langchain_community.document_loaders import PyPDFLoader
from langchain_huggingface import HuggingFaceEmbeddings
import warnings

from langchain_text_splitters import RecursiveCharacterTextSplitter

warnings.filterwarnings("ignore", category=FutureWarning, module="torch")

def get_convert_text_to_embeddings():
    py_pdf_loader = PyPDFLoader("/home/shiva/PycharmProjects/mathematics_zero_to_hero/Mudra_Yoga-_Mudras__Yoga_in_your_Hands.pdf")
    pdf_pages = py_pdf_loader.load()
    recursive_character_text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=0)
    content_chunk = recursive_character_text_splitter.split_documents(pdf_pages)
    final_text = ""
    for i, chunk in enumerate(content_chunk):
        print(f"chunk{i}: {chunk.page_content}")
        final_text = final_text +" "+ chunk.page_content
    hugging_face_embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    embeddings= hugging_face_embeddings.embed_query(final_text)
    print(f"embeddings length : {len(embeddings)}")
    print(embeddings)



if __name__ == "__main__":
    get_convert_text_to_embeddings()
