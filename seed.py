from werkzeug.security import generate_password_hash
from db import get_db_connection, get_database_path


def seed_database() -> None:
    conn = get_db_connection()
    cursor = conn.cursor()

    # Clear existing data
    cursor.execute("DELETE FROM listings;")
    cursor.execute("DELETE FROM agents;")
    cursor.execute("DELETE FROM locations;")
    cursor.execute("DELETE FROM users;")

    # Reset auto-increment IDs
    cursor.execute("DELETE FROM sqlite_sequence WHERE name IN ('users', 'locations', 'agents', 'listings');")

    # Demo user
    cursor.execute(
        """
        INSERT INTO users (name, email, password_hash, role)
        VALUES (?, ?, ?, ?)
        """,
        (
            "Sahil Kumar",
            "sahil@example.com",
            generate_password_hash("123456"),
            "admin",
        ),
    )

    # Demo locations / offices
    locations = [
        ("Manhattan Office", "New York", "120 Broadway, New York, NY", "Active"),
        ("Brooklyn Office", "Brooklyn", "55 Court Street, Brooklyn, NY", "Active"),
        ("Queens Office", "Queens", "31-00 Queens Blvd, Queens, NY", "Active"),
    ]

    cursor.executemany(
        """
        INSERT INTO locations (name, city, address, status)
        VALUES (?, ?, ?, ?)
        """,
        locations,
    )

    # Demo agents
    agents = [
        ("Ava Johnson", "ava.johnson@example.com", "+1 212 555 0101", "Rentals", 1, "Active"),
        ("Michael Carter", "michael.carter@example.com", "+1 212 555 0102", "Sales", 1, "Active"),
        ("Sophia Lee", "sophia.lee@example.com", "+1 718 555 0103", "Property Management", 2, "Active"),
        ("Daniel Brooks", "daniel.brooks@example.com", "+1 718 555 0104", "Commercial", 3, "Inactive"),
    ]

    cursor.executemany(
        """
        INSERT INTO agents (name, email, phone, specialization, location_id, status)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        agents,
    )

    # Demo listings
    listings = [
        (
            "Modern 2-Bed Apartment in Manhattan",
            "245 West 34th Street",
            "New York",
            "Apartment",
            4200,
            2,
            1,
            "Available",
            "Bright apartment with open living space, updated kitchen, and easy access to transit.",
            1,
            1,
        ),
        (
            "Luxury Condo near Central Park",
            "78 West 58th Street",
            "New York",
            "Condo",
            850000,
            1,
            1,
            "Pending",
            "Premium condo with city views, modern finishes, and full-service building amenities.",
            2,
            1,
        ),
        (
            "Spacious Brooklyn Family Home",
            "112 Bedford Avenue",
            "Brooklyn",
            "House",
            6500,
            3,
            2,
            "Available",
            "Family-friendly home with spacious bedrooms, outdoor space, and nearby schools.",
            3,
            2,
        ),
        (
            "Studio Apartment in Queens",
            "41-20 27th Street",
            "Queens",
            "Studio",
            2300,
            0,
            1,
            "Rented",
            "Compact studio ideal for young professionals with easy subway access.",
            1,
            3,
        ),
        (
            "Commercial Retail Space",
            "88 Queens Plaza South",
            "Queens",
            "Commercial",
            12000,
            0,
            2,
            "Available",
            "High-visibility commercial space suitable for retail, office, or service business.",
            4,
            3,
        ),
    ]

    cursor.executemany(
        """
        INSERT INTO listings (
            title,
            address,
            city,
            property_type,
            price,
            bedrooms,
            bathrooms,
            status,
            description,
            agent_id,
            location_id
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        listings,
    )

    conn.commit()
    conn.close()


if __name__ == "__main__":
    print(f"Using database at: {get_database_path()}")
    seed_database()
    print("✅ Demo real estate data inserted successfully.")
    print("")
    print("Demo login:")
    print("Email: sahil@example.com")
    print("Password: 123456")