import sqlite3

from fastapi import FastAPI, HTTPException, status,File, HTTPException, UploadFile
from pathlib import Path
import logging
import uuid
from fastapi.responses import FileResponse
from doc_classifier.db_store.doc_db_store import DocDbStore
from doc_classifier.model.models import ShipmentCreate, ShipmentResponse

UPLOAD_DIR = Path.cwd() / "uploads" / "invoices"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

MAX_FILE_SIZE = 20 * 1024 * 1024  # 20 MB

logger = logging.getLogger(__name__)

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


@app.post("/invoices/upload", status_code=201)
async def upload_invoice(file: UploadFile = File(...)):
    # Validate the original filename.
    if not file.filename or Path(file.filename).suffix.lower() != ".pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF invoice files are allowed.",
        )

    # Validate the PDF signature and enforce the file-size limit.
    content = await file.read(MAX_FILE_SIZE + 1)

    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="File size must not exceed 20 MB.",
        )

    if not content.startswith(b"%PDF-"):
        raise HTTPException(
            status_code=400,
            detail="The uploaded file is not a valid PDF.",
        )

    # Generate a unique storage name; never use the supplied filename
    # directly as a filesystem path.
    stored_filename = f"{uuid.uuid4().hex}.pdf"
    file_path = UPLOAD_DIR / stored_filename

    try:
        file_path.write_bytes(content)

        invoice_id = db.save_invoice(
            original_filename=Path(file.filename).name,
            stored_filename=stored_filename,
            file_path=str(file_path.resolve()),
            content_type="application/pdf",
            file_size=len(content),
        )

        return {
            "message": "Invoice uploaded successfully",
            "invoice_id": invoice_id,
            "filename": Path(file.filename).name,
            "file_size": len(content),
        }

    except Exception:
        # Avoid leaving an orphaned PDF if the database operation fails.
        file_path.unlink(missing_ok=True)
        logger.exception("Failed to save uploaded invoice")
        raise HTTPException(
            status_code=500,
            detail="Unable to save the invoice.",
        )

    finally:
        await file.close()


@app.get("/invoices")
def list_invoices():
    return db.get_all_invoices()


@app.get("/invoices/{invoice_id}")
def get_invoice(invoice_id: int):
    invoice = db.get_invoice(invoice_id)

    if invoice is None:
        raise HTTPException(
            status_code=404,
            detail="Invoice not found.",
        )

    # Expose metadata, not the internal filesystem path.
    return {
        "id": invoice["id"],
        "filename": invoice["original_filename"],
        "content_type": invoice["content_type"],
        "file_size": invoice["file_size"],
        "uploaded_at": invoice["uploaded_at"],
    }


@app.get("/invoices/{invoice_id}/download")
def download_invoice(invoice_id: int):
    invoice = db.get_invoice(invoice_id)

    if invoice is None:
        raise HTTPException(
            status_code=404,
            detail="Invoice not found.",
        )

    file_path = Path(invoice["file_path"])

    if not file_path.is_file():
        raise HTTPException(
            status_code=404,
            detail="Invoice file not found on disk.",
        )

    return FileResponse(
        path=file_path,
        media_type="application/pdf",
        filename=invoice["original_filename"],
    )