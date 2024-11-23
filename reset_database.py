# Resets the database by clearing all data and resetting ID sequences for players, properties, and spaces.
from database import connect

def reset_database():
    conn = connect()
    if conn:
        cursor = conn.cursor()
        try:
            # First, remove ownership from properties
            cursor.execute("UPDATE properties SET owner_id = NULL")
            # Then, delete all records from players, properties, and spaces tables
            cursor.execute("DELETE FROM players")
            cursor.execute("DELETE FROM properties")
            cursor.execute("DELETE FROM spaces")
            # Reset the sequences for each table
            cursor.execute("ALTER SEQUENCE players_id_seq RESTART WITH 1")
            cursor.execute("ALTER SEQUENCE properties_id_seq RESTART WITH 1")
            cursor.execute("ALTER SEQUENCE spaces_id_seq RESTART WITH 1")
            conn.commit()
            print("Database has been reset.")
        except Exception as e:
            print("Error resetting database:", e)
            conn.rollback()
        finally:
            cursor.close()
            conn.close()

if __name__ == "__main__":
    reset_database()
