from bs4 import BeautifulSoup
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


def get_html_tag_based_splitting():
    html_doc = """
    <html>
      <body>
        <h1>RAG Pipeline</h1>
        <p>Load → Split → Embed → Retrieve → Generate</p>
        <p>Used in chatbots, document search, and more.</p>
      </body>
    </html>
    """
    # 2. Parse the HTML and extract text from specific tags, Here, we will extract text from <h1> and <p> tags.
    beautiful_soup = BeautifulSoup(html_doc, 'html.parser')
    paragraphs = beautiful_soup.find_all(['h1','p'])
    documents = [Document(page_content=paragraph.get_text() ) for paragraph in paragraphs]
    recursive_character_text_splitter = RecursiveCharacterTextSplitter(chunk_size=50, chunk_overlap=10)
    chunks = recursive_character_text_splitter.split_documents(documents)
    for i, chunk in enumerate(chunks):
        print(chunk.page_content)



if __name__ == '__main__':
    get_html_tag_based_splitting()