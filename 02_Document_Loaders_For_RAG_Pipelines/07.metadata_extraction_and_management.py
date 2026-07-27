from langchain_community.document_loaders import TextLoader


def get_load_txt_file():
    txt_file_path = "/home/shiva/PycharmProjects/mathematics_zero_to_hero/02_Document_Loaders_For_RAG_Pipelines/RAG.txt"
    text_loader = TextLoader(txt_file_path)
    raw_docs = text_loader.load()
    custom_docs = []
    for raw_doc in raw_docs:
        raw_doc.metadata["source"] = "local_file"
        raw_doc.metadata["category"] = "tutorial"
        raw_doc.metadata["author"] = "Deepak"
        custom_docs.append(raw_doc)

    for i, doc in enumerate(custom_docs):
        print(f"\n - -- Document {i + 1} - --")
        print("Content:", doc.page_content)
        print("Metadata:", doc.metadata)

if __name__ == "__main__":
    get_load_txt_file()
