from db import get_db_connection, get_database_path


def create_tables() -> None:
    conn = get_db_connection()
    cursor = conn.cursor()

    # Temporarily disable foreign key checks while dropping old tables
    cursor.execute("PRAGMA foreign_keys = OFF;")

    cursor.executescript(
        """
        DROP TABLE IF EXISTS assets;
        DROP TABLE IF EXISTS employees;
        DROP TABLE IF EXISTS listings;
        DROP TABLE IF EXISTS agents;
        DROP TABLE IF EXISTS locations;
        DROP TABLE IF EXISTS users;
        """
    )

    # Re-enable foreign key checks for new schema
    cursor.execute("PRAGMA foreign_keys = ON;")

    cursor.executescript(
        """
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'admin',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE locations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            city TEXT NOT NULL,
            address TEXT,
            status TEXT NOT NULL DEFAULT 'Active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE agents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT,
            specialization TEXT,
            location_id INTEGER,
            status TEXT NOT NULL DEFAULT 'Active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (location_id) REFERENCES locations(id)
                ON DELETE SET NULL
        );

        CREATE TABLE listings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            address TEXT NOT NULL,
            city TEXT NOT NULL,
            property_type TEXT NOT NULL,
            price REAL NOT NULL,
            bedrooms INTEGER DEFAULT 0,
            bathrooms INTEGER DEFAULT 0,
            status TEXT NOT NULL DEFAULT 'Available',
            description TEXT,
            agent_id INTEGER,
            location_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (agent_id) REFERENCES agents(id)
                ON DELETE SET NULL,
            FOREIGN KEY (location_id) REFERENCES locations(id)
                ON DELETE SET NULL
        );

        CREATE INDEX idx_listings_status ON listings(status);
        CREATE INDEX idx_listings_agent_id ON listings(agent_id);
        CREATE INDEX idx_listings_location_id ON listings(location_id);
        CREATE INDEX idx_agents_location_id ON agents(location_id);
        """
    )

    conn.commit()
    conn.close()


if __name__ == "__main__":
    print(f"Using database at: {get_database_path()}")
    create_tables()
    print("✅ Database tables created successfully.")