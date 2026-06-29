import os
import sqlite3
from typing import Any, Iterable, Optional


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "ams.db")


def get_db_connection() -> sqlite3.Connection:
    """
    Creates a SQLite connection with:
    - dictionary-like row access
    - foreign key support
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


# Backward-compatible alias in case any old file imports get_db()
def get_db() -> sqlite3.Connection:
    return get_db_connection()


def row_to_dict(row: Optional[sqlite3.Row]) -> Optional[dict]:
    """
    Converts a single SQLite row to a Python dict.
    """
    if row is None:
        return None
    return dict(row)


def rows_to_dicts(rows: Iterable[sqlite3.Row]) -> list[dict]:
    """
    Converts multiple SQLite rows to a list of Python dicts.
    """
    return [dict(row) for row in rows]


def fetch_one(query: str, params: tuple = ()) -> Optional[dict]:
    """
    Runs a SELECT query and returns one row as a dict.
    """
    conn = get_db_connection()
    try:
        row = conn.execute(query, params).fetchone()
        return row_to_dict(row)
    finally:
        conn.close()


def fetch_all(query: str, params: tuple = ()) -> list[dict]:
    """
    Runs a SELECT query and returns all rows as list of dicts.
    """
    conn = get_db_connection()
    try:
        rows = conn.execute(query, params).fetchall()
        return rows_to_dicts(rows)
    finally:
        conn.close()


def execute_query(query: str, params: tuple = ()) -> int:
    """
    Runs INSERT/UPDATE/DELETE query.
    Returns last inserted row id when applicable.
    """
    conn = get_db_connection()
    try:
        cursor = conn.execute(query, params)
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()


def execute_many(query: str, params_list: list[tuple]) -> None:
    """
    Runs multiple INSERT/UPDATE/DELETE queries.
    Useful for seeding data.
    """
    conn = get_db_connection()
    try:
        conn.executemany(query, params_list)
        conn.commit()
    finally:
        conn.close()


def database_exists() -> bool:
    return os.path.exists(DB_PATH)


def get_database_path() -> str:
    return DB_PATH