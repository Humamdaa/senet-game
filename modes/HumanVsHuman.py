from utils.RandomStep import Random
from game.Board import Board
from game.Rules import Rules
from game.Render import Render
from game.StateGenerator import StateGenrator


class HumanVsHuman:
    def __init__(self, board):
        self.board: Board = board
        self.rand = Random()

    def start(self):
        Render.draw_board(self.board.grid)

        while True:
            dist = self.rand.roll_distance()

            print(f"\n{self.board.get_current_player()} rolled: {dist}")

            # Ask for simulation or actual move
            user_input = input(
                f"Select the piece to move (distance = {dist}) or press N to simulate: "
            ).strip()

            # Simulation mode
            if user_input.upper() == "N":
                Rules.show_simulations(self.board, dist)
                print("\n" + "=" * 50)
                Render.draw_board(self.board.grid)
                continue

            # Actual move mode
            while True:
                print("\n" + "=" * 50)
                print(f"{self.board.get_current_player()} can move {dist} cells")

                # If user already entered a number before, use it
                if user_input.isdigit():
                    cur_pos = int(user_input)
                    user_input = None  # reset for next loop
                else:
                    # Ask again for a valid number
                    cur_pos = input("Select the piece to move: ").strip()
                    if not cur_pos.isdigit():
                        print("Invalid input. Enter a number.")
                        continue
                    cur_pos = int(cur_pos)

                # Convert to zero-based index
                pos_index = cur_pos - 1

                if Rules.checkMove(self.board, pos_index, dist):
                    Rules.move(self.board, pos_index, dist)
                    Render.draw_board(self.board.grid)
                    self.board.switchPlayer()
                    break

                print("Try again my dear")

