"""SQLite-backed, deterministic synthetic evidence for the offline demo."""

from __future__ import annotations

import sqlite3
from pathlib import Path


DEFAULT_DATABASE_PATH = Path(__file__).with_name("evidence-tracer.sqlite3")

SCHEMA = """
PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS transactions (
    id TEXT PRIMARY KEY, reference TEXT NOT NULL UNIQUE, status TEXT NOT NULL,
    description TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS stock_movements (
    id TEXT PRIMARY KEY, transaction_id TEXT NOT NULL REFERENCES transactions(id),
    movement_type TEXT NOT NULL, quantity INTEGER NOT NULL, occurred_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS invoices (
    id TEXT PRIMARY KEY, transaction_id TEXT NOT NULL REFERENCES transactions(id),
    invoice_number TEXT NOT NULL UNIQUE, quantity INTEGER NOT NULL,
    amount_cents INTEGER NOT NULL, status TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS payments (
    id TEXT PRIMARY KEY, transaction_id TEXT NOT NULL REFERENCES transactions(id),
    payment_reference TEXT NOT NULL UNIQUE, amount_cents INTEGER NOT NULL,
    status TEXT NOT NULL, received_at TEXT NOT NULL
);
"""

TRANSACTIONS = (
    ("txn-clear", "TXN-1001", "completed", "Completed synthetic supply request"),
    ("txn-quantity", "TXN-1002", "completed", "Synthetic request with a quantity conflict"),
    ("txn-missing-payment", "TXN-1003", "awaiting_payment", "Synthetic request awaiting payment evidence"),
)
STOCK_MOVEMENTS = (
    ("stock-1001", "txn-clear", "outbound", 12, "2026-10-01T09:15:00Z"),
    ("stock-1002", "txn-quantity", "outbound", 8, "2026-10-02T10:30:00Z"),
    ("stock-1003", "txn-missing-payment", "outbound", 5, "2026-10-03T11:45:00Z"),
)
INVOICES = (
    ("invoice-1001", "txn-clear", "INV-1001", 12, 180000, "issued"),
    ("invoice-1002", "txn-quantity", "INV-1002", 10, 150000, "issued"),
    ("invoice-1003", "txn-missing-payment", "INV-1003", 5, 75000, "issued"),
)
PAYMENTS = (
    ("payment-1001", "txn-clear", "PAY-1001", 180000, "settled", "2026-10-01T12:00:00Z"),
    ("payment-1002", "txn-quantity", "PAY-1002", 150000, "settled", "2026-10-02T14:00:00Z"),
)


def connect(database_path: str | Path = DEFAULT_DATABASE_PATH) -> sqlite3.Connection:
    """Open a local SQLite database with named-column access enabled."""
    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def initialize(connection: sqlite3.Connection) -> None:
    """Create the schema and replace its contents with the repeatable demo seed."""
    connection.executescript(SCHEMA)
    with connection:
        for table in ("payments", "invoices", "stock_movements", "transactions"):
            connection.execute(f"DELETE FROM {table}")
        connection.executemany("INSERT INTO transactions VALUES (?, ?, ?, ?)", TRANSACTIONS)
        connection.executemany("INSERT INTO stock_movements VALUES (?, ?, ?, ?, ?)", STOCK_MOVEMENTS)
        connection.executemany("INSERT INTO invoices VALUES (?, ?, ?, ?, ?, ?)", INVOICES)
        connection.executemany("INSERT INTO payments VALUES (?, ?, ?, ?, ?, ?)", PAYMENTS)


def list_transactions(connection: sqlite3.Connection) -> list[dict]:
    """Return transaction summaries in stable reference order."""
    rows = connection.execute(
        "SELECT id, reference, status, description FROM transactions ORDER BY reference"
    ).fetchall()
    return [dict(row) for row in rows]


def get_evidence_links(connection: sqlite3.Connection, transaction_id: str) -> list[dict]:
    """Return every evidence record for one transaction in trail display order."""
    query = """
        SELECT evidence_type, id, detail, quantity, amount_cents, recorded_at
        FROM (
            SELECT 'stock_movement' AS evidence_type, id, movement_type AS detail,
                   quantity, NULL AS amount_cents, occurred_at AS recorded_at, 1 AS trail_order
            FROM stock_movements WHERE transaction_id = ?
            UNION ALL
            SELECT 'invoice', id, invoice_number, quantity, amount_cents, NULL, 2
            FROM invoices WHERE transaction_id = ?
            UNION ALL
            SELECT 'payment', id, payment_reference, NULL, amount_cents, received_at, 3
            FROM payments WHERE transaction_id = ?
        )
        ORDER BY trail_order, id
    """
    rows = connection.execute(query, (transaction_id, transaction_id, transaction_id)).fetchall()
    return [dict(row) for row in rows]


def seed_database(database_path: str | Path = DEFAULT_DATABASE_PATH) -> None:
    """Create or reset a local demonstration database at *database_path*."""
    with connect(database_path) as connection:
        initialize(connection)
