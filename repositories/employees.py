import sqlite3
from typing import Optional

from db import get_db_connection, row_to_dict, rows_to_dicts


def get_all_agents() -> list[dict]:
    conn = get_db_connection()

    try:
        rows = conn.execute(
            """
            SELECT
                agents.*,
                locations.name AS location_name,
                locations.city AS location_city,
                COUNT(listings.id) AS assigned_listings
            FROM agents
            LEFT JOIN locations ON locations.id = agents.location_id
            LEFT JOIN listings ON listings.agent_id = agents.id
            GROUP BY agents.id
            ORDER BY agents.id DESC
            """
        ).fetchall()

        return rows_to_dicts(rows)

    finally:
        conn.close()


def get_agent_by_id(agent_id: int) -> Optional[dict]:
    conn = get_db_connection()

    try:
        row = conn.execute(
            """
            SELECT
                agents.*,
                locations.name AS location_name,
                locations.city AS location_city
            FROM agents
            LEFT JOIN locations ON locations.id = agents.location_id
            WHERE agents.id = ?
            """,
            (agent_id,),
        ).fetchone()

        return row_to_dict(row)

    finally:
        conn.close()


def create_agent(
    name: str,
    email: str,
    phone: str,
    specialization: str,
    location_id: Optional[int],
    status: str,
) -> Optional[dict]:
    conn = get_db_connection()

    try:
        cursor = conn.execute(
            """
            INSERT INTO agents (name, email, phone, specialization, location_id, status)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                name,
                email.lower().strip(),
                phone,
                specialization,
                location_id,
                status,
            ),
        )
        conn.commit()

        return get_agent_by_id(cursor.lastrowid)

    except sqlite3.IntegrityError:
        return None

    finally:
        conn.close()


def update_agent(
    agent_id: int,
    name: str,
    email: str,
    phone: str,
    specialization: str,
    location_id: Optional[int],
    status: str,
) -> Optional[dict]:
    conn = get_db_connection()

    try:
        conn.execute(
            """
            UPDATE agents
            SET name = ?, email = ?, phone = ?, specialization = ?, location_id = ?, status = ?
            WHERE id = ?
            """,
            (
                name,
                email.lower().strip(),
                phone,
                specialization,
                location_id,
                status,
                agent_id,
            ),
        )
        conn.commit()

        return get_agent_by_id(agent_id)

    except sqlite3.IntegrityError:
        return None

    finally:
        conn.close()


def delete_agent(agent_id: int) -> bool:
    conn = get_db_connection()

    try:
        cursor = conn.execute(
            """
            DELETE FROM agents
            WHERE id = ?
            """,
            (agent_id,),
        )
        conn.commit()

        return cursor.rowcount > 0

    finally:
        conn.close()
