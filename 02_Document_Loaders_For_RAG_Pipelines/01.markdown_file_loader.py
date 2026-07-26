from langchain_community.document_loaders import UnstructuredMarkdownLoader

# Load a Markdown file using LangChain's UnstructuredMarkdownLoader
def get_unstructured_markdown_loader():
    mark_down_file_path = "/home/shiva/PycharmProjects/mathematics_zero_to_hero/02_Document_Loaders_For_RAG_Pipelines/document_loader_flow.md"
    unstructured_markdown_loader = UnstructuredMarkdownLoader(file_path=mark_down_file_path)
    markdown_docs = unstructured_markdown_loader.load()
    for markdown_doc in range(len(markdown_docs)):
        print(markdown_docs[markdown_doc].page_content)


if __name__ == '__main__':
    get_unstructured_markdown_loader()
