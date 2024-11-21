from database import connect


def buy_property(player_id, property_id):
    conn = connect()
    if conn:
        cursor = conn.cursor()
        try:
            # Check the property cost
            cursor.execute("SELECT cost FROM properties WHERE id = %s", (property_id,))
            cost = cursor.fetchone()[0]

            # Update player's money
            cursor.execute("UPDATE players SET money = money - %s WHERE id = %s", (cost, player_id))

            # Update property ownership
            cursor.execute("UPDATE properties SET owner_id = %s WHERE id = %s", (player_id, property_id))

            conn.commit()
            print(f"Player {player_id} bought property {property_id} for {cost}.")
        except Exception as e:
            print("Error buying property:", e)
            conn.rollback()
        finally:
            cursor.close()
            conn.close()


if __name__ == "__main__":
    player_id = int(input("Enter player ID: "))
    property_id = int(input("Enter property ID: "))
    buy_property(player_id, property_id)
