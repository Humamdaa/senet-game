# Board.py
from Cell import Cell
from SpecialSquareRules import SpecialSquareRules


PIECE_NUM = 7

class Board:
    def __init__(self, grid_data):
        self.grid_data = grid_data
        self.level = grid_data.get("name", "Level 1")
        self.size = grid_data["size"]
        self.grid: list[Cell] = self.create_grid_from_data1(grid_data["grid"])
        self.current_player = 'A'
        
        # إنشاء كائن قواعد المربعات الخاصة
        self.special_rules = SpecialSquareRules(self)
        
        # إزالة المتغيرات المكرورة
        # self.last_roll = 0  # محذوف
        # self.piece_on_28 = None  # محذوف
        # self.piece_on_29 = None  # محذوف
        # self.piece_on_30 = None  # محذوف

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
        # طباعة الأرقام كما هي
        for i in range(1, 11):
            print(i, end=" ")
        print()
        
        # إعادة ترتيب اللوحة
        data = list(self.grid)
        result = data[:10] + list(reversed(data[10:20])) + data[20:]
        
        # طباعة اللوحة
        for i, cell in enumerate(result):
            if i % 10 == 0:
                print()
            print(cell.get_value(), end=" ")
    
    def checkMove(self, cur_pos, dist):
        print(f"cur = {cur_pos}  dist = {dist}")
        
        # التحقق الأساسي من الحدود
        if cur_pos < 0 or cur_pos >= 30:
            return False
            
        if self.grid[cur_pos].get_value() != self.current_player:
            return False
        
        # حساب الهدف
        target = cur_pos + dist
        
        # إذا كان الهدف خارج اللوحة
        if target >= 30:
            # السماح فقط بالهبوط الدقيق على المربع 30
            if target > 30:
                print("❌ Need exact roll to exit (must land on square 30)")
                return False
            return True
        
        # تحقق من حدود الهدف
        if target < 0 or target >= 30:
            return False
            
        # تحقق من أن الهدف ليس فيه قطعة لنفس اللاعب
        if self.grid[target].get_value() == self.current_player:
            return False
        
        # التحقق من قاعدة بيت السعادة
        if not self.special_rules.can_pass_happiness_house(cur_pos, dist):
            return False

        print('can move !')
        return True
    
    def move(self, cur_pos, dist):
        target = cur_pos + dist
        
        if not self.checkMove(cur_pos, dist):
            print("wrong input")
            return
        
        # تحديث الرمية الأخيرة في قواعد المربعات الخاصة
        self.special_rules.update_last_roll(dist)
        
        source_cell = self.grid[cur_pos]
        target_cell = self.grid[target]
        
        # أولاً: التحقق من القواعد الخاصة
        is_special_handled = self.special_rules.handle_special_square(
            cur_pos, target, source_cell, target_cell, self.current_player
        )
        
        # إذا لم يكن المربع خاصاً، ننفذ الحركة العادية
        if not is_special_handled:
            print(f"Moving to normal square {target + 1}")
            
            if target_cell.is_empty():
                print('empty')
                target_cell.set_value(source_cell.get_value())
                source_cell.set_value('.')
                
            elif target_cell.is_special():
                # إذا كان المربع خاصاً ولكن لم يتعامل معه handle_special_square
                # (هذا لا يجب أن يحدث، لكنه احتياطي)
                print('special (fallback)')
                target_cell.set_value(source_cell.get_value())
                source_cell.set_value('.')
                
            elif target_cell.is_player_piece():
                print('player swap')
                source_val = source_cell.get_value()
                target_val = target_cell.get_value()
                source_cell.set_value(target_val)
                target_cell.set_value(source_val)
        
        # ثانياً: التحقق من المربعات الخاصة بعد الحركة
        self.special_rules.check_special_squares_after_move(self.current_player)
        
        # ثالثاً: تبديل اللاعب
        # self.switchPlayer()
    
    def switchPlayer(self):
        if self.current_player == "A":
            self.current_player = "B"
        else:
            self.current_player = "A"
        print(f"Switched to Player {self.current_player}")