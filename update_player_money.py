from database import connect

def update_player_money(player_id, amount):
    conn = connect()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE players
                SET money = money + %s
                WHERE id = %s
            """, (amount, player_id))
            conn.commit()
            print(f"Updated player {player_id}'s money by {amount}.")
        except Exception as e:
            print("Error updating player money:", e)
            conn.rollback()
        finally:
            cursor.close()
            conn.close()

if __name__ == "__main__":
    player_id = int(input("Enter player ID: "))
    amount = int(input("Enter amount to update money by: "))
    update_player_money(player_id, amount)
