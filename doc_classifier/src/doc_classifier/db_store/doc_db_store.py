import sqlite3
from pathlib import Path
from typing import Any

class DocDbStore:

    def __init__(self, database_name="shipment_info.db"):
        self.database_name = database_name
        self.initialize_database()

    def initialize_database(self):
        with sqlite3.connect(self.database_name) as connection:
            connection.execute("""
                CREATE TABLE IF NOT EXISTS shipment_info (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    awb TEXT NOT NULL UNIQUE,
                    status TEXT NOT NULL,
                    origin TEXT NOT NULL,
                    destination TEXT NOT NULL
                )
            """)
            connection.execute("""
                CREATE TABLE IF NOT EXISTS shipment_documents (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    shipment_id INTEGER,
                    original_filename TEXT NOT NULL,
                    stored_filename TEXT NOT NULL UNIQUE,
                    file_path TEXT NOT NULL,
                    content_type TEXT NOT NULL,
                    file_size INTEGER NOT NULL,
                    uploaded_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
            """)

    def insert_shipment(self, shipment: dict):
        with sqlite3.connect(self.database_name) as connection:
            cursor = connection.execute("""
                INSERT INTO shipment_info
                    (awb, status, origin, destination)
                VALUES (?, ?, ?, ?)
            """, (
                shipment["awb"],
                shipment["status"],
                shipment["origin"],
                shipment["destination"]
            ))

            return {
                "id": cursor.lastrowid,
                **shipment
            }

    def get_shipment(self, awb: str):
        with sqlite3.connect(self.database_name) as connection:
            connection.row_factory = sqlite3.Row

            row = connection.execute("""
                SELECT id, awb, status, origin, destination
                FROM shipment_info
                WHERE awb = ?
            """, (awb,)).fetchone()

            return dict(row) if row else None

    def get_all_shipments(self):
        with sqlite3.connect(self.database_name) as connection:
            connection.row_factory = sqlite3.Row

            rows = connection.execute("""
                SELECT id, awb, status, origin, destination
                FROM shipment_info
                ORDER BY id DESC
            """).fetchall()

            return [dict(row) for row in rows]

    def save_invoice(
            self,
            original_filename: str,
            stored_filename: str,
            file_path: str,
            content_type: str,
            file_size: int,
            shipment_id
    ) -> int | None:
        with sqlite3.connect(self.database_name) as conn:
            cursor = conn.execute(
                """
                INSERT INTO shipment_documents (
                    original_filename,
                    stored_filename,
                    file_path,
                    content_type,
                    file_size,
                    shipment_id
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    original_filename,
                    stored_filename,
                    file_path,
                    content_type,
                    file_size,
                    shipment_id
                ),
            )
            return cursor.lastrowid

    def get_invoice(self, invoice_id: int) -> dict[str, Any] | None:
        with sqlite3.connect(self.database_name) as conn:
            conn.row_factory = sqlite3.Row

            row = conn.execute(
                "SELECT * FROM shipment_documents WHERE id = ?",
                (invoice_id,),
            ).fetchone()

            return dict(row) if row else None

    def get_all_invoices(self) -> list[dict[str, Any]]:
        with sqlite3.connect(self.database_name) as conn:
            conn.row_factory = sqlite3.Row

            rows = conn.execute(
                "SELECT * FROM shipment_documents ORDER BY uploaded_at DESC"
            ).fetchall()

            return [dict(row) for row in rows]