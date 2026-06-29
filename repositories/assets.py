from typing import Optional

from db import get_db_connection, row_to_dict, rows_to_dicts


def get_all_listings() -> list[dict]:
    conn = get_db_connection()

    try:
        rows = conn.execute(
            """
            SELECT
                listings.*,
                agents.name AS agent_name,
                agents.email AS agent_email,
                locations.name AS location_name,
                locations.city AS location_city
            FROM listings
            LEFT JOIN agents ON agents.id = listings.agent_id
            LEFT JOIN locations ON locations.id = listings.location_id
            ORDER BY listings.id DESC
            """
        ).fetchall()

        return rows_to_dicts(rows)

    finally:
        conn.close()


def get_listing_by_id(listing_id: int) -> Optional[dict]:
    conn = get_db_connection()

    try:
        row = conn.execute(
            """
            SELECT
                listings.*,
                agents.name AS agent_name,
                agents.email AS agent_email,
                agents.phone AS agent_phone,
                locations.name AS location_name,
                locations.city AS location_city
            FROM listings
            LEFT JOIN agents ON agents.id = listings.agent_id
            LEFT JOIN locations ON locations.id = listings.location_id
            WHERE listings.id = ?
            """,
            (listing_id,),
        ).fetchone()

        return row_to_dict(row)

    finally:
        conn.close()


def create_listing(
    title: str,
    address: str,
    city: str,
    property_type: str,
    price: float,
    bedrooms: int,
    bathrooms: int,
    status: str,
    description: str,
    agent_id: Optional[int],
    location_id: Optional[int],
) -> dict:
    conn = get_db_connection()

    try:
        cursor = conn.execute(
            """
            INSERT INTO listings (
                title, address, city, property_type, price,
                bedrooms, bathrooms, status, description, agent_id, location_id
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (title, address, city, property_type, price, bedrooms, bathrooms,
             status, description, agent_id, location_id),
        )
        conn.commit()

        return get_listing_by_id(cursor.lastrowid)

    finally:
        conn.close()


def update_listing(
    listing_id: int,
    title: str,
    address: str,
    city: str,
    property_type: str,
    price: float,
    bedrooms: int,
    bathrooms: int,
    status: str,
    description: str,
    agent_id: Optional[int],
    location_id: Optional[int],
) -> Optional[dict]:
    conn = get_db_connection()

    try:
        conn.execute(
            """
            UPDATE listings
            SET title = ?, address = ?, city = ?, property_type = ?, price = ?,
                bedrooms = ?, bathrooms = ?, status = ?, description = ?,
                agent_id = ?, location_id = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (title, address, city, property_type, price, bedrooms, bathrooms,
             status, description, agent_id, location_id, listing_id),
        )
        conn.commit()

        return get_listing_by_id(listing_id)

    finally:
        conn.close()


def delete_listing(listing_id: int) -> bool:
    conn = get_db_connection()

    try:
        cursor = conn.execute("DELETE FROM listings WHERE id = ?", (listing_id,))
        conn.commit()

        return cursor.rowcount > 0

    finally:
        conn.close()
