from game.Cell import Cell
from game.SpecialSquareRules import SpecialSquareRules

PIECE_NUM = 7


class Board:
    def __init__(self, grid_data):
        self.level = grid_data.get("name", "Level 1")
        self.size = grid_data["size"]
        self.grid: list[Cell] = self._create_grid_from_data1(grid_data["grid"])
        self.current_player = 'A'
        self.last_move = 0  # لتتبع الرمية الأخيرة
        self.special_rules = SpecialSquareRules(self)
        self.counter = 0
    def get_cell(self, pos):
        return self.grid[pos]

    def get_current_player(self):
        return self.current_player

    def set_current_player(self, cur_player):
        self.current_player = cur_player

    def _create_grid_from_data1(self, data):
        grid = []
        for i, value in enumerate(data):
            cell = Cell(i,  value)
            grid.append(cell)
        return grid

    def switchPlayer(self):
        self.current_player = 'B' if self.current_player == 'A' else "A"
