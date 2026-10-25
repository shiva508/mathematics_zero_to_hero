import sqlite3


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