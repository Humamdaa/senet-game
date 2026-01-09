from Cell import Cell


PIECE_NUM = 7

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BEIGE = (245, 245, 220)
GRAY = (169, 169, 169)


class Board1:
    def __init__(self, current_player=None):
        self.board = [[0 for _ in range(10)] for _ in range(3)]
        self.white_left = PIECE_NUM
        self.gray_left = PIECE_NUM
        self.dice_num = 0
        self.turn = GRAY
        self.current_player = current_player
        self.create_pieces()

    def set_current_player(self, player):
        self.current_player = player

    def get_current_player(self):
        return self.current_player

    def change_turn(self):
        if self.turn == GRAY:
            self.turn = WHITE
            self.set_current_player(self.white_player)
        else:
            self.board.turn = GRAY
            self.board.set_current_player(self.gray_player)

        self.state = 'ROLL'
        self.board.update_dice(0)

    def draw_board(self):
        pass

    # def create_pieces(self):
    #     for col in range(COLS):
    #         if col % 2 == 0:
    #             self.board[0][col] = Piece(0, col, WHITE)
    #         else:
    #             self.board[0][col] = Piece(0, col, GRAY)
    #     for col in range(9, 5, -1):
    #         if col % 2 == 1:
    #             self.board[1][col] = Piece(1, col, WHITE)
    #         else:
    #             self.board[1][col] = Piece(1, col, GRAY)


class Board:
    def __init__(self, grid_data):
        self.grid_data = grid_data
        self.level = grid_data.get("name", "Level 1")
        self.size = grid_data["size"]
        self.grid: list[Cell] = self.create_grid_from_data1(grid_data["grid"])
        self.current_player = 'A'
<<<<<<< Updated upstream

        # بناء المسار مباشرة عند التهيئة
        # self.path = self.build_path()
=======
        self.last_move = 0  # لتتبع الرمية الأخيرة
        self.piece_on_28 = None  # لتتبع القطعة على المربع 28
        self.piece_on_29 = None  # لتتبع القطعة على المربع 29
        self.piece_on_30 = None  # لتتبع القطعة على المربع 30
        
        self.special_squares = {
            15: "House of Rebirth",      # بيت البعث
            26: "House of Happiness",    # بيت السعادة
            27: "House of Water",        # بيت الماء
            28: "House of Three Truths", # بيت الحقائق الثلاث
            29: "House of Re-Atoum",     # بيت إعادة أتوم
            30: "House of Horus"         # بيت حورس
        }
>>>>>>> Stashed changes

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

    def draw_board(self):
<<<<<<< Updated upstream
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

=======
        for i in range(1,11):
            print(i,end=" ")
        print()
        data = list(self.grid)
        result = data[:10] + list(reversed(data[10:20])) + data[20:]
        for i,cell in enumerate(result):
            if i%10==0:
                print()
            print(cell.get_value(), end=" ")
            
>>>>>>> Stashed changes
    def move(self, cur_pos, dist):

        target = cur_pos + dist
        if not self.checkMove(cur_pos, dist):
            print("wrong input")
            return
<<<<<<< Updated upstream

        print('hhhh')
=======
        
>>>>>>> Stashed changes
        source_cell = self.grid[cur_pos]
        target_cell = self.grid[target]

        if target_cell.is_empty():
            print('empty')
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
        self.switchPlayer()
    def checkMove(self, cur_pos, dist):
        
        print(f"cur = {cur_pos}  dist = {dist}")
        if cur_pos < 0 or cur_pos >= 30:
            return False
            
        if self.grid[cur_pos].get_value() != self.current_player \
                or self.grid[cur_pos + dist].get_value() == self.current_player:
            return False

        print('can move !')
        return True

<<<<<<< Updated upstream
    def switchPlayer(player):
        if player == 'A':
            return 'B'
        return 'A'

    # def build_path(self):
    #     """
    #     يبني مسار الحركة على شكل S:
    #     - الصف الأول: من اليسار لليمين
    #     - الصف الثاني: من اليمين لليسار
    #     - الصف الثالث: من اليسار لليمين
    #     """
    #     path = []
    #     for i in range(self.rows):
    #         if i % 2 == 0:  # الصفوف الزوجية (0, 2) → يسار لليمين
    #             for j in range(self.cols):
    #                 path.append(self.grid[i][j])
    #         else:           # الصفوف الفردية (1) → يمين لليسار
    #             for j in reversed(range(self.cols)):
    #                 path.append(self.grid[i][j])
    #     return path
=======
    def switchPlayer(self,player):
        if self.current_player == "A":
            self.current_player="B"
        else:
            self.current_player="A"

>>>>>>> Stashed changes
