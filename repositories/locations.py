from typing import Optional

from db import get_db_connection, row_to_dict, rows_to_dicts


def get_all_locations() -> list[dict]:
    conn = get_db_connection()

    try:
        rows = conn.execute(
            """
            SELECT
                locations.*,
                COUNT(DISTINCT agents.id) AS total_agents,
                COUNT(DISTINCT listings.id) AS total_listings
            FROM locations
            LEFT JOIN agents ON agents.location_id = locations.id
            LEFT JOIN listings ON listings.location_id = locations.id
            GROUP BY locations.id
            ORDER BY locations.id DESC
            """
        ).fetchall()

        return rows_to_dicts(rows)

    finally:
        conn.close()


def get_location_by_id(location_id: int) -> Optional[dict]:
    conn = get_db_connection()

    try:
        row = conn.execute(
            """
            SELECT *
            FROM locations
            WHERE id = ?
            """,
            (location_id,),
        ).fetchone()

        return row_to_dict(row)

    finally:
        conn.close()


def create_location(name: str, city: str, address: str, status: str) -> dict:
    conn = get_db_connection()

    try:
        cursor = conn.execute(
            """
            INSERT INTO locations (name, city, address, status)
            VALUES (?, ?, ?, ?)
            """,
            (name, city, address, status),
        )
        conn.commit()

        return get_location_by_id(cursor.lastrowid)

    finally:
        conn.close()


def update_location(location_id: int, name: str, city: str, address: str, status: str) -> Optional[dict]:
    conn = get_db_connection()

    try:
        conn.execute(
            """
            UPDATE locations
            SET name = ?, city = ?, address = ?, status = ?
            WHERE id = ?
            """,
            (name, city, address, status, location_id),
        )
        conn.commit()

        return get_location_by_id(location_id)

    finally:
        conn.close()


def delete_location(location_id: int) -> bool:
    conn = get_db_connection()

    try:
        cursor = conn.execute(
            """
            DELETE FROM locations
            WHERE id = ?
            """,
            (location_id,),
        )
        conn.commit()

        return cursor.rowcount > 0

    finally:
        conn.close()
