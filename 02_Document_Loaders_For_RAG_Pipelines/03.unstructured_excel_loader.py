from langchain_community.document_loaders import UnstructuredExcelLoader


def get_unstructured_excel_loader():
    excel_file_path = "/home/shiva/PycharmProjects/mathematics_zero_to_hero/02_Document_Loaders_For_RAG_Pipelines/my-loans-2026.xlsx"
    unstructured_excel_loader = UnstructuredExcelLoader(excel_file_path)
    excel_sheets  = unstructured_excel_loader.load()
    for excel_sheet in range(len(excel_sheets)):
        print(excel_sheets[excel_sheet])


if __name__ == "__main__":
    get_unstructured_excel_loader()