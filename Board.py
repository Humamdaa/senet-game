from Cell import Cell


PIECE_NUM = 7


class Board:
    def __init__(self, grid_data):
        self.level = grid_data.get("name", "Level 1")
        self.size = grid_data["size"]
        self.grid: list[Cell] = self.create_grid_from_data1(grid_data["grid"])
        self.current_player = 'A'
        self.special_squares = {
            15: "House of Rebirth",      # بيت البعث
            26: "House of Happiness",    # بيت السعادة
            27: "House of Water",        # بيت الماء
            28: "House of Three Truths",  # بيت الحقائق الثلاث
            29: "House of Re-Atoum",     # بيت إعادة أتوم
            30: "House of Horus"         # بيت حورس
        }

    def get_current_player(self):
        return self.current_player

    def set_current_player(self, cur_player):
        self.current_player = cur_player

    def create_grid_from_data1(self, data):
        grid = []
        for i, value in enumerate(data):
            cell = Cell(i,  value)
            grid.append(cell)
        return grid

    def draw_board2(self):
        arr = []
        for i, cell in enumerate(self.grid):

            if 10 <= i <= 19:
                arr.append(cell.value)

            if i == 19:
                print(" ".join(reversed(arr)), end=" ")

            if i % 10 == 0:
                print()
            if not (10 <= i <= 19):
                print(cell.get_value(), end=" ")

    def draw_board(self):
        data = list(self.grid)
        result = data[:10] + list(reversed(data[10:20])) + data[20:]
        for i, cell in enumerate(result):
            if i % 10 == 0:
                print()
            print(cell.get_value(), end=" ")

    def move(self, cur_pos, dist):
        if not self.checkMove(cur_pos, dist):
            return

        target = cur_pos + dist
        
        source_cell = self.grid[cur_pos]
        target_cell = self.grid[target]

        if target_cell.is_empty():
            target_cell.set_value(source_cell.get_value())
            source_cell.set_value('.')

        elif target_cell.is_special():
            pass

        elif target_cell.is_player_piece():
            print('player')
            source_val = source_cell.get_value()
            target_val = target_cell.get_value()
            source_cell.set_value(target_val)
            target_cell.set_value(source_val)

        self.set_current_player(self.switchPlayer())

    def checkMove(self, cur_pos, dist):
        if self.grid[cur_pos].get_value() != self.current_player \
                or self.grid[cur_pos + dist].get_value() == self.current_player:
            return False

        print('can move !')
        return True

    def switchPlayer(player):
        if player == 'A':
            return 'B'
        return 'A'
