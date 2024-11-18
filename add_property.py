from database import connect

class Property:
    def __init__(self, name, cost, rent, improvements=0, owner_id=None):
        self.name = name
        self.cost = cost
        self.rent = rent
        self.improvements = improvements
        self.owner_id = owner_id

    def save_to_db(self, connection):
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO properties (name, cost, rent, improvements, owner_id) 
                VALUES (%s, %s, %s, %s, %s) RETURNING id
            """, (self.name, self.cost, self.rent, self.improvements, self.owner_id))
            property_id = cursor.fetchone()[0]
            connection.commit()
            self.id = property_id
            print(f"Property {self.name} added to the database with ID: {self.id}")

def add_property(name, cost, rent):
    conn = connect()
    if conn:
        property = Property(name, cost, rent)
        property.save_to_db(conn)
        conn.close()

if __name__ == "__main__":
    name = input("Enter property name: ")
    cost = int(input("Enter property cost: "))
    rent = int(input("Enter property rent: "))
    add_property(name, cost, rent)
