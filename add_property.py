from database import connect

class Property:
    def __init__(self, name, cost, rent, owner_id=None, improvements=0):
        self.name = name
        self.cost = cost
        self.rent = rent
        self.owner_id = owner_id
        self.improvements = improvements

    def save_to_db(self, connection):
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO properties (name, cost, rent, owner_id, improvements)
                VALUES (%s, %s, %s, %s, %s) RETURNING id
            """, (self.name, self.cost, self.rent, self.owner_id, self.improvements))
            property_id = cursor.fetchone()[0]
            connection.commit()
            self.id = property_id
            print(f"Property {self.name} added to the game with ID: {self.id}")

def add_property(name, cost, rent, owner_id=None, improvements=0):
    conn = connect()
    if conn:
        property = Property(name, cost, rent, owner_id, improvements)
        property.save_to_db(conn)
        conn.close()

def add_predefined_properties():
    properties = [
        ("Mediterranean Avenue", 60, 2),
        ("Baltic Avenue", 60, 4),
        ("Oriental Avenue", 100, 6),
        ("Vermont Avenue", 100, 6),
        ("Connecticut Avenue", 120, 8),
        ("Park Place", 350, 35),
        ("Boardwalk", 400, 50)
    ]
    for prop in properties:
        add_property(prop[0], prop[1], prop[2])

if __name__ == "__main__":
    add_predefined_properties()
