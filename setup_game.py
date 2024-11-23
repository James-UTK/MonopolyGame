from player import add_player
from property import add_property, add_predefined_properties
from space import add_space

def setup_game():
    # Set up players
    num_players = int(input("Enter the number of players: "))
    for i in range(num_players):
        name = input(f"Enter the name for player {i + 1}: ")
        money = int(input(f"Enter starting money for player {name}: "))
        turn_order = i + 1
        add_player(name, money, turn_order)

    # Add predefined properties
    add_predefined_properties()

    # Add custom non-property spaces
    non_property_spaces = [
        ("Go", "Collect $200 salary as you pass."),
        ("Jail", "Just visiting or stay for 3 turns."),
        ("Chance", "Draw a Chance card for a random event."),
        ("Income Tax", "Pay 10% of your total money or $200."),
    ]
    for space in non_property_spaces:
        add_space(space[0], space[1])

if __name__ == "__main__":
    setup_game()
