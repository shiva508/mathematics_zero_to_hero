from langchain_core.document_loaders import BaseLoader
from langchain_core.documents import Document

class CustomTextLoader(BaseLoader):
    def __init__(self, file_path: str, metadata: dict = None):
        self.file_path = file_path
        self.metadata = metadata or {}

    def load(self):
        with open(self.file_path, "r") as f:
            text = f.read()
        return [Document(page_content=text, metadata=self.metadata)]

if __name__ == "__main__":
    custom = CustomTextLoader(file_path="/home/shiva/PycharmProjects/mathematics_zero_to_hero/02_Document_Loaders_For_RAG_Pipelines/RAG.txt")
    print(custom.load())