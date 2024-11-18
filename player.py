class Player:
    def __init__(self, name, money, turn_order):
        self.name = name
        self.money = money
        self.turn_order = turn_order

    def save_to_db(self, connection):
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO players (name, money, turn_order) 
                VALUES (%s, %s, %s) RETURNING id
            """, (self.name, self.money, self.turn_order))
            player_id = cursor.fetchone()[0]
            connection.commit()
            self.id = player_id
            print(f"Player {self.name} added to the game with ID: {self.id}")

if __name__ == "__main__":
    from database import connect

    conn = connect()
    if conn:
        player = Player("James", 1500, 1)
        player.save_to_db(conn)
        conn.close()
