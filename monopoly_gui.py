import tkinter as tk
from tkinter import messagebox
import random


class MonopolyGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Monopoly Game")

        # Initialize players and player money before setting up the UI
        self.players = ["Player 1", "Player 2"]
        self.player_money = {"Player 1": 1500, "Player 2": 1500}
        self.current_player_index = 0

        self.setup_ui()

    def setup_ui(self):
        # Create main frames
        self.board_frame = tk.Frame(self.root)
        self.board_frame.pack(side=tk.LEFT, padx=10, pady=10)

        self.legend_frame = tk.Frame(self.root)
        self.legend_frame.pack(side=tk.RIGHT, padx=10, pady=10)

        # Create game board
        self.create_board()

        # Create legend
        self.create_legend()

        # Create dice
        self.create_dice()

    def create_board(self):
        # Example: Create a simple board with labeled spaces
        for i in range(5):
            for j in range(5):
                label = tk.Label(self.board_frame, text=f"{i},{j}", borderwidth=2, relief="groove", width=10, height=5)
                label.grid(row=i, column=j)

    def create_legend(self):
        # Example: Display player order and money
        self.legend_labels = []
        for player in self.players:
            label = tk.Label(self.legend_frame, text=f"{player}: ${self.player_money[player]}")
            label.pack()
            self.legend_labels.append(label)

    def create_dice(self):
        # Create dice roll button
        self.dice_label = tk.Label(self.root, text="Dice: 0, 0", font=("Helvetica", 16))
        self.dice_label.pack(pady=20)

        self.roll_button = tk.Button(self.root, text="Roll Dice", command=self.roll_dice)
        self.roll_button.pack(pady=20)

    def roll_dice(self):
        # Roll the dice and update the label
        dice1 = random.randint(1, 6)
        dice2 = random.randint(1, 6)
        self.dice_label.config(text=f"Dice: {dice1}, {dice2}")

        # Update player position
        current_player = self.players[self.current_player_index]
        messagebox.showinfo("Dice Roll", f"{current_player} rolled a {dice1} and a {dice2}")

        # Switch to the next player
        self.current_player_index = (self.current_player_index + 1) % len(self.players)


if __name__ == "__main__":
    root = tk.Tk()
    game = MonopolyGame(root)
    root.mainloop()
