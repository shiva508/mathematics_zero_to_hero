import json

from langchain_core.documents import Document


def get_custom_separator_splitting():
    text = "START This is first chunk. END START This is a second chunk. END"
    chunks = text.split("START")
    documents = []
    for chunk in chunks:
        if "END" in chunk:
            cleaned_chunk =  chunk.split("END")[0].strip()
            documents.append(Document(page_content=cleaned_chunk))

    # 3. Print the resulting Document objects, Each Document represents a chunk of text between the custom keywords.
    for i, doc in enumerate(documents, 1):
        print(f"[Chunk {i}] {doc.page_content}")


def get_json_splitter():
    json_lines = """
        {"id": 1, "text": "First entry"}
        {"id": 2, "text": "Second entry"}
    """
    chunks = []
    for json_line in json_lines.strip().splitlines():
        item = json.loads(json_line)
        chunks.append(Document(page_content=item["text"], metadata={"id": item["id"]}))

    for doc in chunks:
        print(f"[ID {doc.metadata['id']}] {doc.page_content}")

if __name__ == "__main__":
    #get_custom_separator_splitting()
    get_json_splitter()


