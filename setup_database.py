from database import connect


def setup_database():
    conn = connect()
    if conn:
        cursor = conn.cursor()
        try:
            # Drop existing tables if they exist (optional but useful for initial setup)
            cursor.execute("DROP TABLE IF EXISTS properties")
            cursor.execute("DROP TABLE IF EXISTS spaces")
            cursor.execute("DROP TABLE IF EXISTS players")

            # Create players table with the new "position" column
            cursor.execute("""
                CREATE TABLE players (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    money INT NOT NULL,
                    turn_order INT NOT NULL,
                    position INT NOT NULL DEFAULT 0
                )
            """)
            # Create properties table
            cursor.execute("""
                CREATE TABLE properties (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    cost INT NOT NULL,
                    rent INT NOT NULL,
                    owner_id INT,
                    improvements INT NOT NULL DEFAULT 0,
                    FOREIGN KEY (owner_id) REFERENCES players(id)
                )
            """)
            # Create spaces table
            cursor.execute("""
                CREATE TABLE spaces (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    description TEXT NOT NULL
                )
            """)
            conn.commit()
            print("Database setup complete.")
        except Exception as e:
            print("Error setting up database:", e)
            conn.rollback()
        finally:
            cursor.close()
            conn.close()


if __name__ == "__main__":
    setup_database()
