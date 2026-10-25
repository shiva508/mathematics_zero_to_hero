import os
from typing import Optional

from pydantic import BaseModel, Field
from google.adk.agents import LlmAgent
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


# 1. Define the expected JSON structure
class InvoiceDetails(BaseModel):
    awb_no: Optional[str] = Field(
        default=None,
        description="Air Waybill number found in the invoice",
    )
    total_price: Optional[float] = Field(
        default=None,
        description="Total invoice price as a number",
    )


# 2. Define the tool before creating the agent
def data_extraction(filename) -> dict:
    """Extract the text from the commercial invoice PDF.

    Returns:
        A dictionary containing the extracted invoice text.
    """
    final_file_path = f"/home/shiva/PycharmProjects/mathematics_zero_to_hero/{filename}"
    print(f"final_file_path: {final_file_path}")
    file_path = (
        final_file_path
    )

    if not os.path.exists(file_path):
        return {"status":"error"}

    loader = PyPDFLoader(file_path)
    pages = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
    )

    chunks = splitter.split_documents(pages)

    # LangChain Document uses page_content
    full_content = "\n".join(
        chunk.page_content for chunk in chunks
    )

    return {"status":"success","content":full_content}


# 3. Create the agent
data_extractor_agent = LlmAgent(
    model=os.getenv("ADK_MODEL", "ollama_chat/llama3.2:3b"),
    name="root_agent",
    description="Extracts structured information from commercial invoices.",
    instruction="""
            You are a commercial invoice data extraction agent.
            
            Extract these two fields:
            
            1. awb_no:
               - Extract ONLY the value associated with the exact label
                 "INTERNATIONAL AIR WAYBILL NO".
               - The AWB number in this document is a numeric identifier.
               - Do not use the order number, commercial invoice number,
                 purchase order number, or any other identifier.
               - In particular, do not return values such as
                 "ORD-2026-1045" or "CI-2026-001".
               - Preserve the AWB number as a string.
               - If the value associated with the AWB label cannot be
                 identified, return null.
            
            2. total_price:
               - Extract the final total invoice price.
               - Return a numeric value, not a string.
               - Do not use the unit price as the total price.
               - If the total price cannot be identified, return null.
            3. shipper_address
               - complete name, address, telephone, Business
Registration No./ Customs / Tax ID No. e.g. GST / RFC / VAT / IN / EIN / ABN /
SSN, or as locally required
              - first line as company_name
              - Other than Tel and Tax Id as address
              - Tel as telephone_number 
              - Tax Id as tax_id
            4. consignee_address
              - complete name, address, telephone, Business Registration
No./ Customs / Tax ID No. e.g. GST / RFC / VAT / IN / EIN / ABN / SSN, or as
locally required)
              - first line as company_name
              - Other than Tel and Tax Id as address
              - Tel as telephone_number 
              - Tax Id as tax_id
            
            Return JSON containing exactly these fields:
            {
                "awb_no": "string or null",
                "total_price": "number or null",
                "shipper_address":{
                "company_name":"string or null",
                "address":"string or null",
                "telephone_number":"string or null",
                "tax_id":"string or null",
                },
                "consignee_address": {
                "company_name":"string or null",
                "address":"string or null",
                "telephone_number":"string or null",
                "tax_id":"string or null",
                }
            }
            
            Use only the extracted document text.
            Do not invent values.
            Return JSON only, without Markdown or explanations.
""",
    tools=[data_extraction]
)