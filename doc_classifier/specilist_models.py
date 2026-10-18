from pydantic import BaseModel

class InvoiceDetails(BaseModel):
    vendor: str
    total_amount: str
    due_date: str


class ReviewDetails(BaseModel):
    rating: int
    sentiment: str
    key_point: str