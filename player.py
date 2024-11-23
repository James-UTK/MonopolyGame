# Manages player-related actions such as updating money, position, and handling player creation.
from database import connect

class Player:
    def __init__(self, name, money, turn_order, position=0):
        self.name = name
        self.money = money
        self.turn_order = turn_order
        self.position = position

    def save_to_db(self, connection):
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO players (name, money, turn_order, position) 
                VALUES (%s, %s, %s, %s) RETURNING id
            """, (self.name, self.money, self.turn_order, self.position))
            player_id = cursor.fetchone()[0]
            connection.commit()
            self.id = player_id
            print(f"Player {self.name} added to the game with ID: {self.id}")

    @staticmethod
    def get_player_money(player_id, connection):
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT money FROM players WHERE id = %s", (player_id,))
                money = cursor.fetchone()[0]
                return money
        except Exception as e:
            print("Error fetching player money:", e)
            return 0

def add_player(name, money, turn_order):
    # Adds a new player to the database with the specified name, starting money, and turn order.

    conn = connect()
    if conn:
        player = Player(name, money, turn_order)
        player.save_to_db(conn)
        conn.close()

def update_player_money(player_id, amount):
    # Updates a player's money by the specified amount (positive or negative).

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
    name = input("Enter player name: ")
    money = int(input("Enter starting money: "))
    turn_order = int(input("Enter turn order: "))
    add_player(name, money, turn_order)
