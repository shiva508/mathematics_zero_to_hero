import os.path
from concurrent.futures.thread import ThreadPoolExecutor

from langchain_community.document_loaders import PyPDFLoader, TextLoader, UnstructuredWordDocumentLoader, \
    UnstructuredExcelLoader, BSHTMLLoader, JSONLoader, CSVLoader, UnstructuredFileLoader

# file loader
def get_file_loader(file_path):
    file_formate = os.path.splitext(file_path)[1].lower()
    if file_formate == ".pdf":
        return PyPDFLoader(file_path)
    elif file_formate == ".txt":
        return TextLoader(file_path)
    elif file_formate in [".docx", ".doc"]:
        return UnstructuredWordDocumentLoader(file_path)
    elif file_formate == ".xlsx":
        return UnstructuredExcelLoader(file_path)
    elif file_formate == ".html":
        return BSHTMLLoader(file_path)
    elif file_formate in [".json",".JSON"]:
        return JSONLoader(file_path= file_path,
                          jq_schema=".",
                          text_content=False)
    elif file_formate == ".csv":
        return CSVLoader(file_path= file_path)
    else:
        return UnstructuredFileLoader(file_path)



def get_documents_parallel(file_paths, max_workers=4):
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(get_file_loader(file_path).load()): file_path
            for file_path in file_paths
        }


def get_files_paths(directory):
    supported_formats = [".pdf", ".txt", ".doc", ".json", ".JSON", ".csv"]
    for file in os.listdir(directory):
        if os.path.splitext(file)[1] in supported_formats:
            print(file)


if __name__ == "__main__":
    get_files_paths("/home/shiva/PycharmProjects/mathematics_zero_to_hero/02_Document_Loaders_For_RAG_Pipelines")