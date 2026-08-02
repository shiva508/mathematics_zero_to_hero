from langchain_community.document_loaders import PyPDFLoader


def get_page_based_splitting():
    py_pdf_loader = PyPDFLoader("/home/shiva/PycharmProjects/mathematics_zero_to_hero/Mudra_Yoga-_Mudras__Yoga_in_your_Hands.pdf")
    pdf_pages = py_pdf_loader.load()
    for page in pdf_pages:
        print(page)


if __name__ == "__main__":
    get_page_based_splitting()
