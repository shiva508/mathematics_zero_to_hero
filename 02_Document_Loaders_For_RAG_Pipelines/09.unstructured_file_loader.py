from langchain_community.document_loaders import UnstructuredFileLoader


def get_unstructured_file_loader():
    file_path = "/home/shiva/PycharmProjects/mathematics_zero_to_hero/02_Document_Loaders_For_RAG_Pipelines/RAG.txt"
    excel_file_path = "/home/shiva/PycharmProjects/mathematics_zero_to_hero/02_Document_Loaders_For_RAG_Pipelines/my-loans-2026.xlsx"
    unstructured_file_loader = UnstructuredFileLoader(excel_file_path)
    files_data = unstructured_file_loader.load()
    for file in files_data:
        print(file)



if __name__ == "__main__":
    get_unstructured_file_loader()