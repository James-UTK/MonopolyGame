from database import connect


def improve_property(player_id, property_id):
    conn = connect()
    if conn:
        cursor = conn.cursor()
        try:
            # Check if the player owns the property
            cursor.execute("SELECT owner_id FROM properties WHERE id = %s", (property_id,))
            owner_id = cursor.fetchone()[0]
            if owner_id != player_id:
                print("You do not own this property.")
                return

            # Calculate improvement cost
            improvement_cost = 100  # Example cost
            cursor.execute("UPDATE players SET money = money - %s WHERE id = %s", (improvement_cost, player_id))

            # Update property improvements
            cursor.execute("UPDATE properties SET improvements = improvements + 1 WHERE id = %s", (property_id,))

            conn.commit()
            print(f"Player {player_id} improved property {property_id}.")
        except Exception as e:
            print("Error improving property:", e)
            conn.rollback()
        finally:
            cursor.close()
            conn.close()


if __name__ == "__main__":
    player_id = int(input("Enter player ID: "))
    property_id = int(input("Enter property ID: "))
    improve_property(player_id, property_id)
