from langchain_community.document_loaders import TextLoader
from langchain_core.documents import Document
import nltk
from nltk.corpus import stopwords
import re
nltk.download("stopwords")

def get_preprocessing_and_text_normalization():
    txt_file_path = "/home/shiva/PycharmProjects/mathematics_zero_to_hero/02_Document_Loaders_For_RAG_Pipelines/RAG.txt"
    text_loader = TextLoader(txt_file_path)
    raw_docs = text_loader.load()
    stop_words = set(stopwords.words('english'))
    processed_docs = []
    for raw_doc in raw_docs:
        cleaned = preprocess(raw_doc.page_content, stop_words)
        processed_doc = Document(page_content=cleaned, metadata=raw_doc.metadata)
        processed_docs.append(processed_doc)

    for raw_doc in processed_docs:
        print(raw_doc.page_content)



def preprocess(text, stop_words):
    text = text.lower()
    words = text.split()
    filtered = [word for word in words if word not in  stop_words]
    text = " ".join(filtered)
    # Normalizing white spaces
    text = re.sub(r'\s+', ' ', text).strip()
    return text

if __name__ == "__main__":
    get_preprocessing_and_text_normalization()
