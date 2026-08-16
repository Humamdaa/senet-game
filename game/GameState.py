# game/GameState.py
from copy import deepcopy
from game.Rules import Rules
from game.StateGenerator import StateGenrator

class GameState:
    def __init__(self, board, current_player):
        self.board = board
        self.current_player = current_player

    def clone(self):
        return GameState(deepcopy(self.board), self.current_player)

    def apply_move(self, move):
        from_pos = move["from"] - 1
        dist = move["dist"]
        Rules.move(self.board, from_pos, dist)
        # بعد الحركة نبدل اللاعب
        self.current_player = "B" if self.current_player == "A" else "A"

    def get_legal_moves(self, dice_value):
        state_gen = StateGenrator(self.board)
        return state_gen.generate_legal_moves(dice_value)

    def is_terminal(self):
        return self.board.has_player_won("A") or self.board.has_player_won("B")
