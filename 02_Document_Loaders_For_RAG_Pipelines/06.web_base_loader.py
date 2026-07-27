from langchain_community.document_loaders import WebBaseLoader


def get_web_base_loader():
    url = "https://www.agentsfordata.com/json/sample"
    web_base_loader = WebBaseLoader(url)
    web_pages = web_base_loader.load()
    for web_page in range(len(web_pages)):
        print(web_pages[web_page])


if __name__ == "__main__":
    get_web_base_loader()