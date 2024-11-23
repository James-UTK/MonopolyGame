# This file controls the game flow, including player turns, movement, and interactions with properties and spaces.
from player import add_player, update_player_money
from property import add_property, add_predefined_properties, buy_property, pay_rent, sell_property
from space import add_predefined_spaces
from roll_dice import roll_dice
from improve_property import improve_property
from reset_database import reset_database
from database import connect

# Define the game board as an ordered list of spaces
BOARD = [
    "Go", "Mediterranean Avenue", "Community Fund", "Baltic Avenue",
    "Income Tax", "Jail", "Oriental Avenue", "Vermont Avenue",
    "Connecticut Avenue", "Luxury Tax", "Park Place", "Boardwalk"
]


def setup_game():
    # Initializes the game by resetting the database, adding players, and setting up predefined properties and spaces.

    reset_database()  # Ensure the database is clear at the start

    # Ensure the number of players is between 1 and 8
    while True:
        num_players = int(input("Enter the number of players (1-8): "))
        if 1 <= num_players <= 8:
            break
        print("Invalid number of players. Please enter a number between 1 and 8.")

    for i in range(num_players):
        name = input(f"Enter name for player {i + 1}: ")
        if name.lower() == "quit":
            print("Game ended by user.")
            return
        money = 1500  # Starting money
        turn_order = i + 1
        add_player(name, money, turn_order)

    # Add predefined properties and spaces
    add_predefined_properties()
    add_predefined_spaces()


def update_player_position(cursor, player_id, new_position):
    try:
        cursor.execute("""UPDATE players SET position = %s WHERE id = %s""", (new_position, player_id))
        cursor.connection.commit()
        print(f"Updated player {player_id}'s position to {new_position}.")
    except Exception as e:
        print("Error updating player position:", e)
        cursor.connection.rollback()


def get_player_money(cursor, player_id):
    try:
        cursor.execute("SELECT money FROM players WHERE id = %s", (player_id,))
        money = cursor.fetchone()[0]
        return money
    except Exception as e:
        print("Error fetching player money:", e)
        return 0


def check_bankruptcy(cursor, player_id, player_name, players):
    cursor.execute("SELECT money FROM players WHERE id = %s", (player_id,))
    money = cursor.fetchone()[0]

    if money <= 0:
        cursor.execute("SELECT id FROM properties WHERE owner_id = %s", (player_id,))
        properties = cursor.fetchall()

        if not properties:
            print(f"{player_name} is bankrupt and out of the game!")
            return [p for p in players if p[0] != player_id]  # Remove the player
        else:
            print(f"{player_name} is bankrupt. Selling all properties.")
            for property_id in properties:
                sell_property(player_id, property_id[0])

    return players


def handle_player_turn(player_id, player_name):
    # Start the player's turn and display their name.
    print(f"{player_name}'s turn.")

    # Prompt the player to either roll the dice or quit the game.
    input_value = input(f"{player_name}, press Enter to roll the dice or type 'quit' to end the game: ")

    # If the player types 'quit', end the game.
    if input_value.lower() == "quit":
        return "quit"

    dice1, dice2 = roll_dice()  # Using the roll_dice function here
    total_roll = dice1 + dice2  # Calculate the total roll
    print(f"Rolled: {dice1} and {dice2}, Total roll: {total_roll}")

    # Open a single connection for all operations in this turn
    conn = connect()
    if not conn:
        return

    cursor = conn.cursor()
    cursor.execute("SELECT position FROM players WHERE id = %s", (player_id,))
    current_position = cursor.fetchone()[0]

    # Calculate new position
    new_position = (current_position + total_roll) % len(BOARD)
    update_player_position(cursor, player_id, new_position)

    # Determine the space landed on
    landed_space = BOARD[new_position]
    print(f"{player_name} landed on {landed_space}.")

    player_money = get_player_money(cursor, player_id)
    print(f"{player_name}, you have ${player_money}.")

    if landed_space in ["Go", "Community Fund", "Income Tax", "Luxury Tax", "Jail"]:
        # Handle non-property spaces
        if landed_space == "Go":
            print("You passed Go! Collect $200.")
            update_player_money(player_id, 200)

        elif landed_space == "Jail":
            print("Just visiting jail. No action needed.")
        elif landed_space == "Community Fund":
            amount = 50
            print(f"{landed_space}: Receive or pay {amount}.")
            if total_roll % 2 == 0:  # Simple logic to alternate
                print(f"You receive ${amount}.")
                update_player_money(player_id, amount)

            else:
                print(f"You pay ${amount}.")
                update_player_money(player_id, -amount)
        elif landed_space in ["Income Tax", "Luxury Tax"]:
            tax_amount = 200 if landed_space == "Income Tax" else 100
            print(f"Pay {tax_amount} for {landed_space}.")
            update_player_money(player_id, -tax_amount)
    else:
        # Handle property spaces
        cursor.execute("SELECT id, cost FROM properties WHERE name = %s", (landed_space,))
        property_data = cursor.fetchone()
        if property_data:  # Prevents crash if property is not found
            property_id, property_cost = property_data
            cursor.execute("SELECT owner_id FROM properties WHERE id = %s", (property_id,))
            owner_id = cursor.fetchone()[0]
            if owner_id:
                if owner_id != player_id:
                    pay_rent(player_id, property_id)
                else:
                    improve_property(player_id, property_id)
            else:
                while True:
                    choice = input(f"Do you want to buy {landed_space} for ${property_cost}? (yes/no): ")
                    if choice.lower() in ["yes", "no"]:
                        break
                    print("Invalid input. Please enter 'yes' or 'no'.")
                if choice.lower() == "yes":
                    buy_property(player_id, property_id)
                else:
                    print("Property not bought.")

    player_money = get_player_money(cursor, player_id)
    print(f"{player_name}, your new balance is ${player_money}.")

    cursor.close()
    conn.close()


def play_game():
    # Runs the main game loop, managing player turns, checking for bankruptcy, and determining the winner.

    conn = connect(print_message=True)  # Print message only once at setup
    if not conn:
        return

    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM players ORDER BY turn_order")
    players = cursor.fetchall()

    game_over = False
    while not game_over:
        for player_id, player_name in players:
            result = handle_player_turn(player_id, player_name)
            if result == "quit":
                game_over = True
                break

            # Check for bankruptcy
            players = check_bankruptcy(cursor, player_id, player_name, players)

            # Check for a winner
            if len(players) == 1:
                print(f"Congratulations, {players[0][1]} wins!")
                game_over = True
                break

    cursor.close()
    conn.close()
    reset_database()
    print("Game Over. Database reset.")


if __name__ == "__main__":
    setup_game()
    play_game()
