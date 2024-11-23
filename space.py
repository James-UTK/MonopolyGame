from database import connect

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
            print(f"Space {self.name} added to the game with ID: {self.id}")

def add_space(name, description):
    conn = connect()
    if conn:
        space = Space(name, description)
        space.save_to_db(conn)
        conn.close()

def add_predefined_spaces():
    spaces = [
        ("Go", "Collect $200 salary as you pass."),
        ("Jail", "Just visiting."),
        ("Community Fund", "Receive or pay $50."),
        ("Income Tax", "Pay $200."),
        ("Luxury Tax", "Pay $100."),
    ]
    for space in spaces:
        add_space(space[0], space[1])

if __name__ == "__main__":
    add_predefined_spaces()
