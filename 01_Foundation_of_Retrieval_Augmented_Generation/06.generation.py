# simple RAG pipeline using LangChain and Ollama. It retrieves relevant text chunks from a Chroma vector store and uses them to answer a query.
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_ollama import embeddings, ChatOllama
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pypdf import PdfReader


def langChain_ollama_chroma():
    pdf_reader = PyPDFLoader("/home/shiva/PycharmProjects/mathematics_zero_to_hero/Mudra_Yoga-_Mudras__Yoga_in_your_Hands.pdf")
    pdf_documents = pdf_reader.load()
    recursive_character_text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    pdf_document_chunks = recursive_character_text_splitter.split_documents(pdf_documents)
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    chroma_vector_store = Chroma.from_documents(
                                        documents=pdf_document_chunks,
                                        embedding=embedding_model,
                                        persist_directory="chroma_vector_store")
    query = "What is the document about?"
    vector_search_results = chroma_vector_store.similarity_search(query= query, k=5)
    context = "\n\n".join([vector_search.page_content for vector_search in vector_search_results])
    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template="""
    You are an AI assistant. Use the context below to answer the question 
    accurately.
    Context:
    {context}
    Question:
    {question}
    Answer:
    """)
    llm = ChatOllama(model="llama3.2:3b", temperature=0.3)
    rag_chain = prompt | llm
    answer = rag_chain.invoke({"context": context, "question": query})
    print("Question:", query)
    print("Answer:", answer.content)



if __name__ == "__main__":
    langChain_ollama_chroma()