# Contains all the logic related to properties, including buying, selling, paying rent, and improvements.
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

    def update_owner(self, connection, owner_id):
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE properties
                SET owner_id = %s
                WHERE id = %s
            """, (owner_id, self.id))
            connection.commit()

    def improve(self, connection):
        self.improvements += 1
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE properties
                SET improvements = %s
                WHERE id = %s
            """, (self.improvements, self.id))
            connection.commit()

def add_property(name, cost, rent, owner_id=None, improvements=0):
    # Adds a new property to the database with the given details: name, cost, rent, owner, and improvements.

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

def buy_property(player_id, property_id):
    # Allows a player to buy a property if it is unowned and they have enough money.

    conn = connect()
    if conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT cost, owner_id FROM properties WHERE id = %s", (property_id,))
            property_data = cursor.fetchone()
            cost, owner_id = property_data
            if owner_id is None:  # Property is available for purchase
                cursor.execute("SELECT money FROM players WHERE id = %s", (player_id,))
                player_money = cursor.fetchone()[0]
                if player_money >= cost:
                    cursor.execute("""
                        UPDATE players
                        SET money = money - %s
                        WHERE id = %s
                    """, (cost, player_id))
                    cursor.execute("""
                        UPDATE properties
                        SET owner_id = %s
                        WHERE id = %s
                    """, (player_id, property_id))
                    conn.commit()
                    print(f"Player {player_id} has bought {property_id} for ${cost}.")
                else:
                    print(f"Player {player_id} does not have enough money to buy {property_id}.")
            else:
                print(f"Property {property_id} is already owned by Player {owner_id}.")
        conn.close()

def pay_rent(player_id, property_id):
    # Handles rent payment when a player lands on a property owned by another player.

    conn = connect()
    if conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT cost, rent, owner_id FROM properties WHERE id = %s", (property_id,))
            property_data = cursor.fetchone()
            cost, rent, owner_id = property_data
            if owner_id != player_id:  # Only pay rent if the player isn't the owner
                cursor.execute("SELECT money FROM players WHERE id = %s", (player_id,))
                player_money = cursor.fetchone()[0]
                if player_money >= rent:
                    cursor.execute("""
                        UPDATE players
                        SET money = money - %s
                        WHERE id = %s
                    """, (rent, player_id))
                    cursor.execute("""
                        UPDATE players
                        SET money = money + %s
                        WHERE id = %s
                    """, (rent, owner_id))
                    conn.commit()
                    print(f"Player {player_id} has paid ${rent} in rent to Player {owner_id}.")
                else:
                    print(f"Player {player_id} does not have enough money to pay rent.")
            else:
                print(f"Player {player_id} owns {property_id}, no rent needed.")
        conn.close()

def sell_property(player_id, property_id):
    """Allows a player to sell a property back to the bank for half its original cost."""
    conn = connect()
    if conn:
        with conn.cursor() as cursor:
            try:
                cursor.execute("SELECT cost, owner_id FROM properties WHERE id = %s", (property_id,))
                property_data = cursor.fetchone()
                if not property_data:
                    print("Invalid property ID.")
                    return

                cost, owner_id = property_data
                if owner_id != player_id:
                    print("You do not own this property.")
                    return

                # Refund half the property's value
                sale_price = cost // 2
                cursor.execute("""
                    UPDATE players SET money = money + %s WHERE id = %s
                """, (sale_price, player_id))

                # Reset ownership
                cursor.execute("""
                    UPDATE properties SET owner_id = NULL, improvements = 0 WHERE id = %s
                """, (property_id,))
                conn.commit()
                print(f"Player {player_id} sold property {property_id} for ${sale_price}.")
            except Exception as e:
                print("Error selling property:", e)
                conn.rollback()
            finally:
                conn.close()
