from pydantic import BaseModel, Field
import datetime


class ShipmentCreate(BaseModel):
    awb: str = Field(min_length=1, max_length=50)
    status: str = Field(default="Created", min_length=1)
    origin: str = Field(min_length=1)
    destination: str = Field(min_length=1)


class ShipmentResponse(BaseModel):
    id: int
    awb: str
    status: str
    origin: str
    destination: str

class DocumentRequest(BaseModel):
    shipment_id: int | None = None
    original_filename: str = Field()
    stored_filename: str = Field()
    file_path: str = Field()
    content_type: str = Field()
    file_size: int = Field()

class DocumentResponse(BaseModel):
    id: int
    shipment_id: int | None = None
    original_filename: str
    stored_filename: str
    file_path: str
    content_type: str
    file_size: int
    uploaded_at: datetime