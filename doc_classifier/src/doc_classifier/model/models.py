from pydantic import BaseModel, Field


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