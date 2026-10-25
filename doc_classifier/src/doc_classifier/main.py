import sqlite3

from fastapi import FastAPI, HTTPException, status

from doc_classifier.db_store.doc_db_store import DocDbStore
from doc_classifier.model.models import ShipmentCreate, ShipmentResponse


app = FastAPI(
    title="Shipment Information API",
    description="API for managing shipment information using SQLite",
    version="1.0.0"
)

db = DocDbStore()


@app.get("/")
def home():
    return {
        "message": "Shipment Information API is running"
    }


@app.post(
    "/shipments",
    response_model=ShipmentResponse,
    status_code=status.HTTP_201_CREATED
)
def create_shipment(shipment: ShipmentCreate):
    try:
        return db.insert_shipment(shipment.model_dump())

    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A shipment with this AWB already exists"
        )


@app.get(
    "/shipments",
    response_model=list[ShipmentResponse]
)
def get_all_shipments():
    return db.get_all_shipments()


@app.get(
    "/shipments/{awb}",
    response_model=ShipmentResponse
)
def get_shipment(awb: str):
    shipment = db.get_shipment(awb)

    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shipment not found"
        )

    return shipment


@app.put(
    "/shipments/{awb}",
    response_model=ShipmentResponse
)
def update_shipment(awb: str, shipment: ShipmentCreate):
    updated = db.update_shipment(
        awb,
        shipment.model_dump()
    )

    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shipment not found"
        )

    return db.get_shipment(awb)


@app.delete("/shipments/{awb}")
def delete_shipment(awb: str):
    deleted = db.delete_shipment(awb)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shipment not found"
        )

    return {
        "message": "Shipment deleted successfully",
        "awb": awb
    }