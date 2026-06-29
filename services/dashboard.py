from db import get_db_connection, rows_to_dicts


def get_dashboard_stats() -> dict:
    conn = get_db_connection()

    try:
        total_listings = conn.execute("SELECT COUNT(*) AS count FROM listings").fetchone()["count"]
        available_listings = conn.execute("SELECT COUNT(*) AS count FROM listings WHERE status = 'Available'").fetchone()["count"]
        pending_listings = conn.execute("SELECT COUNT(*) AS count FROM listings WHERE status = 'Pending'").fetchone()["count"]
        rented_listings = conn.execute("SELECT COUNT(*) AS count FROM listings WHERE status = 'Rented'").fetchone()["count"]
        sold_listings = conn.execute("SELECT COUNT(*) AS count FROM listings WHERE status = 'Sold'").fetchone()["count"]
        active_agents = conn.execute("SELECT COUNT(*) AS count FROM agents WHERE status = 'Active'").fetchone()["count"]
        total_locations = conn.execute("SELECT COUNT(*) AS count FROM locations").fetchone()["count"]
        unassigned_listings = conn.execute("SELECT COUNT(*) AS count FROM listings WHERE agent_id IS NULL").fetchone()["count"]

        recent_listings = conn.execute(
            """
            SELECT listings.id, listings.title, listings.city, listings.property_type,
                   listings.price, listings.status, agents.name AS agent_name
            FROM listings
            LEFT JOIN agents ON agents.id = listings.agent_id
            ORDER BY listings.id DESC
            LIMIT 5
            """
        ).fetchall()

        return {
            "total_listings": total_listings,
            "available_listings": available_listings,
            "pending_listings": pending_listings,
            "rented_listings": rented_listings,
            "sold_listings": sold_listings,
            "active_agents": active_agents,
            "total_locations": total_locations,
            "unassigned_listings": unassigned_listings,
            "recent_listings": rows_to_dicts(recent_listings),
        }

    finally:
        conn.close()
