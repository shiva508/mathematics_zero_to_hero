from langchain_community.document_loaders import BSHTMLLoader


def get_bshtml_loader():
    html_file_path = "/home/shiva/PycharmProjects/mathematics_zero_to_hero/02_Document_Loaders_For_RAG_Pipelines/sample_html"
    bshtml_loader = BSHTMLLoader(html_file_path)
    bshtml_files = bshtml_loader.load()
    for bshtml_file in range(len(bshtml_files)):
        print(bshtml_files[bshtml_file])

if __name__ == "__main__":
    get_bshtml_loader()