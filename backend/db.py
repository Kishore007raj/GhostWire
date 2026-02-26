#our main file for handling database operations for the ghostwire agent

import sqlite3
import os
from pathlib import Path

DB_PATH = Path("data/db/ghostwire.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Enable dict-like access to rows
    return conn

def fetch_all_connections(limit: int = 100):
    conn = get_db_connection()
    rows = conn.execute(
        """SELECT * FROM connections ORDER BY timestamp DESC LIMIT ?""",
        (limit,)
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]

def fetch_all_alerts(limit: int = 100):
    conn = get_db_connection()
    rows = conn.execute(
        """SELECT * FROM alerts ORDER BY timestamp DESC LIMIT ?""",
        (limit,)
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]

def fetch_bandwidth_summary(limit: int = 100):
    conn = get_db_connection()
    rows = conn.execute(
        """SELECT * FROM bandwidth_summary ORDER BY timestamp DESC LIMIT ?""",
        (limit,)
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]