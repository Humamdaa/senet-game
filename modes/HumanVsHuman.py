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

            if self._check_win():
                return

            print(f"\n{self.board.get_current_player()} rolled: {dist}")

            # Ask for simulation or actual move
            user_input = input(
                f"Select the piece to move (distance = {dist}) or press N to simulate: "
            ).strip()

            # Simulation mode
            if user_input.upper() == "N":
                self._handle_simulation(dist)
                continue

            # Actual move mode
            self._handle_real_move(dist, user_input)


# ===========================================
# ========== Helper functions ============
# ===========================================

    def _check_win(self):
        if self.board.has_player_won(self.board.get_current_player()):
            print(f"🎉 Player {self.board.get_current_player()} wins!")
            return True

        return False

    def _handle_simulation(self, dist):
        print("\nSimulation Mode")
        Rules.show_simulations(self.board, dist)
        print("\n" + "=" * 50)
        Render.draw_board(self.board.grid)

    def _handle_real_move(self, dist, first_input):
        while True:
            print("\n" + "=" * 50)
            print(f"{self.board.get_current_player()} can move {dist} cells")

            pos_index = self._get_valid_piece_input(first_input)
            first_input = ""  # reset after first use

            if Rules.checkMove(self.board, pos_index, dist):
                Rules.move(self.board, pos_index, dist)
                Render.draw_board(self.board.grid)
                self.board.switchPlayer()
                break

            print("Try again my dear")

    def _get_valid_piece_input(self, first_input):
        # If the first input was numeric, use it once
        if first_input.isdigit():
            return int(first_input) - 1

        # Otherwise ask until valid
        while True:
            user_input = input("Select the piece to move: ").strip()
            if user_input.isdigit():
                return int(user_input) - 1
            print("Invalid input. Enter a number.")
