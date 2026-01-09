from Cell import Cell


PIECE_NUM = 7

class Board:
    def __init__(self, grid_data):
        self.grid_data = grid_data
        self.level = grid_data.get("name", "Level 1")
        self.size = grid_data["size"]
        self.grid: list[Cell] = self.create_grid_from_data1(grid_data["grid"])
        self.current_player = 'A'
        self.last_roll = 0  # لتتبع الرمية الأخيرة
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
        for i in range(1,11):
            print(i,end=" ")
        print()
        data = list(self.grid)
        result = data[:10] + list(reversed(data[10:20])) + data[20:]
        for i,cell in enumerate(result):
            if i%10==0:
                print()
            print(cell.get_value(), end=" ")
            
    def move(self, cur_pos, dist):
        target = cur_pos + dist
        if not self.checkMove(cur_pos, dist):
            print("wrong input")
            return
        
        self.last_roll = dist

        source_cell = self.grid[cur_pos]
        target_cell = self.grid[target]

        new_target = self.apply_special_square_rules(target, cur_pos, dist)
        if new_target != target:
            print(f"Special rule applied! New target: {new_target}")
            target = new_target
            target_cell = self.grid[target]
        
        if target_cell.is_empty():
            print('empty')
            target_cell.set_value(source_cell.get_value())
            source_cell.set_value('.')

        elif target_cell.is_special():
            self.handle_special_cell(target, cur_pos, source_cell)

        elif target_cell.is_player_piece():
            print('player')
            source_val = source_cell.get_value()
            target_val = target_cell.get_value()
            source_cell.set_value(target_val)
            target_cell.set_value(source_val)

        # self.switchPlayer()
    def checkMove(self, cur_pos, dist):
        
        print(f"cur = {cur_pos}  dist = {dist}")
        if cur_pos < 0 or cur_pos >= 30:
            return False
            
        if self.grid[cur_pos].get_value() != self.current_player \
                or self.grid[cur_pos + dist].get_value() == self.current_player:
            return False

        print('can move !')
        return True

    def apply_special_square_rules(self, target, cur_pos, dist):
        
        if target == 26:
            print("Landed on House of Happiness (26)")
            
        elif target == 27:
            print("Landed on House of Water (27) - Going to Rebirth House!")
            return self.go_to_rebirth_house()
            
        elif target == 28:
            print("Landed on House of Three Truths (28)")
            self.piece_on_28 = self.current_player
            return target
            
        elif target == 29:
            print("Landed on House of Re-Atoum (29)")
            self.piece_on_29 = self.current_player
            return target
            
        elif target == 30:
            print("Landed on House of Horus (30)")
            self.piece_on_30 = self.current_player
            return target
            
        return target
    
    def handle_special_cell(self, target, cur_pos, source_cell):
        target_cell = self.grid[target]
        
        if target_cell.is_empty():
            target_cell.set_value(source_cell.get_value())
            source_cell.set_value('.')
        else:
            source_val = source_cell.get_value()
            target_val = target_cell.get_value()
            source_cell.set_value(target_val)
            target_cell.set_value(source_val)
    
    def switchPlayer(self):
        if self.current_player == "A":
            self.current_player="B"
        else:
            self.current_player="A"

