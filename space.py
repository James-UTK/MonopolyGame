class Space:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def save_to_db(self, connection):
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO spaces (name, description) 
                VALUES (%s, %s) RETURNING id
            """, (self.name, self.description))
            space_id = cursor.fetchone()[0]
            connection.commit()
            self.id = space_id
            print(f"Space {self.name} added to the database with ID: {self.id}")

if __name__ == "__MAIN__":
    from database import connect

    conn = connect()
    if conn:
        space = Space("Jail", "You are in jail. You lose a turn.")
        space.save_to_db(conn)
        conn.close()
