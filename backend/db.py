#our main file for handling database operations for the ghostwire agent

import sqlite3
import os
from pathlib import Path

# Use an absolute path so backend and agent agree regardless of cwd
PROJECT_ROOT = Path(__file__).parent.parent  # backend/..
DB_PATH = PROJECT_ROOT / "data" / "db" / "ghostwire.db"

# make sure directory exists before connecting
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

def get_db_connection():
    # each caller gets a fresh connection; configure for WAL and reasonable timeout
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row  # Enable dict-like access to rows
    try:
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA busy_timeout=5000;")
    except sqlite3.DatabaseError:
        # if database not yet created or another error, continue silently
        pass
    return conn

def fetch_all_connections(limit: int = 100):
    try:
        conn = get_db_connection()
        rows = conn.execute(
            """SELECT * FROM connections ORDER BY timestamp DESC LIMIT ?""",
            (limit,)
        ).fetchall()
        return [dict(row) for row in rows]
    except Exception as e:
        # log issue and return empty list
        print(f"DB error fetching connections: {e}")
        return []
    finally:
        try:
            conn.close()
        except Exception:
            pass

def fetch_all_alerts(limit: int = 100):
    try:
        conn = get_db_connection()
        rows = conn.execute(
            """SELECT * FROM alerts ORDER BY timestamp DESC LIMIT ?""",
            (limit,)
        ).fetchall()
        return [dict(row) for row in rows]
    except Exception as e:
        print(f"DB error fetching alerts: {e}")
        return []
    finally:
        try:
            conn.close()
        except Exception:
            pass

def fetch_bandwidth_summary(limit: int = 100):
    try:
        conn = get_db_connection()
        rows = conn.execute(
            """SELECT * FROM bandwidth_summary ORDER BY timestamp DESC LIMIT ?""",
            (limit,)
        ).fetchall()
        return [dict(row) for row in rows]
    except Exception as e:
        print(f"DB error fetching bandwidth: {e}")
        return []
    finally:
        try:
            conn.close()
        except Exception:
            pass