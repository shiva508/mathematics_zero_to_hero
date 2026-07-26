from langchain_community.document_loaders import CSVLoader

# load a CSV file using LangChain's CSVLoader

def get_csv_file_loader():
    csv_loader = CSVLoader("/home/shiva/PycharmProjects/mathematics_zero_to_hero/02_Document_Loaders_For_RAG_Pipelines/currency.csv")
    csv_docs = csv_loader.load()
    for doc in range(len(csv_docs)):
        print(csv_docs[doc].page_content)


if __name__ == "__main__":
    get_csv_file_loader()