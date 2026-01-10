from game.Board import Board
from game.Rules import Rules


class StateGenrator:
    def __init__(self, board: Board):
        self.board = board

    def generate_legal_moves(self):
        current_player = self.board.get_current_player()
        legal_moves = []

        for c, i in enumerate(self.board.grid):
            if current_player == c.get_value():
                for dist in range(1, 6):
                    if Rules.checkMove(self.board, i, dist):
                        target = i + dist
                        legal_moves.append({
                            "from": i,
                            "to": target,
                            "dist": dist
                        })

        return legal_moves
