from database import connect

def create_tables():
    connection = connect()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS players (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(50) NOT NULL,
                    money INTEGER NOT NULL,
                    turn_order INTEGER NOT NULL
                );
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS properties (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    owner_id INTEGER REFERENCES players(id),
                    cost INTEGER NOT NULL,
                    rent INTEGER NOT NULL,
                    improvements INTEGER DEFAULT 0
                );
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS spaces (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    description TEXT
                );
            """)
            connection.commit()
            print("Tables created successfully!")
        except Exception as e:
            print("Error creating tables:", e)
            connection.rollback()
        finally:
            cursor.close()
            connection.close()

if __name__ == "__main__":
    create_tables()
