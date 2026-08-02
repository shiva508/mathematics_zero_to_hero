from langchain_community.document_loaders import PyPDFLoader
from transformers import AutoTokenizer, AutoModel
import torch
import warnings
warnings.filterwarnings("ignore", category=FutureWarning, module="torch")

def get_embed_a_list_of_documents_into_vectors():


    # Load the pre-trained model and tokenizer
    # The model 'sentence-transformers/all-MiniLM-L6-#v2' is suitable for generating embeddings.
    # You can replace it with any other model available in HuggingFace.
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    auto_model = AutoModel.from_pretrained(model_name)

    # Define a list of documents to be embedded
    # Each document is a string that will be transformed into a vector representation.
    py_pdf_loader = PyPDFLoader(
        "/home/shiva/PycharmProjects/mathematics_zero_to_hero/Mudra_Yoga-_Mudras__Yoga_in_your_Hands.pdf")
    pdf_pages = py_pdf_loader.load()
    documents = []
    for page in pdf_pages:
        documents.append(page.page_content)

    # Generate embeddings for the list of documents
    # The embed_documents function is called with the list of documents to get their embeddings.
    embeddings = embed_documents(documents, tokenizer, auto_model)

    # Print the resulting embeddings
    # Each embedding is a vector representation of the corresponding  # document
    for i, vec in enumerate(embeddings):
        print(f"Document {i + 1} vector (first 5 dims): {vec[:5]}")

# Tokenize the documents The tokenizer converts the list of documents into a format suitable for the model.
def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output.last_hidden_state
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size())
    return (token_embeddings * input_mask_expanded).sum(1)/input_mask_expanded.sum(1)

# Embed the documents
def embed_documents(docs, tokenizer, auto_model):
    encoded = tokenizer(docs, padding=True, truncation=True, return_tensors='pt')
    with torch.no_grad():
        output = auto_model(**encoded)
    return mean_pooling(output, encoded['attention_mask'])


if __name__ == "__main__":
    get_embed_a_list_of_documents_into_vectors()