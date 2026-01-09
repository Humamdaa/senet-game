from game.Cell import Cell


PIECE_NUM = 7


class Board:
    def __init__(self, grid_data):
        self.level = grid_data.get("name", "Level 1")
        self.size = grid_data["size"]
        self.grid: list[Cell] = self._create_grid_from_data1(grid_data["grid"])
        self.current_player = 'A'
        self.last_move = 0  # لتتبع الرمية الأخيرة
        self.piece_on_28 = None  # لتتبع القطعة على المربع 28
        self.piece_on_29 = None  # لتتبع القطعة على المربع 29
        self.piece_on_30 = None  # لتتبع القطعة على المربع 30

        self.special_squares = {
            15: "House of Rebirth",      # بيت البعث
            26: "House of Happiness",    # بيت السعادة
            27: "House of Water",        # بيت الماء
            28: "House of Three Truths",  # بيت الحقائق الثلاث
            29: "House of Re-Atoum",     # بيت إعادة أتوم
            30: "House of Horus"         # بيت حورس
        }

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
