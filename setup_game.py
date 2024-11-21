from add_player import add_player
from add_property import add_property
from add_space import add_space

def setup_game():
    num_players = int(input("Enter the number of players: "))
    for i in range(num_players):
        name = input(f"Enter name for player {i + 1}: ")
        money = int(input("Enter starting money for player: "))
        turn_order = i + 1
        add_player(name, money, turn_order)

    # Add properties
    add_property("Park Place", 350, 35)
    add_property("Boardwalk", 400, 50)

    # Add non-property spaces
    add_space("Go", "Collect $200 salary as you pass.")
    add_space("Jail", "Just visiting.")
    add_space("Chance", "Draw a Chance card.")
    add_space("Income Tax", "Pay 10% or $200.")

if __name__ == "__main__":
    setup_game()
