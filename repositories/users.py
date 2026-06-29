import sqlite3
from typing import Optional

from werkzeug.security import check_password_hash, generate_password_hash

from db import get_db_connection, row_to_dict


def create_user(name: str, email: str, password: str, role: str = "admin") -> Optional[dict]:
    conn = get_db_connection()

    try:
        cursor = conn.execute(
            """
            INSERT INTO users (name, email, password_hash, role)
            VALUES (?, ?, ?, ?)
            """,
            (name, email.lower().strip(), generate_password_hash(password), role),
        )
        conn.commit()

        user_id = cursor.lastrowid
        row = conn.execute(
            """
            SELECT id, name, email, role, created_at
            FROM users
            WHERE id = ?
            """,
            (user_id,),
        ).fetchone()

        return row_to_dict(row)

    except sqlite3.IntegrityError:
        return None

    finally:
        conn.close()


def get_user_by_email(email: str) -> Optional[dict]:
    conn = get_db_connection()

    try:
        row = conn.execute(
            """
            SELECT id, name, email, password_hash, role, created_at
            FROM users
            WHERE email = ?
            """,
            (email.lower().strip(),),
        ).fetchone()

        return row_to_dict(row)

    finally:
        conn.close()


def get_user_by_id(user_id: int) -> Optional[dict]:
    conn = get_db_connection()

    try:
        row = conn.execute(
            """
            SELECT id, name, email, role, created_at
            FROM users
            WHERE id = ?
            """,
            (user_id,),
        ).fetchone()

        return row_to_dict(row)

    finally:
        conn.close()


def authenticate_user(email: str, password: str) -> Optional[dict]:
    user = get_user_by_email(email)

    if not user:
        return None

    if not check_password_hash(user["password_hash"], password):
        return None

    return {
        "id": user["id"],
        "name": user["name"],
        "email": user["email"],
        "role": user["role"],
        "created_at": user["created_at"],
    }
