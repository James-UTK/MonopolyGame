from database import connect


def pay_rent(player_id, property_id):
    conn = connect()
    if conn:
        cursor = conn.cursor()
        try:
            # Get property rent and owner
            cursor.execute("SELECT rent, owner_id FROM properties WHERE id = %s", (property_id,))
            rent, owner_id = cursor.fetchone()

            # Update player's money
            cursor.execute("UPDATE players SET money = money - %s WHERE id = %s", (rent, player_id))

            # Update owner's money
            cursor.execute("UPDATE players SET money = money + %s WHERE id = %s", (rent, owner_id))

            conn.commit()
            print(f"Player {player_id} paid {rent} in rent to player {owner_id}.")
        except Exception as e:
            print("Error paying rent:", e)
            conn.rollback()
        finally:
            cursor.close()
            conn.close()


if __name__ == "__main__":
    player_id = int(input("Enter player ID: "))
    property_id = int(input("Enter property ID: "))
    pay_rent(player_id, property_id)
